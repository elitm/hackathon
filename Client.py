import time
from Utils import *
from socket import *


# Class Client
class Client:

    RECEIVED_PORT = 13117
    DEFAULT_TIMEOUT = 10

    def __init__(self, name):
        self.team_name = name

    def run(self):
        client_socket = socket(AF_INET, SOCK_STREAM) # todo works tcp
        client_socket.bind(('', Client.LISTEN_PORT))
        print(f"[Main Client]: Created main socket binded to port: {Client.listen_port}")

        while True:  # todo something else instead of TRUE
            # Wait for BROADCAST
            print("[Client]: Client waiting for an offer message")
            message, address_broadcaster = client_socket.recvfrom(self.RECEIVED_PORT) # todo check if legal port

            # TIMER DEFAULT
            try:
                print(f"[Main Server]: Server got a message from: {address_broadcaster}")  # , message is: {message}
                magic_cookie, message_type, dest_port = split_message(message)
                is_legal = check_legal_offer(magic_cookie, message_type, dest_port)

                if is_legal:
                    message = self.team_name + '\n'
                    client_socket.sendto(message, address_broadcaster)

                else:
                    print("[Client]: Client got a message but it wasn't a BROADCAST")
                    continue

            except Exception as e:
                print(f"Client: Exception: {e}")
                client_socket.close()

