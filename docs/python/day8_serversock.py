# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:29:11 2018

@author: KDK
"""

print('################### SERVER SOCKET 모듈 ###################')
import socket

HOST = '' # 
PORT = 50007
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))     # 주의: 인자가 튜플 
sock.listen(1)              # 접속이 있을 때까지 대기
con, addr = sock.accept()   # 접속을 수락
print('connected by ', addr)

while True:
    data = con.recv(1024)
    if not data:
        break
    con.send(data)          # 받은 데이터를 클라이언트에 전송
    
con.close()