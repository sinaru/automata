#!/usr/bin/env python

import pydevd_pycharm
import yaml
import lib.manager as manager
from lib.handlers import process_apt_packages, process_apt_keys, process_sources, process_file_block, \
    process_systemd_services

manager.init()
args = manager.console_input_args()

if args.debug:
    pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)

with open(args.file) as file:
    content = yaml.load(file)

version = content.pop('version', '')

if version != '0.1':
    raise Exception("Unknown version")

key_function = {
    'apt_packages': 'process_apt_packages',
    'apt_keys': 'process_apt_keys',
    'sources': 'process_sources',
    'files': 'process_file_block',
    'systemd.services': 'process_systemd_services'
}

for key in content.keys():
    data = content[key]
    function = key_function.get(key, False)

    if not function:
        raise Exception(f"Invalid type {key}")

    locals()[function](data)
