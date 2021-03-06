import socket
import queue
import options

class socket_poler:
    def __init__(self, options, buffer_size=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((options.host, options.port))
        self.socket.listen()

        self.buffer = queue.Queue()

        self.options = options


    def pol(self):
        while True:
            conn, addr = self.socket.accept()
            print("connected with {}".format(addr))
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                orders = data.split(u"\u0003")[:-1]
                
                for order in orders:
                    self.buffer.put(order)

    def orders(self):
        return self.buffer

    def connection(self):
        return "{}/{}/".format(socket.gethostbyname(socket.gethostname()), self.options.port)


