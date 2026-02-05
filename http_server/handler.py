# http_server/handler.py

"""
HTTP request handler.

Модуль содержит класс `HttpHandler`, отвечающий за обработку
HTTP-запросов уровня приложения.

Зона ответственности:
- проверка поддерживаемых HTTP-методов
- безопасное разрешение пути внутри DOCUMENT_ROOT
- работа с файловой системой (файлы, директории, index.html)
- формирование корректных HTTP-ответов

Модуль НЕ работает с сокетами и не занимается сетевым вводом/выводом.
"""


import os
from resp import build_response
from utils import safe_path, guess_content_type

DOCUMENT_ROOT = './www'

# pylint: disable=too-few-public-methods
class HttpHandler:
    """
    Обработчик HTTP-запросов.

    Класс инкапсулирует логику обработки одного HTTP-запроса
    и формирования соответствующего HTTP-ответа.
    """

    def handle(self, request):
        """
        Обрабатывает HTTP-запрос и возвращает HTTP-ответ.

        Метод:
        - проверяет поддерживаемость HTTP-метода
        - определяет безопасный путь к ресурсу
        - обрабатывает запросы к файлам и директориям
        - возвращает корректный HTTP-ответ в виде bytes

        :param request: объект HttpRequest с распарсенным запросом
        :return: HTTP-ответ (bytes)
        """

        if request.method not in ('GET', 'HEAD'):
            return build_response(
                405,
                'Method Not Allowed',
                method=request.method,
            )

        file_path = safe_path(DOCUMENT_ROOT, request.path)

        if file_path is None:
            return build_response(403, 'Forbidden', method=request.method)

        if request.path.endswith('/') and os.path.isfile(file_path):
            return build_response(404, 'Not Found', method=request.method)

        if os.path.isdir(file_path):
            return self._handle_directory(file_path, request)

        if os.path.isfile(file_path):
            return self._handle_file(file_path, request)

        return build_response(404, 'Not Found', method=request.method)

    def _handle_directory(self, path, request):
        """
        Обрабатывает запрос к директории.

        Если в директории присутствует файл index.html —
        возвращает его содержимое.

        В противном случае возвращает ответ 404 Not Found.

        :param path: Абсолютный путь к директории
        :param request: объект HttpRequest
        :return: HTTP-ответ (bytes)
        """
        index_path = os.path.join(path, 'index.html')

        if not os.path.isfile(index_path):
            return build_response(404, 'Not Found', method=request.method)

        return self._build_file_response(index_path, request)

    def _handle_file(self, path, request):
        """
        Обрабатывает запрос к файлу.

        Формирует HTTP-ответ с содержимым файла и корректным
        Content-Type.

        :param path: Абсолютный путь к файлу
        :param request: объект HttpRequest
        :return: HTTP-ответ (bytes)
        """
        return self._build_file_response(path, request)

    def _build_file_response(self, path, request):
        """
        Формирует HTTP-ответ для файла.

        Метод:
        - считывает содержимое файла
        - определяет MIME-тип
        - формирует HTTP-ответ с кодом 200 OK

        :param path: Абсолютный путь к файлу
        :param request: объект HttpRequest
        :return: HTTP-ответ (bytes)
        """
        with open(path, 'rb') as f:
            body = f.read()

        content_type = guess_content_type(path)

        return build_response(
            200,
            'OK',
            body=body,
            content_type=content_type,
            method=request.method,
        )
