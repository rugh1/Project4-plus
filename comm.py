"""
Author: Rugh1
Date: 26.01.2024
Description: wrote proper way of getting information
"""
import socket

def recv(connected_socket):
    """
    Receives an HTTP message until it encounters the end of headers (CRLF CRLF).

    :param connected_socket: The socket to receive data from.
    :type connected_socket: socket.socket

    :return: The received HTTP message.
    :rtype: str
    """
    msg = ''
    while '\r\n\r\n' not in msg:
        data = connected_socket.recv(1).decode()
        if data == '':
            msg = ''
            break
        msg += data
    return msg


def recv_body(connected_socket, leng):
    """
    Receives the body of an HTTP message.

    :param connected_socket: The socket to receive data from.
    :type connected_socket: socket.socket

    :param leng: The expected length of the body.
    :type leng: int

    :return: The received body of the HTTP message.
    :rtype: bytes
    """
    print('1')
    msg = b''
    print('2')
    while len(msg) < leng:
        print('4')
        data = connected_socket.recv(leng - len(msg))
        if data == b'':
            msg = b''
            break
        msg += data
    print('3')
    return msg 
    