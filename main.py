#!/usr/bin/env python3

import yaml
import argparse
from automata import process_content


def console_input_args():
    parser = argparse.ArgumentParser(description='Automate machine setup')
    parser.add_argument('--file', help='Provide location of the YAML configuration file')
    parser.add_argument('--remote-debug', action='store_true', help=argparse.SUPPRESS, default=False)
    return parser.parse_args()


args = console_input_args()

if args.remote_debug:
    import pydevd_pycharm

    pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)

with open(args.file) as file:
    content = yaml.load(file)

process_content(content)
