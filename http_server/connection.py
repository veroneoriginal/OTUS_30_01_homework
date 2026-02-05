# http_server/connection.py
"""
Модуль содержит функцию обработки одного клиентского соединения
на уровне HTTP-протокола.
"""


from http_server.request import HttpRequest
from http_server.handler import HttpHandler
from resp import build_response


def handle_request(client_socket):
    """
    Обрабатывает одно клиентское соединение.

    Функция:
    - читает HTTP-запрос из сокета
    - парсит запрос и обрабатывает ошибки формата
    - делегирует обработку HTTP-логики объекту HttpHandler
    - отправляет HTTP-ответ клиенту
    - закрывает сокет по завершении обработки

    :param client_socket: сокет, подключённый к клиенту
    """
    try:
        data = client_socket.recv(4096)
        if not data:
            return

        try:
            request = HttpRequest(data)
        except ValueError:
            response = build_response(400, 'Bad Request')
            client_socket.sendall(response)
            return

        handler = HttpHandler()
        response = handler.handle(request)
        client_socket.sendall(response)

    finally:
        client_socket.close()
