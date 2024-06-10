from socket import *
import struct

class Client:

    # Массив данных в VR Concept
    send_array = []

    server_address_port = ("127.0.0.1", 6501)

    def __init__(self, server_ip, server_port, array_range):
        self.server_address_port = (server_ip, server_port)
        self.send_array = [0 for i in range(array_range)]

    def send_data(self):
        udp_client_socket = socket(family=AF_INET, type=SOCK_DGRAM)
        # Превращаем числа в массиве в 8 байт каждое
        bts = [struct.pack('d', f) for f in self.send_array]
        # Соединяем все элементы массива в одну длинную байтовую строку и отправляем
        udp_client_socket.sendto(b''.join(bts), self.server_address_port)