"""
Тестирование с использованием моков
"""
from http_server.handler import HttpHandler


class DummyRequest:
    """
    Заглушка HTTP-запроса для тестирования HttpHandler.

    Используется вместо реального HttpRequest,
    содержит только необходимые поля.
    """
    def __init__(self, method, path):
        self.method = method
        self.path = path


def test_method_not_allowed():
    """
    Проверяет, что неподдерживаемый HTTP-метод
    приводит к ответу 405 Method Not Allowed.
    """
    handler = HttpHandler()
    req = DummyRequest("POST", "/")

    response = handler.handle(req)

    assert b"405 Method Not Allowed" in response


def test_not_found():
    """
    Проверяет, что запрос к несуществующему ресурсу
    приводит к ответу 404 Not Found.
    """
    handler = HttpHandler()
    req = DummyRequest("GET", "/hope")

    response = handler.handle(req)

    assert b"404 Not Found" in response
