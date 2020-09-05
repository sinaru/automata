#!/usr/bin/env python

import pydevd_pycharm
import yaml
import os

from lib.handlers import process_apt_packages, process_apt_keys, process_sources, process_file_block, \
    process_systemd_services

# remote debugging
pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)

if not os.path.exists('.automata/'):
    os.mkdir('.automata')

with open('examples/lab/lab_1.yml') as file:
    content = yaml.load(file)

version = content.pop('version', '')

if version != '0.1':
    raise Exception("Unknown version")

for key in content.keys():
    data = content[key]
    if key == 'apt_packages':
        process_apt_packages(data)
    elif key == 'apt_keys':
        process_apt_keys(data)
    elif key == 'sources':
        process_sources(data)
    elif key == 'files':
        process_file_block(data)
    elif key == 'systemd.services':
        process_systemd_services(data)
    else:
        raise Exception(f"Invalid type {key}")
