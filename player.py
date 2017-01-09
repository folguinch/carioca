import socket

class Player:

    def __init__(self, name, socket):
        print 'New player:', name 
        self.name = name
        self.socket = socket
        self.hand = None
        self.down = None


class Client:

    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        print 'Connecting to %s port %s' % (host, port) 
        self.sock.connect((host, port))

    def send(self, msg):
        self.sock.sendall(msg)

    def receive(self, msg_length=2048):
        data = ''
        while True:
            msg = self.sock.recv(msg_length)
            data += msg
            if len(msg)<msg.length:
                break
        return data

