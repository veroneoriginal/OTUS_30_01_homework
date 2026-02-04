# server.py
# сокеты, accept, threading

import socket
import threading
from handler import handle_request

HOST = 'localhost'
PORT = 8080

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f'Server started on {HOST}:{PORT}')

    try:
        while True:
            client_socket, _ = server_socket.accept()
            thread = threading.Thread(
                target=handle_request,
                args=(client_socket,),
                daemon=True
            )
            thread.start()
    finally:
        server_socket.close()
