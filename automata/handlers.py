import hashlib
import subprocess
import apt
import requests


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
                raise Exception(f"Sorry, package installation failed [{str(arg)}]")


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


def process_file_block(files_data):
    for file_info in files_data:
        new_content = open(file_info['content']).read()
        open(file_info['path'], 'w').write(new_content)


def process_systemd_services(service_block):
    for service_name in service_block.keys():
        for action in service_block[service_name]:
            process_cmd = f"systemctl {action} {service_name}".split()
            process = subprocess.Popen(process_cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr != b'':
                raise Exception(stderr.decode())

key_function = {
    'apt_packages': 'process_apt_packages',
    'apt_keys': 'process_apt_keys',
    'sources': 'process_sources',
    'files': 'process_file_block',
    'systemd.services': 'process_systemd_services'
}