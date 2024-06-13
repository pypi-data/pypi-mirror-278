# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mflt_compact_log']

package_data = \
{'': ['*'],
 'mflt_compact_log': ['decode/decode.wasm',
                      'decode/decode.wasm',
                      'decode/decode_x86_64-linux.so',
                      'decode/decode_x86_64-linux.so']}

install_requires = \
['cbor2>=5,<6',
 'click>=8.0,<9.0',
 'prettytable>=3,<4',
 'pyelftools>=0.31,<0.32']

extras_require = \
{':python_version >= "3.10" and python_version < "3.11"': ['wasmer-py310==1.0.0',
                                                           'wasmer-compiler-cranelift-py310==1.0.0'],
 ':python_version >= "3.8" and python_version < "3.10"': ['wasmer==1.0.0',
                                                          'wasmer-compiler-cranelift==1.0.0']}

entry_points = \
{'console_scripts': ['mflt-compact-log.compact = mflt_compact_log.compact:main',
                     'mflt-compact-log.log_fmt = '
                     'mflt_compact_log.log_fmt:main']}

setup_kwargs = {
    'name': 'mflt-compact-log',
    'version': '0.0.4',
    'description': 'Memfault Compact Log Library',
    'long_description': '# Memfault Compact Log Library\n\nThis library enables decoding Memfault-flavored compact logs. For background\ninformation on compact logs, see here:\n\nhttps://mflt.io/compact-logs\n\n## Usage\n\nSome brief usage information below. See the source for detailed usage.\n\n### Extracting compact log format strings from .elf\n\nTo extract the format strings from the symbol file:\n\n```python\nfrom mflt_compact_log.log_fmt import LogFormatElfSectionParser\n\nelf = "path to elf file"\n# parse the elf file\nmappings = LogFormatElfSectionParser.get_mapping_from_elf_file(elf)\n# \'mappings\' is a dictionary mapping log id to LogFormatInfo data\nprint(mappings)\n\n>>> {8: LogFormatInfo(filename=\'./main/console_example_main.c\', line=245, n_args=0, fmt=\'This is a compact log example\')}\n```\n\n### Decoding compact logs\n\nTo apply the format string to raw compact log data:\n\n```python\nfrom mflt_compact_log.compact import CompactLogDecoder\n\n# example format string; this could instead be retrieved from the elf file\nfmt = "An Integer Format String: %d"\n\n# compact log hex encoded raw data\ncompact_log = "820A0B"\n\n# decode the log!\ncompact_log_as_bytes = bytes.fromhex(compact_log)\nlog = CompactLogDecoder.from_cbor_array(fmt, compact_log_as_bytes)\nlog.decode()\n>>> \'An Integer Format String: 11\'\n```\n\n## Changes\n\n### 0.0.4\n\n- Source pyelftools from https://pypi.org/project/pyelftools/ again, as the\n  required bugfixes have been merged upstream. See notes of 0.0.3 below.\n\n### 0.0.3\n\n- Source pyelftools from https://github.com/memfault/pyelftools while we are\n  waiting for 2 bugfixes to get merged upstream\n  (https://github.com/eliben/pyelftools/pull/537 and\n  https://github.com/eliben/pyelftools/pull/538).\n\n### 0.0.2\n\n- support Python 3.9 and 3.10\n- update `prettytable` dependency from `0.7.2` to `3.4.1`\n- update `pyelftools` dependency from `^0.28.0` to `^0.29.0`\n',
    'author': 'Memfault Inc',
    'author_email': 'hello@memfault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/memfault/memfault-firmware-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
