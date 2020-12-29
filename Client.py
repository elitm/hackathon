import time
from Utils import *
from socket import *


# Class Client
class Client:

    RECEIVED_PORT = 13117 #UDP
    SEND_PORT = 2026 #TCP
    DEFAULT_TIMEOUT = 10

    def __init__(self, name):
        self.team_name = name

    def run(self):
        UDP_client_socket = socket(AF_INET, SOCK_DGRAM) # todo works tcp
        UDP_client_socket.bind(('', Client.LISTEN_PORT))
        print(f"[Main Client]: Created main socket binded to port: {Client.listen_port}")

        while True:  # todo something else instead of TRUE
            # Wait for BROADCAST
            print("[Client]: Client waiting for an offer message")
            message, address_broadcaster = UDP_client_socket.recvfrom(1024) # todo check if legal port

            # TIMER DEFAULT
            try:
                print(f"[Main Server]: Server got a message from: {address_broadcaster}")  # , message is: {message}
                magic_cookie, message_type, dest_port = split_message(message)
                is_legal = check_legal_offer(magic_cookie, message_type, dest_port)

                ip_address = sock.gethostbyname(sock.gethostname())

                TCP_Client_socket = socket(AF_INET, SOCK_STREAM)
                TCP_Client_socket.bind((ip_address, Client.SEND_PORT))

                if is_legal:
                    message = self.team_name + '\n'
                    TCP_Client_socket.sendto(message, address_broadcaster) #tcp socket

                else:
                    print("[Client]: Client got a message but it wasn't a BROADCAST")
                    continue

            except Exception as e:
                print(f"Client: Exception: {e}")
                client_socket.close()

