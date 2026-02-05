# http_server/request.py
"""
Парсинг HTTP-запроса
"""


# pylint: disable=too-few-public-methods
class HttpRequest:
    """
    Представление HTTP-запроса.

    Класс инкапсулирует данные HTTP-запроса, полученные
    из стартовой строки протокола.
    """

    def __init__(self, raw: bytes):
        self.method = None
        self.path = None
        self.version = None
        self._parse(raw)

    def _parse(self, raw: bytes):
        """
        Парсит стартовую строку HTTP-запроса.

        Ожидаемый формат:
        <METHOD> <PATH> <HTTP_VERSION>

        В случае ошибки парсинга возбуждается исключение ValueError.

        :param raw: Сырые данные HTTP-запроса (bytes)
        :raises ValueError: если стартовая строка некорректна
        """

        try:
            line = raw.split(b'\r\n', 1)[0].decode('utf-8')
            self.method, self.path, self.version = line.split()
        except Exception as exc:
            raise ValueError("Bad HTTP request") from exc
