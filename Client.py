import time
#from Utils import *
import socket


# Class Client
class Client:

    RECEIVED_PORT = 13117 #UDP
    SEND_PORT = 2026 #TCP
    DEFAULT_TIMEOUT = 10

    def __init__(self, name):
        self.team_name = name

    def run(self):
        UDP_Client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_Client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDP_Client_socket.bind(('', Client.RECEIVED_PORT))
        print(f"[Main Client]: Created main socket binded to port: {Client.RECEIVED_PORT}")

        while True:  # todo something else instead of TRUE
            # Wait for BROADCAST
            print("[Client]: Client started, listening for offer requests...")
            message, address_broadcaster = UDP_Client_socket.recvfrom(1024)

            # TIMER DEFAULT
            try:
                print(f"[Main Server]: Server got a message from: {address_broadcaster}")  # , message is: {message}
                magic_cookie, message_type, dest_port = self.split_message(message)
                is_legal = self.check_legal_offer(magic_cookie, message_type, dest_port)

                ip_address = socket.gethostbyname(socket.gethostname())

                TCP_Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                TCP_Client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                TCP_Client_socket.bind((ip_address, Client.SEND_PORT))

                if is_legal:
                    message = self.team_name + '\n'
                    TCP_Client_socket.sendto(message, address_broadcaster) #tcp socket

                else:
                    print("[Client]: Client got a message but it wasn't a BROADCAST")
                    continue

            except Exception as e:
                print(f"Client: Exception: {e}")
                TCP_Client_socket.close()




    def split_message(self,m):
        message1 = m.hex()
        magic_cookie = message1[:8]
        message_type = message1[8:10]
        dest_port = message1[10:]
        return magic_cookie, message_type, dest_port


    def check_legal_offer(self, magic_cookie, message_type, dest_port):
        flag1 = True
        flag2 = True
        flag3 = True
        if not magic_cookie == 'feedbeef':
            flag1 = False
        if not message_type == '02':
            flag2 = False
        if not dest_port == '2026': #todo change
            flag3 = False
        return flag1 and flag2 and flag3
