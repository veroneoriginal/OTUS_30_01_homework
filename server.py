# server.py
"""
TCP HTTP server.

Отвечает за создание серверного сокета,
приём входящих соединений и запуск обработчиков
в отдельных потоках (thread-per-connection).
"""


import socket
import threading
from http_server.connection import handle_request

HOST = 'localhost'
PORT = 8080

def start_server():
    """
    Запускает TCP-сервер и принимает входящие соединения.
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f'Server started on {HOST}:{PORT}')

    try:
        while True:
            client_socket, _ = server_socket.accept()
            thread = threading.Thread(
                target=handle_request,
                args=(client_socket,),
                daemon=True,
            )
            thread.start()
    except KeyboardInterrupt:
        print('\nServer shutting down...')

    finally:
        server_socket.close()
