# resp.py
# формирование HTTP-ответов

from utils import http_date

def build_response(status_code, reason, body=b'', content_type='text/html', method='GET'):

    body_length = len(body) if method == 'GET' else 0

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
