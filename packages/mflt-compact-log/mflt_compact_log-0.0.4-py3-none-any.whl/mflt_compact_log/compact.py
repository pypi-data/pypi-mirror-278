import decimal
import functools
import logging
import os
import pathlib
import platform
import struct
from contextlib import contextmanager
from enum import IntEnum
from typing import Any

import cbor2
import click
from wasmer.wasmer import Instance, Module, Store, engine

log = logging.getLogger(__name__)

FILE_DIR = pathlib.Path(__file__).resolve().parent
WASM_EXE_DIR = FILE_DIR / "decode"
WASM_BYTECODE = WASM_EXE_DIR / "decode.wasm"


class CompactLogDecodeError(ValueError):
    pass


@functools.lru_cache(maxsize=1)
def load_wasm_program_serialized():
    machine = platform.machine().lower()  # i.e x86_64
    system = platform.system().lower()  # i.e linux
    wasm_exe = f"decode_{machine}-{system}.so"
    native_exe_path = WASM_EXE_DIR / wasm_exe
    if native_exe_path.exists() and not os.environ.get("MFLT_COMPACT_LOG_FORCE_JIT"):
        store = Store(engine.Native())
        log.info("Using Native WASM engine")
        return store, native_exe_path.read_bytes()
    else:
        # We don't have a pre-compiled runtime so compile on the fly
        # Lazy load import so we don't have to pull in dep for pre-compiled use case
        #
        # WARNING: We have seen random compiler hangs when this path is hit from certain
        # environments (i.e forked python child processes). If a hang is observed, first
        # try building a native binary using the native_engine.py script.
        log.info("Running a JIT WASM compilation")
        from wasmer_compiler_cranelift.wasmer_compiler_cranelift import Compiler

        store = Store(engine.JIT(Compiler))
        return store, Module(store, WASM_BYTECODE.read_bytes()).serialize()


class CompactLogPromotionType(IntEnum):
    INT32 = 0
    INT64 = 1
    DOUBLE = 2
    STRING = 3


class CompactLogDecoder:
    def __init__(self):
        store, serialized = load_wasm_program_serialized()
        self.wasm_instance = Instance(Module.deserialize(store, serialized))
        self.allocations = []

    @staticmethod
    def unpack_compact_log(
        input_args: list,
    ) -> tuple[int, list[tuple[CompactLogPromotionType, object]]]:
        """
        Unpacks CBOR encoded "compact logs" into the log_id & a va_arg array

        where,
         - log_id The id used to recover the C fmt string from an ELF
         - va_args A list of [ argument type, argument value ]

        More details about the encoding scheme in:
          sdk/embedded/components/log/src/memfault_compact_log_serializer.c
        """
        args = iter(input_args)
        log_fmt_id = next(args)
        arg_list: list[tuple[CompactLogPromotionType, Any]] = []

        for arg in args:
            if isinstance(arg, int):
                arg_list.append((CompactLogPromotionType.INT32, arg))
            elif isinstance(arg, list):
                arg_list.append((CompactLogPromotionType.INT64, arg[0]))
            elif isinstance(arg, float):
                arg_list.append((CompactLogPromotionType.DOUBLE, arg))
            elif isinstance(arg, str):
                arg_list.append((CompactLogPromotionType.STRING, arg))
            else:
                raise TypeError(f"Unknown arg type {arg}")

        return log_fmt_id, arg_list

    @contextmanager
    def _alloc_tracking(self):
        try:
            yield
        finally:
            for ptr in self.allocations:
                self.wasm_instance.exports.log_free(ptr)
            self.allocations = []

    def _zmalloc(self, length: int):
        pointer = self.wasm_instance.exports.log_zmalloc(length)
        self.allocations.append(pointer)
        return pointer

    def strdup(self, in_str: str):
        """
        Give a Python string, build a C NUL termintated string in the WASM runtime
        """
        # We are building a null terminated c-string
        pointer = self._zmalloc(len(in_str) + 1)

        # Copy python string into wasm environment
        memory = self.wasm_instance.exports.memory.uint8_view(pointer)
        for idx, c in enumerate(in_str.encode()):
            memory[idx] = c

        # return reference
        return pointer

    def build_va_args(self, va_args: list[tuple[CompactLogPromotionType, object]]):
        """
        Converts va_args as a Python List to a C-lang suitable format in the WASM runtime

        Note: The "..." (va_args) in C are just a pointer to a bytearray of arguments. The
        "fmt" is used for recovering the actual args. Arguments will always be 4 or 8 bytes
        and double-word args need to be double-word aligned.
        """
        curr_offset = 0
        c_va_args = bytearray()

        for arg_type, arg in va_args:
            # First check if it's a double-word and we need to pad
            # out to aligned boundary
            if arg_type in (CompactLogPromotionType.INT64, CompactLogPromotionType.DOUBLE):
                if curr_offset % 8 != 0:
                    # Pad out to double-word aligned boundary
                    c_va_args.extend(struct.pack("<I", 0))
                    curr_offset += 4

            if arg_type == CompactLogPromotionType.INT32:
                assert isinstance(arg, int)
                encoded_arg = struct.pack("<I", arg & 0xFFFFFFFF)
            elif arg_type == CompactLogPromotionType.INT64:
                assert isinstance(arg, int)
                encoded_arg = struct.pack("<q", arg)
            elif arg_type == CompactLogPromotionType.DOUBLE:
                assert isinstance(arg, int | float)
                encoded_arg = struct.pack("d", arg)
            elif arg_type == CompactLogPromotionType.STRING:
                assert isinstance(arg, str)
                str_ptr = self.strdup(arg)
                encoded_arg = struct.pack("<I", int(str_ptr))
            else:
                raise TypeError(f"Unexpected Arg {arg_type} {arg}")

            c_va_args.extend(encoded_arg)
            curr_offset += len(encoded_arg)

        # We've built what the memory layout for va_args should look like
        # Now let's copy it into the C env
        va_args_ptr = self._zmalloc(curr_offset)
        args_view = self.wasm_instance.exports.memory.uint8_view(va_args_ptr)
        for idx, b in enumerate(c_va_args):
            args_view[idx] = b

        return va_args_ptr

    def decode(self, c_fmt: str, va_args: list, *, max_result_len=512) -> bytes:
        """
        Converts compact log to a full byte string given a C fmt string & arg list

        Args:
          c_fmt: A format string suitable for libc's printf family of functions
          va_args: Argument output from unpack_compact_log
          max_result_len: Maximum length string to generate before truncating decode
        """
        with self._alloc_tracking():
            result_ptr = self._zmalloc(max_result_len)

            c_fmt_ptr = self.strdup(c_fmt)

            va_args_ptr = self.build_va_args(va_args)

            try:
                self.wasm_instance.exports.log_vsnprintf(
                    result_ptr, max_result_len, c_fmt_ptr, va_args_ptr
                )
            except RuntimeError as e:
                raise CompactLogDecodeError from e

            result = self.wasm_instance.exports.memory.uint8_view(result_ptr)
            result_str = bytes(result[0:max_result_len]).split(b"\x00")[0]
        return result_str

    @classmethod
    def from_cbor_array(cls, fmt_str, compact_log: bytes | bytearray | memoryview):
        """
        Helper for 1-off decoding a compact log.
        """
        try:
            args = cbor2.loads(compact_log, tag_hook=tag_hook)
        except (
            UnicodeDecodeError,
            ValueError,
            RecursionError,
            TypeError,
            LookupError,
            OSError,
            OverflowError,
            decimal.InvalidOperation,
            MemoryError,
        ) as e:
            raise cbor2.CBORDecodeValueError(str(e)) from e
        if not isinstance(args, list):
            raise TypeError(f"Type is {type(args)}. Expected <class 'list'>")

        _, va_args = cls.unpack_compact_log(args)
        compact_log_decoder = cls()
        return compact_log_decoder.decode(fmt_str, va_args)

    @classmethod
    def from_arg_list(cls, fmt_str, args: list):
        """
        Helper for 1-off decoding a format log that has been deserialized from cbor
        """
        _, va_args = cls.unpack_compact_log(args)
        compact_log_decoder = cls()
        return compact_log_decoder.decode(fmt_str, va_args)


def tag_hook(decoder: cbor2.CBORDecoder, tag: cbor2.CBORTag) -> object:
    if decoder.immutable:
        # We received a tagged value inside in a context where Python requires values
        # to be hashable (e.g. keys for a mapping). We need to bail here.
        raise cbor2.CBORDecodeValueError(f"Unsupported/unknown tagged value in mapping: {tag.tag}")

    return tag


@click.command()
@click.argument("fmt")
@click.argument("compact-log")
def main(fmt, compact_log):
    """
    Given a fmt string and hex string encoded compact log, recover original
    string

    Example Usage:

    \b
    $ python compact.py "An Integer Format String: %d" 820A0B
        Log Recovered:
        An Integer Format String: 11

    """
    compact_log_as_bytes = bytes.fromhex(compact_log)
    log = CompactLogDecoder.from_cbor_array(fmt, compact_log_as_bytes)
    click.secho("Log Recovered:")
    click.secho(log.decode(), fg="green")


if __name__ == "__main__":
    main()
