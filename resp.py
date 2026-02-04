"""
Формирование HTTP-ответов
"""

from utils import http_date


def build_response(
        status_code,
        reason, body=b'',
        content_type='text/html',
        method='GET',
):
    """
   Формирует HTTP-ответ.

   :param status_code: HTTP status code (200, 404, 403 и т.д.)
   :param reason: текстовое описание статуса
   :param body: тело ответа (bytes)
   :param content_type: MIME-тип содержимого
   :param method: HTTP-метод (GET или HEAD)
   :return: bytes HTTP-ответ
    """
    body_length = len(body)

    headers = [
        f'HTTP/1.1 {status_code} {reason}',
        f'Date: {http_date()}',
        'Server: SimplePythonServer',
        f'Content-Length: {body_length}',
        f'Content-Type: {content_type}',
        'Connection: close',
        '',
        ''
    ]
    response = '\r\n'.join(headers).encode('utf-8')

    if method == 'GET' and body:
        response += body

    return response
