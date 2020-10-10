import subprocess
import uuid
import re
import requests


def url_to_local_file_path(url):
    r = requests.get(url, allow_redirects=True)
    if not r.ok:
        r.raise_for_status()
    return content_to_temp_path(r.content)


def content_to_temp_path(content):
    key_name = uuid.uuid4()
    local_path = f".automata/{key_name}"
    mode = 'w' if isinstance(content, str) else 'wb'
    open(local_path, mode).write(content)
    return local_path


def run_command(cmd):
    completed_process = subprocess.run(cmd)
    return completed_process


def is_http_url(path):
    return re.match(r"^https?://", path) is not None
