# import time
#
# from requests import request
#
#
#
# def send_requests():
#     result = request(method="GET", url="http://localhost:8080/")
#     print(result)
#
# for i in range(1000):
#     time.sleep(0.3)
#     send_requests()


import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8080))

s.sendall(b'HELLO SERVER\n')
print(s.recv(1024))

s.close()