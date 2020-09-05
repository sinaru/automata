#!/usr/bin/env python

import pydevd_pycharm
import apt
import sys
import yaml
import requests
import subprocess
import os
import hashlib

# remote debugging
pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)


def process_apt_packages(packages_data):
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    for pkg_name in packages_data:
        pkg = cache[pkg_name]
        if pkg.is_installed:
            print(f"{pkg_name} already installed")
        else:
            print(f"[AUTOMATA LOG] Installing package: {pkg}")
            pkg.mark_install()

            try:
                cache.commit()
            except Exception as arg:
                print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))


def process_apt_keys(key_data):
    for key_set in key_data:
        if key_set.get('url', False):
            apt_key = key_set['url']
            key_name = hashlib.sha224(apt_key.encode()).hexdigest()
            key_path = f".automata/{key_name}.gdp"
            r = requests.get(apt_key, allow_redirects=True)
            open(key_path, 'wb').write(r.content)

            process = subprocess.Popen(['apt-key', 'add', key_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, _stderr = process.communicate()
            if stdout == b'OK\n':
                print(f"key added: {apt_key}")
            else:
                raise Exception('failed to add key')


def process_sources(sources_list):
    for source in sources_list:
        key_name = list(source.keys())[0]
        file_name = key_name + '.list'
        source_content = source[key_name]
        open(f"/etc/apt/sources.list.d/{file_name}", 'w').write(source_content)


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
    else:
        raise Exception(f"Invalid type {key}")
