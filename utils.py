# utils.py
# утилиты (date, content-type и т.п.)

import os
from urllib.parse import unquote
import time

def http_date():
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())

def safe_path(document_root, url_path):

    decoded_path = unquote(url_path)
    decoded_path = decoded_path.split('?', 1)[0]

    parts = decoded_path.split('/')

    if any(part == '..' for part in parts):
        return None

    decoded_path = decoded_path.lstrip('/')

    # собираем путь
    full_path = os.path.join(document_root, decoded_path)

    # нормализуем путь
    real_path = os.path.realpath(full_path)

    # нормализуем root
    real_root = os.path.realpath(document_root)

    if real_path != real_root and not real_path.startswith(real_root + os.sep):
        return None

    return real_path

def guess_content_type(path):
    ext = os.path.splitext(path)[1].lower()

    return {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.swf': 'application/x-shockwave-flash',
    }.get(ext, 'application/octet-stream')