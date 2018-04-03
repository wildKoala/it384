import argparse
import socket
import time

def random_msg():
    """ Creates an alpha-numeric string of between 1 and 3000 characters in length.  
    Python 3 strings are unicode (2-bytes per char),so we will change the encoding 
    to ascii to reduce the size of the message in transit, as a result the message 
    size will the same as the length (1 to 3000 bytes)
    """
    import random, string
    size = random.randint(1,3000)
    #The double carriage return line feed sequence is typically used to denote the end of an application layer protocol header
    messageHeader = "Length: " + str(size + 12) + "\r\n\r\n" 
    messageBody = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(size)])
    message = messageHeader + messageBody
    return message.encode('ascii')

class tcp_prog():
    def __init__(self):
        self.argparse()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.args.role == 'server':
            self.server()
        else:
            self.client()
    
    def recvall(self,sock):
        data = sock.recv(32)
        #print(data)
        length = int(data.split()[1])
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting {} bytes but only received'
                               ' {} bytes before the socket closed'
                               .format(length, len(data)))
            data += more
        return data

    def server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.args.ip, self.args.port))
        self.sock.listen(1)
        print('Listening at', self.sock.getsockname())
        while True:
            print('Waiting to accept a new connection')
            sc, sockname = self.sock.accept()
            print('We have accepted a connection from', sockname)
            print('  Socket name:', sc.getsockname())
            print('  Socket peer:', sc.getpeername())

            sc.sendall("The server is making a move...".encode())
            #message = self.recvall(sc)
            #print("client says:", message.decode())
            #sc.sendall(message)
            time.sleep(.5) # so the client has time to receive before closing the socket.
            sc.close()
            print('  Reply sent, socket closed')
    
    def client(self):
        self.sock.connect((self.args.ip, self.args.port))
        print('Client has been assigned socket name', self.sock.getsockname())
        #self.sock.sendall(random_msg())
        reply = self.recvall(self.sock)
        print('The server said:', reply.decode('utf-8'))
        self.sock.close()


    def argparse(self):
        choices = ['client', 'server']
        parser = argparse.ArgumentParser(description='Send and receive over TCP')
        parser.add_argument('role', choices=choices, help='which role to play')
        parser.add_argument('ip', help='interface the server listens at;'
                            ' host the client sends to')
        parser.add_argument('-p', "--port", type=int, default=1060,
                            help='TCP port (default 1060)')
        self.args = parser.parse_args()

if __name__ == '__main__':
    tcp_instance = tcp_prog()
