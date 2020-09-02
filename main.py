#!/usr/bin/env python

import apt
import sys
import yaml


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


with open('examples/lab/lab_1.yml') as file:
    content = yaml.load(file)

for key in content.keys():
    if key == 'packages':
        process_packages(content[key])
    else:
        raise Exception(f"Invalid type {key}")
