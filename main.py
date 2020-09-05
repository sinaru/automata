#!/usr/bin/env python

import pydevd_pycharm
import yaml
from automata import process_entry
import automata.manager as manager

manager.init()
args = manager.console_input_args()

if args.remote_debug:
    pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)

with open(args.file) as file:
    content = yaml.load(file)

version = content.pop('version', '')

if version != '0.1':
    raise Exception("Unknown version")

for key in content.keys():
    process_entry(key, content[key])
