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
