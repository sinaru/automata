from automata.helpers import url_to_local_file_path, content_to_temp_path, run_command, is_http_url


# todo maybe use apt package
def process_apt_packages(packages_data):
    run_command(['sudo', 'apt', 'update'])

    for pkg_name in packages_data:
        run_command(['sudo', 'apt', 'install', pkg_name])


def process_apt_keys(data):
    for item in data:
        if is_http_url(item):
            f_path = url_to_local_file_path(item)
        else:
            f_path = item
        run_command(['sudo', 'apt-key', 'add', f_path])
        print(f"key added: {item}")


def process_bash_scripts(data):
    for key in data:
        if is_http_url(key):
            f_path = url_to_local_file_path(key)
            run_command(['bash', f_path])
        else:
            run_command(['bash', key])


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
        action = service_block[service_name]
        run_command(['sudo', 'systemctl', action, service_name])


def process_version(version):
    if version != '0.1':
        raise Exception("Unknown version")


def process_git(data):
    for block in data:
        if block.get('clone', False):
            cmd = ['git', 'clone', (block['clone'])]
            if block.get('dest', ''):
                cmd.append(block['dest'])
            run_command(cmd)
