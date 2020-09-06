import os
import shutil

from automata.handlers import process_apt_packages, process_apt_keys, process_sources, process_file_block, \
    process_systemd_services, process_version, process_bash_scripts

key_function = {
    'version': 'process_version',
    'apt_packages': 'process_apt_packages',
    'apt_keys': 'process_apt_keys',
    'sources': 'process_sources',
    'files': 'process_file_block',
    'systemd.services': 'process_systemd_services',
    'bash_scripts': 'process_bash_scripts',
}


def init():
    d_path = '.automata/'
    if os.path.exists(d_path):
        shutil.rmtree(d_path)
    os.mkdir(d_path)


def process_content(content):
    init()
    for entry in content:
        process_list_entry(entry)


def process_list_entry(data):
    for key in data.keys():
        process_entry(key, data[key])


def process_entry(section_name, data):
    function = key_function.get(section_name, False)

    if not function:
        raise Exception(f"Invalid type {section_name}")

    globals()[function](data)
