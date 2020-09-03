#!/usr/bin/env python
import pydevd_pycharm
import apt
import sys
import yaml
import requests
import subprocess

pydevd_pycharm.settrace('localhost', port=8080, stdoutToServer=True, stderrToServer=True)


def process_packages(packages_data):
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


def process_apt_keys(data):
    for key_set in data:
        if key_set.get('url', False):
            r = requests.get(key_set['url'], allow_redirects=True)
            open('temp_key.gdp', 'wb').write(r.content)

            process = subprocess.Popen(['apt-key', 'add', 'temp_key.gdp'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, _stderr = process.communicate()
            if stdout != b'OK\n':
                raise Exception('failed to add key')


with open('examples/lab/lab_1.yml') as file:
    content = yaml.load(file)

version = content.pop('version', '')

if version != '0.1':
    raise Exception("Unknown version")

for key in content.keys():
    data = content[key]
    if key == 'packages':
        process_packages(data)
    elif key == 'apt_keys':
        process_apt_keys(data)
    else:
        raise Exception(f"Invalid type {key}")
