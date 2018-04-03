# I want to continue receiving 16 bytes until the message is complete. I know how much data I'm getting now because I have parsed it.
# 


import socket, argparse
from ipaddress import *

# tic tac toe logic

# A server is started, using outward facing ip address, and then a port -1060 by default
# the server hosting the game also plays the game.

# A client is instantiated. Connects to the server. Game begins when the client connects

# Server goes first, selects position. Server will be X

# LOOP ======================================================================

# sends string out to client

# client recieves string

# print screen

# client checks for win

    #if win:
        # send "X has won!"
        # close connection
    #else:
        # client makes choice
        # if choice has already been chosen, force to make another choice.
        # client sends back string, which is the number they chose -1.

# server recieves string

# print screen

# server checks for win

    #if win:
        # send "O has won!"
        # close connection
    #else:
        # check for tie
        # server makes choice
        # server sends back string, which is the number they chose -1.

# END LOOP ======================================================================

def intro():
    
    print(" 7 | 8 | 9 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 1 | 2 | 3 ")

    print("use the number pad to place your X's and O's in the corresponding squares.")

def is_valid(input_val):
    if input_val in map(str, range(1,10)):
        return True
        
    
def is_legal(board, mark_location):
    """
    This function takes the string of characters representing the board and the mark location the user
    wants to go as input and returns True if space is on the board and open. Otherwise, it returns False
    """    
    if board[mark_location-1] != " ":
        return False
    return True

def game_tied(board):
    for ltr in board:
        if ltr == " ":
            return False
    return True

def print_board(board):
    """
    This function takes the 2d array representing the board as input and prints a 
    formatted board to the screen.
    """
    print(" {} | {} | {} ".format(board[6], board[7], board[8]))
    print("---+---+---")
    print(" {} | {} | {} ".format(board[3], board[4], board[5]))
    print("---+---+---")
    print(" {} | {} | {} ".format(board[0], board[1], board[2]))

def place_mark(board_string, mark, number):
    if number == 9:
        new_string = board_string[:8] + mark
    else:
        new_string = board_string[:number-1] + mark + board_string[number:]
    return new_string

def game_won(board):
    """
    This function takes the array of characters representing the board as input
    and returns True if 3 spaces in a row match.  Otherwise, it returns False
    """
    linesToCheck = [[0,1,2],
                    [3,4,5],
                    [6,7,8],
                    [0,3,6],
                    [1,4,7],
                    [2,5,8],
                    [0,4,8],
                    [2,4,6]]
                    
    for line in linesToCheck:
        if board[line[0]] == board[line[1]] == board[line[2]]:
            if board[line[0]] != " " and board[line[1]] != " " and board[line[2]] != " ":
                print(board[line[0]], "has won!")
                return True
    return False

'''
def server_turn(board): # probably just delete this.
    
    server_mark = "X"
    
    try:
        number = int(input("Please enter the number of the square you want to place your mark in. "))
    except ValueError:
        print("You must enter a number")
        #server_turn(board)
        return "INVALID"
    
    if game_won(board):
        print("GAME OVER, O wins!")
        #return game over string. normally would return len(9) string
    if game_tied(board):
        print("GAME OVER, it was a tie!")
    
    if is_legal(board, number):
        return place_mark(board, server_mark, number) # am i allowed to return a function call like this?
    else:
        print("Invalid number")
        server_turn(board)
                    [0,3,6],
                    [1,4,7],
                    [2,5,8],
                    [0,4,8],
                    [2,4,6]]
                    
    for line in linesToCheck:
        if board[line[0]] == board[line[1]] == board[line[2]]:
            if board[line[0]] != " " and board[line[1]] != " " and board[line[2]] != " ":
                print(board[line[0]], "has won!")
                return True
    return False
'''         

class tic_tac_toe(object):
   

    def server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.args.ip, self.args.port))
        self.sock.listen(1)
        print('Listening at', self.sock.getsockname())
        while True:
        server_mark = "X"
        board = "         "
        
        print('Listening at', self.sock.getsockname())
        
        intro()

        # where do I accept a connection?
        
        while not game_won(board):
            
            if game_tied(board):
                print("It was a tie!")
                break

            square_chosen = input(server_mark + " to play: ")
            if is_valid(square_chosen):
                square_chosen = int(square_chosen)
            else:
                print("You must enter a digit 1-9")
                continue
            
            if is_legal(board, square_chosen):
                board = place_mark(board, server_mark, square_chosen)
                print_board(board)
                #want to send to client here
            
        '''
        while True:
            sc, sockname = sock.accept()
            print('Processing up to 8 bytes at a time from', sockname)
            n = 0
            while True:
                data = sc.recv(8)
                output = data.decode('ascii')

                if not data:
                    break
                output = data.decode('ascii')
                sc.sendall(output.encode())  # sending it back
                n += len(data)
                print('\r  %d bytes processed so far' % (n,), end=' ')
                sys.stdout.flush()
            print()
            sc.close()
            print('  Socket closed')
        '''
        
    def client(self):
        self.sock.connect((self.args.ip, self.args.port))
        print('Client has been assigned socket name', self.sock.getsockname())
        #self.sock.sendall(random_msg())
        msg_from_server = self.recvall(self.sock)
        print(msg_from_server.decode('utf-8'))
        #self.sock.close()
        intro()

        bytecount = (bytecount + 15) // 16 * 16  # round up to a multiple of 16
        
        while not game_won(board): # is the while loop correct?
            
            if game_tied(board):
                print("It was a tie!")
                break

            square_chosen = input(client_mark + " to play: ")
            if is_valid(square_chosen):
                square_chosen = int(square_chosen)
            else:
                print("You must enter a digit 1-9")
                continue
            
            if is_legal(board, square_chosen):
                board = place_mark(board, client_mark, square_chosen)
                #want to send to server here
                
        print('Sending', bytecount, 'bytes of data, in chunks of 16 bytes')
        #sock.connect((host, port))

        sent = 0
        received = 0
        while received < bytecount:
            sock.sendall(message)
            sent += len(message)
            print('\r  %d bytes sent' % (sent,), end=' ')
            if sent == bytecount:
                print()
                sock.shutdown(socket.SHUT_WR)            
     

            data = sock.recv(42)
            if not received:
                print('  The first data received says', repr(data))
            if not data:
                break
            received += len(data)
            print('\r  %d bytes received' % (received,), end=' ')

            sys.stdout.flush()

            
    def argparse(self):
        choices = ['client', 'server']
        parser = argparse.ArgumentParser(description='Play tic-tac-toe with a friend across the net.')
        parser.add_argument('role', choices=choices, help='which role to play')
        parser.add_argument('ip', help='interface the server listens at;'
                            ' host the client sends to')
        parser.add_argument('-p', "--port", type=int, default=1060,
                            help='TCP port (default 1060)')
        self.args = parser.parse_args()
        
        
    def __init__(self, role, interface, port):
        self.argparse()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.args.role == 'server':
            self.server()
        else:
            self.client()


if __name__ == '__main__':
    roles = ('client', 'server')
    parser = argparse.ArgumentParser(description='Play a rousing game of tic-tac-toe.')
    parser.add_argument('role', choices=roles, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    
    if args.role == 'client':
        tic_tac_toe('client', args.host, args.p) 
    else:
        tic_tac_toe('server', args.host, args.p)

        #main()














