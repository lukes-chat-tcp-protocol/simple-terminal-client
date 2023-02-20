import socket
import ssl

class SocketCommunication:
    def __init__(self, args):
        if args.insecure:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            self.sock = self.ssl_context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.port = args.port
        self.connect_address = args.connect_address
    def connect(self):
        self.sock.connect((self.connect_address, self.port))
