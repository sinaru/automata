from automata.handlers import process_apt_packages, process_apt_keys, process_sources, process_file_block, \
    process_systemd_services

key_function = {
    'apt_packages': 'process_apt_packages',
    'apt_keys': 'process_apt_keys',
    'sources': 'process_sources',
    'files': 'process_file_block',
    'systemd.services': 'process_systemd_services'
}


def process_entry(section_name, data):
    function = key_function.get(section_name, False)

    if not function:
        raise Exception(f"Invalid type {section_name}")

    globals()[function](data)
