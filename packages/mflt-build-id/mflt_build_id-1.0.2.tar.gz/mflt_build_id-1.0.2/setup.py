# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mflt_build_id']

package_data = \
{'': ['*']}

install_requires = \
['pyelftools>=0.31,<0.32']

entry_points = \
{'console_scripts': ['mflt_build_id = mflt_build_id:main']}

setup_kwargs = {
    'name': 'mflt-build-id',
    'version': '1.0.2',
    'description': 'Memfault Build Id injector',
    'long_description': '# Memfault Build ID Tool\n\nThis package contains the `mflt_build_id` CLI tool.\n\nThe purpose of the tool is simplify reading or writing\n[Build IDs](https://interrupt.memfault.com/blog/gnu-build-id-for-firmware) in a\nfirmware image irrespective of the compiler or build system being used in a\nproject.\n\n## Example Usage\n\n```\n$ mflt_build_id --help\nusage: mflt_build_id [-h] [--dump [DUMP]] [--crc CRC] [--sha1 SHA1] elf\n\nInspects provided ELF for a Build ID and when missing adds one if possible.\n\nIf a pre-existing Build ID is found (either a GNU Build ID or a Memfault Build ID),\nno action is taken.\n\nIf no Build ID is found, this script will generate a unique ID by computing a SHA1 over the\ncontents that will be in the final binary. Once computed, the build ID will be "patched" into a\nread-only struct defined in memfault-firmware-sdk/components/core/src/memfault_build_id.c to hold\nthe info.\n\nIf the --crc <symbol_holding_crc32> argument is used, instead of populating the Memfault Build ID\nstructure, the symbol specified will be updated with a CRC32 computed over the contents that will\nbe in the final binary.\n\nIf the --sha1 <symbol_holding_sha> argument is used, instead of populating the Memfault Build ID\nstructure, the symbol specified will be updated directly with Memfault SHA1 using the same strategy\ndiscussed above. The only expectation in this mode is that a global symbol has been defined as follow:\n\nconst uint8_t g_your_symbol_build_id[20] = { 0x1, };\n\nFor further reading about Build Ids in general see:\n  https://mflt.io//symbol-file-build-ids\n\npositional arguments:\n  elf\n\noptions:\n  -h, --help     show this help message and exit\n  --dump [DUMP]\n  --crc CRC\n  --sha1 SHA1\n```\n',
    'author': 'Memfault Inc',
    'author_email': 'hello@memfault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/memfault/memfault-firmware-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
