# http_server/test_http_server/test_request.py
import pytest

from http_server.request import HttpRequest


def test_http_request_parse_ok():
    """
    Проверяет корректный парсинг валидного HTTP-запроса.
    """
    raw = b"GET /index.html HTTP/1.1\r\n\r\n"
    req = HttpRequest(raw)

    assert req.method == "GET"
    assert req.path == "/index.html"
    assert req.version == "HTTP/1.1"


def test_http_request_bad_request():
    """
    Проверяет, что при некорректном HTTP-запросе
    возбуждается исключение ValueError.
    """
    raw = b"BAD_REQUEST\r\n\r\n"

    with pytest.raises(ValueError):
        HttpRequest(raw)
