# handler.py
# обработка одного HTTP-запроса

import os
from resp import build_response
from utils import safe_path, guess_content_type

DOCUMENT_ROOT = './www'


def handle_request(client_socket):
    try:
        data = client_socket.recv(4096)
        if not data:
            return

        request_line = data.split(b'\r\n', 1)[0].decode('utf-8')
        method, path, _ = request_line.split()

        if method not in ('GET', 'HEAD'):
            response = build_response(
                405,
                'Method Not Allowed',
                method=method,
            )
            client_socket.sendall(response)
            return

        # Получаем безопасный путь
        file_path = safe_path(DOCUMENT_ROOT, path)

        if file_path is None:
            response = build_response(
                403,
                'Forbidden',
                method=method,
            )
            client_socket.sendall(response)
            return

        # Если это директория — ищем index.html
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, 'index.html')

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                body = f.read()

            content_type = guess_content_type(file_path)

            response = build_response(
                200,
                'OK',
                body=body,
                content_type=content_type,
                method=method
            )
        else:
            response = build_response(
                404,
                'Not Found',
                method=method,
            )

        client_socket.sendall(response)

    finally:
        client_socket.close()
