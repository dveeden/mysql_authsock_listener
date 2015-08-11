#!/bin/env python3
import os
import socket
import sys
import logging
import json

import oath

def check_auth(**kwargs):
    username = kwargs['username']
    password = kwargs['password']

    logging.info('Checking authentication for {}'.format(username))

    key='123456'

    if username == 'as':
        if oath.accept_totp(key, password)[0] is True:
            return True
    return False


if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)
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
                    logging.info('Request received')
                    jdata = json.loads(data.decode('utf-8'))
                    if check_auth(**jdata):
                        logging.info('Auth result: OK')
                        conn.send(b'OK\n')
                    else:
                        logging.info('Auth result: FAIL')
                        conn.send(b'FAIL\n')
                else:
                    try:
                        conn.send(b'Bye!\n')
                    except BrokenPipeError:
                        pass
                    break
        finally:
            conn.close()
