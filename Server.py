import struct
import time
from _thread import start_new_thread
import random
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname, SOL_SOCKET, SO_BROADCAST
import socket as sock


# Class Server
class Server:
    # Global servers listen port number
    LISTEN_PORT = 13117  # udp
    TCP_PORT = 2026
    DEFAULT_TIMEOUT = 10
    listen = False
    MAX_THREAD_NUMBER = 4  # todo maybe change?

    def __init__(self, name):
        self.team_name = name

    def run(self):

        """
        run function running the server, mean server able to receive BROADCAST messages,
        for each one a thread will open.
        The server will stay open until static variable 'listen' is 'False'
        todo delete the comment

        :return: None.
        """
        # Create a UDP socket
        UDP_server_socket = socket(AF_INET, SOCK_DGRAM)
        UDP_server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        clients_addresses = []
        clients_team_names = []
        ip_address = sock.gethostbyname(sock.gethostname())

        # Send Broadcast message
        print(f"Server started, listening on IP address {ip_address}")

        magic_cookie = bytes.fromhex('feedbeef')
        message_type = bytes.fromhex('02')
        my_port = bytes.fromhex('2026')
        message = magic_cookie + message_type + my_port  # todo maybe utf-8

        UDP_server_socket.sendto(message, ("255.255.255.255", self.LISTEN_PORT))  # todo IP address
        # server_socket.sendto(message, ('172.1.0.255', my_port))

        # TIMER FOR SEC
        print(f"[Server]: waiting for client to respond")  # todo delete

        UDP_server_socket.settimeout(1)

        server_TCP_socket = socket(AF_INET, sock.SOCK_STREAM)  # tcp
        server_TCP_socket.bind((ip_address, self.TCP_PORT))

        timer = time.time() + 100000000
        while (timer - time.time()) > 0:
            try:
                print("[Main Server]: Server waiting for message")
                message, address_client = TCP_server_socket.recvfrom(self.TCP_PORT)  # todo tcp socket

                # TIMER DEFAULT
                try:
                    print(f"[Main Server]: Server got a message from: {address_client}")  # , message is: {message}
                    team_name = message[:-1]
                    check = message[-1:]
                    if check == '\n':
                        clients_addresses.append(address_client)
                        clients_team_names.append(team_name)
                        # start_new_thread(self.handle_client, address_client)
                    else:
                        print(
                            "[Main Server]: Server got a message but it wasn't legal")  # todo legal way to handle wrong message?
                        continue

                except Exception as e:
                    print(f"Server: Exception: {e}")

            except Exception as e:
                if len(clients_addresses) != 0:
                    continue
                else:
                    print("[Server]: could not find any Clients")
                    return
        UDP_server_socket.settimeout(None)

        # divide into groups
        # clients_team_names = ['a', 'b', 'c', 'd']
        names = clients_team_names
        random.shuffle(names)
        group1, group2 = [names[x::2] for x in range(2)]
        for group in group1:
            names1 = "" + group + '\n'
        for group in group2:
            names2 = "" + group + '\n'
        for client_address in range(len(clients_addresses)):
            message = "Welcome to Keyboard Spamming Battle Royale. \nGroup 1: \n ==\n" + names1 + "\nGroup 2: \n ==\n" + names2 + "Start pressing keys on your keyboard as fast as you can!!"
            print(f"[Client]: sending {client_address}\nmessage: {message}")  # todo delete
            server_socket.sendto(message, client_address)

        for client_address in range(len(clients_addresses)):
            start_new_thread(self.handle_client, client_address)

        #     # Send data
        # print(f"[Client]: waiting for servers answer's")
        # client_socket.settimeout(Client.DEFAULT_TIMEOUT)

