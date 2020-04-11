import socket
import collections

class socket_poler:
    def __init__(self, mouse_buffer_size=2, host="", port=10000):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen()
            

        self.mouse_buffer = collections.deque(maxlen=mouse_buffer_size)
        self.important_list = []


        self.port = port
        self.host = host

    def pol(self):
        while True:
            conn, addr = self.socket.accept()
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                orders = data.split(",")[:-1]

                down = False

                for order in orders:
                    if order[0] != 'm' or down:
                        if order == "a d":
                            down = True
                        self.important_list.append(order)
                    else:
                        self.mouse_buffer.append(order)
                
                print(self.orders())
                

    def orders(self):
        res = self.important_list + list(self.mouse_buffer)
        self.important_list = []
        self.mouse_buffer.clear()

        return res


    def connection(self):
        return "{}/{}/".format(socket.gethostbyname(socket.gethostname()), self.port)


