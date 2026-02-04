"""
Вспомогательные утилиты для HTTP-сервера.

Содержит функции:
- формирования HTTP-даты
- безопасного преобразования URL в путь файловой системы
- определения Content-Type по расширению файла
"""

import os
from urllib.parse import unquote
import time

def http_date():
    """
    Возвращает текущую дату и время в формате HTTP.

    Формат соответствует RFC 7231 и используется
    в заголовке Date HTTP-ответа.

    :return: Строка с датой в формате GMT
    """
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())

def safe_path(document_root, url_path):
    """
    Преобразует URL-путь в безопасный путь файловой системы.

    Функция:
    - декодирует URL (%XX)
    - отбрасывает query string
    - запрещает выход за пределы DOCUMENT_ROOT
    - блокирует использование ".." в пути

    Если путь небезопасен — возвращает None.

    :param document_root: Корневая директория сервера
    :param url_path: путь из HTTP-запроса
    :return: абсолютный безопасный путь или None
    """

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
    """
    Определяет MIME-тип файла по его расширению.
    Используется для формирования заголовка Content-Type.

    :param path: Путь к файлу
    :return: MIME-тип в виде строки
    """

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
