#!/usr/bin/python3 -tt
import os
import socket
import sys
import logging
import json


def check_auth(**kwargs):
    if kwargs['username'] == 'as':
        if kwargs['password'] == 'foobar':
            return True
    return False


if __name__ == "__main__":
    socket_name = '/tmp/authsock.sock'
    
    try:
        os.unlink(socket_name)
    except OSError:
        if os.path.exists(socket_name):
            raise
    
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM);
    
    sock.bind(socket_name)
    sock.listen(1)
    while True:
        conn, client_addr = sock.accept()
        try:
            while True:
                data = conn.recv(100)
                if data:
                    jdata = json.loads(data.decode('utf-8'))
                    if check_auth(**jdata):
                        conn.send(b'OK\n')
                    else:
                        conn.send(b'FAIL\n')
                else:
                    try:
                        conn.send(b'Bye!\n')
                    except BrokenPipeError:
                        pass
                    break
        finally:
            conn.close()
