"""
Author: Rugh1
Date: 26.01.2024
Description: wrote proper way of getting information
"""
import socket

def recv(socket):
    msg = ''
    while '\r\n\r\n' not in msg:
        data = socket.recv(1).decode()
        if data == '':
            msg = ''
            break
        msg += data
    return msg


def recv_body(socket, leng):
    print('1')
    msg = b''
    print('2')
    while len(msg) < leng:
        print('4')
        data = socket.recv(leng - len(msg))
        if data == b'':
            msg = b''
            break
        msg += data
    print('3')
    return msg 
    