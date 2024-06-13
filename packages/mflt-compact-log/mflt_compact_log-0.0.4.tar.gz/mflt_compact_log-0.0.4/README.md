# Memfault Compact Log Library

This library enables decoding Memfault-flavored compact logs. For background
information on compact logs, see here:

https://mflt.io/compact-logs

## Usage

Some brief usage information below. See the source for detailed usage.

### Extracting compact log format strings from .elf

To extract the format strings from the symbol file:

```python
from mflt_compact_log.log_fmt import LogFormatElfSectionParser

elf = "path to elf file"
# parse the elf file
mappings = LogFormatElfSectionParser.get_mapping_from_elf_file(elf)
# 'mappings' is a dictionary mapping log id to LogFormatInfo data
print(mappings)

>>> {8: LogFormatInfo(filename='./main/console_example_main.c', line=245, n_args=0, fmt='This is a compact log example')}
```

### Decoding compact logs

To apply the format string to raw compact log data:

```python
from mflt_compact_log.compact import CompactLogDecoder

# example format string; this could instead be retrieved from the elf file
fmt = "An Integer Format String: %d"

# compact log hex encoded raw data
compact_log = "820A0B"

# decode the log!
compact_log_as_bytes = bytes.fromhex(compact_log)
log = CompactLogDecoder.from_cbor_array(fmt, compact_log_as_bytes)
log.decode()
>>> 'An Integer Format String: 11'
```

## Changes

### 0.0.4

- Source pyelftools from https://pypi.org/project/pyelftools/ again, as the
  required bugfixes have been merged upstream. See notes of 0.0.3 below.

### 0.0.3

- Source pyelftools from https://github.com/memfault/pyelftools while we are
  waiting for 2 bugfixes to get merged upstream
  (https://github.com/eliben/pyelftools/pull/537 and
  https://github.com/eliben/pyelftools/pull/538).

### 0.0.2

- support Python 3.9 and 3.10
- update `prettytable` dependency from `0.7.2` to `3.4.1`
- update `pyelftools` dependency from `^0.28.0` to `^0.29.0`
