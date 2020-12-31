import time
import random
import socket
import threading

class Server:
    def __init__(self, name):
        self.team_name = name
        self.LISTEN_PORT = 13117  # udp
        self.TCP_PORT = 2026
        self.DEFAULT_TIMEOUT = 10
        self.clients_addresses = []
        self.clients_team_names = []
        self.server_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
        self.server_TCP_socket.bind(("", self.TCP_PORT))
        self.UDP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.UDP_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def run_udp_connection(self):
        # Create a UDP socket
        threading.Timer(1.0, self.run_udp_connection).start()
        # get the server ip
        # message
        magic_cookie = bytes.fromhex('feedbeef')
        message_type = bytes.fromhex('02')
        my_port = bytes.fromhex('2026')
        message = magic_cookie + message_type + my_port
        # Send Broadcast message
        self.UDP_server_socket.sendto(message, ("255.255.255.255", self.LISTEN_PORT))
        # print(f"[Server]: waiting for client to respond")  # todo delete

    def run_tcp_connection(self):
        try:
            timer = time.time() + 10
            while (timer - time.time()) > 0:
                self.server_TCP_socket.listen(4)
                print("{Server}: waiting for message")
                message_team_name, address_client = self.server_TCP_socket.accept()
                team_name_before = message_team_name.recv(1024).decode("utf-8")
                print(f"Server: address client", {address_client})
                print(f"Server: team_name_before", {team_name_before})
                try:
                    print(f"[Main Server]: Server got a message from: {address_client}")  # , message is: {message}
                    team_name = team_name_before[:-1]
                    check = team_name_before[-1:]
                    print(f"Server got message",{team_name})
                    if check == '\n':
                        self.clients_addresses.append(address_client)
                        self.clients_team_names.append(team_name)
                    else:
                        print(
                            "[Main Server]: Server got a message but it wasn't legal")  # todo legal way to handle wrong message?
                        # continue

                except Exception as e:
                    print(f"Server: Exception: {e}")
            self.divide_into_groups()
        except Exception as e:
            print(f"Server: problem with TCP socket")
            return

    def reach_winners(self, group1, group2, ):
        score_group_1 = 0
        score_group_2 = 0
        # count score for each group and get the names
        for client in group1:
            score_group_1 = score_group_1 + group1[client]
            names1 = "" + client + '\n'

        for client in group2:
            score_group_2 = score_group_2 + group2[client]
            names2 = "" + client + '\n'

        if score_group_1 > score_group_2:
            message = "Game Over! Group 1 typed in " + score_group_1 + "characters. Group 2 typed in " + score_group_2 + "characters.\n Group 1 wins!\n\n Congratulations to the winners:\n==\n" + names1
        else:
            message = "Game Over! Group 1 typed in " + score_group_1 + "characters. Group 2 typed in " + score_group_2 + "characters.\n Group 2 wins!\n\n Congratulations to the winners:\n==\n" + names2
        # send messages for clients and shut down the clients
        for client_address in range(len(self.clients_addresses)):
            self.server_TCP_socket.sendto(bytes(message, "utf-8"), client_address)
            self.server_TCP_socket.shutdown(1)
            self.server_TCP_socket.close()

    def divide_into_groups(self):
        # divide into groups
        names = self.clients_team_names
        random.shuffle(names)
        group1, group2 = [names[x::2] for x in range(2)]
        for client in group1:
            names1 = "" + client + '\n'
        for client in group2:
            names2 = "" + client + '\n'
        for client_address in range(len(self.clients_addresses)):
            message = "Welcome to Keyboard Spamming Battle Royale. \nGroup 1: \n ==\n" + names1 + "\nGroup 2: \n ==\n" + names2 + "Start pressing keys on your keyboard as fast as you can!!"
            self.server_TCP_socket.sendto(message, client_address)
        self.play_game(group1, group2)

    def run(self):
        print("Start main Server: ")
        threading.Thread(target=self.run_udp_connection).start()
        self.run_tcp_connection()
