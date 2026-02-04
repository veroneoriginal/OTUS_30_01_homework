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

        # плохой HTTP-запрос
        try:
            method, path, _ = request_line.split()
        except ValueError:
            response = build_response(400, 'Bad Request')
            client_socket.sendall(response)
            return

        # поддерживаем только GET и HEAD
        if method not in ('GET', 'HEAD'):
            response = build_response(
                405,
                'Method Not Allowed',
                method=method,
            )
            client_socket.sendall(response)
            return

        # безопасный путь
        file_path = safe_path(DOCUMENT_ROOT, path)

        if file_path is None:
            response = build_response(
                403,
                'Forbidden',
                method=method,
            )
            client_socket.sendall(response)
            return

        # файл + "/" → 404
        if path.endswith('/') and os.path.isfile(file_path):
            response = build_response(
                404,
                'Not Found',
                method=method,
            )
            client_socket.sendall(response)
            return

        # директория → ищем index.html
        if os.path.isdir(file_path):
            index_path = os.path.join(file_path, 'index.html')

            if os.path.isfile(index_path):
                with open(index_path, 'rb') as f:
                    body = f.read()

                content_type = guess_content_type(index_path)

                response = build_response(
                    200,
                    'OK',
                    body=body,
                    content_type=content_type,
                    method=method,
                )
                client_socket.sendall(response)
                return
            else:
                response = build_response(
                    404,
                    'Not Found',
                    method=method,
                )
                client_socket.sendall(response)
                return

        # обычный файл
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                body = f.read()

            content_type = guess_content_type(file_path)

            response = build_response(
                200,
                'OK',
                body=body,
                content_type=content_type,
                method=method,
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
