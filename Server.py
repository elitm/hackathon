import time
from _thread import start_new_thread
import random
# from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname, SOL_SOCKET, SO_BROADCAST
import socket


# Class Server
class Server:
    def __init__(self, name):
        self.team_name = name

    # Global servers listen port number
    LISTEN_PORT = 13117  # udp
    TCP_PORT = 2026
    DEFAULT_TIMEOUT = 10
    listen = False
    MAX_THREAD_NUMBER = 4  # todo maybe change?

    clients_addresses = []
    clients_team_names = []

    def run_udp_connection(self):
        # Create a UDP socket
        UDP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDP_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        ip_address = socket.gethostbyname(socket.gethostname())

        # message
        magic_cookie = bytes.fromhex('feedbeef')
        message_type = bytes.fromhex('02')
        my_port = bytes.fromhex('2026')
        message = magic_cookie + message_type + my_port

        # Send Broadcast message
        print(f"Server started, listening on IP address {ip_address}")
        #while True:
        UDP_server_socket.sendto(message, ("255.255.255.255", self.LISTEN_PORT))  # todo IP address

        # server_socket.sendto(message, ('172.1.0.255', my_port))
        # TIMER FOR SEC
        print(f"[Server]: waiting for client to respond")  # todo delete
        timer = time.time() + 10
        while (timer - time.time()) > 0:
            self.handle_clients(ip_address, UDP_server_socket)
        if len(self.clients_addresses) == 0:
            print("[Server]: could not find any Clients")
        time.sleep(1)
        self.divide_into_groups(UDP_server_socket)
        UDP_server_socket.close()
        # UDP_server_socket.settimeout(1)

    def handle_clients(self, ip_address, UDP_server_socket):
        try:
            server_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
            server_TCP_socket.bind((ip_address, self.TCP_PORT))

            message_team_name, address_client = server_TCP_socket.recvfrom(1024)

            # TIMER DEFAULT
            try:
                print(f"[Main Server]: Server got a message from: {address_client}")  # , message is: {message}
                team_name = message_team_name[:-1]
                check = message_team_name[-1:]
                if check == '\n':
                    self.clients_addresses.append(address_client)
                    self.clients_team_names.append(team_name)
                    # start_new_thread(self.handle_client, address_client)
                else:
                    print(
                        "[Main Server]: Server got a message but it wasn't legal")  # todo legal way to handle wrong message?
                    # continue

            except Exception as e:
                print(f"Server: Exception: {e}")

        except Exception as e:
            #print(f"Server: problem with TCP socket")
            return

                # continue
            # else:
            # print("[Server]: could not find any Clients")
            # return

        # self.run_udp_connection()
        # UDP_server_socket.settimeout(None)


    def divide_into_groups(self, UDP_server_socket):
        # divide into groups
        names = self.clients_team_names
        random.shuffle(names)
        group1, group2 = [names[x::2] for x in range(2)]
        for group in group1:
            names1 = "" + group + '\n'
        for group in group2:
            names2 = "" + group + '\n'
        for client_address in range(len(self.clients_addresses)):
            message = "Welcome to Keyboard Spamming Battle Royale. \nGroup 1: \n ==\n" + names1 + "\nGroup 2: \n ==\n" + names2 + "Start pressing keys on your keyboard as fast as you can!!"
            print(f"[Client]: sending {client_address}\nmessage: {message}")  # todo delete
            UDP_server_socket.sendto(message, client_address)

        for client_address in range(len(self.clients_addresses)):
            start_new_thread(self.handle_client, client_address)

    def run(self):
        while True:
            self.run_udp_connection()

