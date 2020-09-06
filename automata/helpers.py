import subprocess
import uuid

import requests


def url_to_local_file_path(url):
    r = requests.get(url, allow_redirects=True)
    return content_to_temp_path(r.content)


def content_to_temp_path(content):
    key_name = uuid.uuid4()
    local_path = f".automata/{key_name}"
    mode = 'w' if isinstance(content, str) else 'wb'
    open(local_path, mode).write(content)
    return local_path


def run_command(cmd):
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr != b'':
        raise Exception(stderr.decode())
    elif stdout != b'':
        print(stdout.decode())