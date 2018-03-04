#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_remote.py
# UDP client and server for talking over the network

import argparse, random, socket, sys

MAX_BYTES = 65535


class UDP_Remote(object):
    
    def __init__(self, mode, host, port):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                 
        def server(sock):
            sock.bind((host, port))
            print('Listening at', sock.getsockname())
            while True:
                data, address = sock.recvfrom(MAX_BYTES)
                '''
                if random.random() < 0.5:
                    print('Pretending to drop packet from {}'.format(address))
                    continue
                '''
                text = data.decode('utf-8')
                print('The client at {} says {!r}'.format(address, text))
                message = 'Your data was {} bytes long'.format(len(data))
                sock.sendto(message.encode('utf-8'), address)
                   
        def client(sock):
            sock.connect((host, port))
            print('Client socket name is {}'.format(sock.getsockname()))
            send_data(sock)

        def send_data(sock):
            delay = 0.1  # seconds
            message = input("Type your message\n")
            data = message.encode('utf-8')
            sock.send(data)
            #print('Waiting up to {} seconds for a reply'.format(delay))
            sock.settimeout(delay)
            try:
                data = sock.recv(MAX_BYTES)
            except socket.timeout as exc:
                delay *= 2  # wait even longer for the next request
                if delay > 2.0:
                    raise RuntimeError('I think the server is down') from exc

            print('The server says {!r}\n'.format(data.decode('utf-8')))
            send_data(sock)

        if mode == "server":
            server(sock)
            
        elif mode == "client":
            client(sock)
            
            


def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        '''
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        '''
        text = data.decode('utf-8')
        print('The client at {} says {!r}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('utf-8'), address)

def client(hostname, port, message):
    print("WRONGGGGG ONEEEEEEEEEEEEEEEEE")
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1  # seconds
    #text = 'This is another message'
    data = message.encode('utf-8')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc:
            delay *= 2  # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
        #else:
            #break   # we are done, and can stop looping

    print('The server says {!r}'.format(data.decode('utf-8')))

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    UDP_Remote(args.role, args.host, args.p)
    print("passed remote")
    #function = choices[args.role]
    #function(args.host, args.p)
