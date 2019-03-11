import socket


class c_socket(socket.socket):
    def recvall(self, BUFF_SIZE=2048):
        data = b''
        while True:
            part = self.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data
