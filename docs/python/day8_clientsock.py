# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:29:27 2018

@author: KDK
"""

print('################### CLIENT SOCKET 모듈 ###################')
import socket

HOST = '127.0.0.1'
PORT = 50007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(b'Hello, Server')  # 인자가 bytes 배열
data = sock.recv(1024)
sock.close()

print('Received ', data)