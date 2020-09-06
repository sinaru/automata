#!/usr/bin/env python

import pydevd_pycharm
import yaml
from automata import process_content
import os
import argparse


def init():
    if not os.path.exists('.automata/'):
        os.mkdir('.automata')


def console_input_args():
    parser = argparse.ArgumentParser(description='Automate machine setup')
    parser.add_argument('--file', help='Provide location of the YAML configuration file')
    parser.add_argument('--remote-debug', action='store_true', help=argparse.SUPPRESS, default=False)
    return parser.parse_args()


args = console_input_args()

if args.remote_debug:
    pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)

with open(args.file) as file:
    content = yaml.load(file)

version = content.pop('version', '')

if version != '0.1':
    raise Exception("Unknown version")

process_content(content)
