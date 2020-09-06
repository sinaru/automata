import subprocess

from automata.helpers import url_to_local_file_path, content_to_temp_path, run_command

'''
    import apt
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    
    pkg = cache[pkg_name]
        if pkg.is_installed:
            print(f"{pkg_name} already installed")
        else:
            print(f"[AUTOMATA LOG] Installing package: {pkg}")
            pkg.mark_install()
'''


def process_apt_packages(packages_data):
    process = subprocess.Popen(['sudo', 'apt', 'update'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr != b'':
        if stderr != b'\nWARNING: apt does not have a stable CLI interface. Use with caution in scripts.\n\n':
            raise Exception(stderr.decode())
    elif stdout != b'':
        print(stdout.decode())

    for pkg_name in packages_data:
        process = subprocess.Popen(['sudo', 'apt', 'install', pkg_name],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr != b'':
            if stderr != b'\nWARNING: apt does not have a stable CLI interface. Use with caution in scripts.\n\n':
                raise Exception(stderr.decode())
        elif stdout != b'':
            print(stdout.decode())


def process_apt_keys(key_data):
    for key_set in key_data:
        if key_set.get('url', False):
            f_path = url_to_local_file_path(key_set['url'])
            process = subprocess.Popen(['sudo', 'apt-key', 'add', f_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, _stderr = process.communicate()
            if stdout == b'OK\n':
                print(f"key added: {key_set['url']}")
            else:
                raise Exception('failed to add key')


def process_bash_scripts(data):
    for key_set in data:
        if key_set.get('url', False):
            f_path = url_to_local_file_path(key_set['url'])

            process = subprocess.Popen(['bash', f_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stderr != b'':
                raise Exception(stderr.decode())
            elif stdout != b'':
                print(stdout.decode())


def process_sources(sources_list):
    for source in sources_list:
        key_name = list(source.keys())[0]
        file_name = key_name + '.list'
        source_content = source[key_name]
        src_file = content_to_temp_path(source_content)
        dst_file = f"/etc/apt/sources.list.d/{file_name}"

        run_command(['sudo', 'cp', src_file, dst_file])


def process_file_block(files_data):
    for file_info in files_data:
        src_file = file_info['src']
        dst_file = file_info['dest']

        if file_info.get('sudo', False):
            run_command(['sudo', 'cp', src_file, dst_file])
        else:
            new_content = open(dst_file).read()
            open(src_file, 'w').write(new_content)


def process_systemd_services(service_block):
    for service_name in service_block.keys():
        for action in service_block[service_name]:
            run_command(['sudo', 'systemctl', action, service_name])


def process_version(version):
    if version != '0.1':
        raise Exception("Unknown version")
