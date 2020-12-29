import struct
import time
from _thread import start_new_thread
import random
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname, SOL_SOCKET, SO_BROADCAST
import socket as sock

# Class Server
class Server:

    # Global servers listen port number
    LISTEN_PORT = 13117
    DEFAULT_TIMEOUT = 10 #todo seconds?
    listen = False
    MAX_THREAD_NUMBER = 4 #todo maybe change?

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
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        clients_addresses = []
        clients_team_names = []
        ip_address = sock.gethostbyname(sock.gethostname())

        # Send Broadcast message
        print(f"Server started, listening on IP address {ip_address}")
        magic_cookie = bytes.fromhex('feedbeef')
        message_type = bytes.fromhex('02')
        dest_port = self.LISTEN_PORT.to_bytes(2, byteorder='big')
        message = magic_cookie + message_type + dest_port  # todo maybe utf-8
        # message = message.encode("utf-8")  # + (" " * (586 - len(message.encode("utf-8")))).encode("utf-8")
        server_socket.sendto(message, ('255.255.255.255', dest_port))
        # TIMER FOR SEC
        print(f"[Server]: waiting for client to respond") # todo delete

        server_socket.settimeout(2)
        timer = time.time() + 2 # todo 2?
        while (time.time() - timer) < 0:
            try:
                print("[Main Server]: Server waiting for message")
                message, address_client = server_socket.recvfrom(1024)

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
                        print("[Main Server]: Server got a message but it wasn't legal")  # todo legal way to handle wrong message?
                        continue

                except Exception as e:
                    print(f"Server: Exception: {e}")

            except Exception as e:
                if len(clients_addresses) != 0:
                    continue
                else:
                    print("[Server]: could not find any servers")
                    return
        server_socket.settimeout(None)

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
            print(f"[Client]: sending {client_address}\nmessage: {message}") # todo delete
            server_socket.sendto(message, client_address)

        for client_address in range(len(clients_addresses)):
            start_new_thread(self.handle_client, client_address)

        #     # Send data
        # print(f"[Client]: waiting for servers answer's")
        # client_socket.settimeout(Client.DEFAULT_TIMEOUT)

    def handle_client(self, address, port):

        # Creating socket
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(('', 0))

        # Sent OFFER to the client
        print(f"[Server thread]: New server thread was created for client: {address}")

        server_socket.sendto(send_type(2), (address, port))
        print(f"[Server thread]: Send offer message to: {address}, {port}")  #  , message is: {send_type(2)}

        try:
            # Wait for message
            print("[Server thread]: Thread: Waiting for REQUEST")
            server_socket.settimeout(5)
            time_out = time.time() + 5

            while (time.time() - time_out) < 0:

                message, address_request = server_socket.recvfrom(1024)

                print(f"[Server thread]: Got a message from: {address_request}")

                try:
                    team_name, message_type, hashed_word, word_size, start_range, end_range = split_message(message)

                    # Check type is REQUEST
                    if message_type != "3":
                        print("[Server thread]: Got a message but it wasn't a REQUEST")

                    else:
                        server_socket.settimeout(Server.DEFAULT_TIMEOUT)
                        break

                except Exception as e:
                    print(f"[Server thread]: Got a timeout and didn't got a message")

            print("[Server Thread]: Got a REQUEST message")

            team_name, message_type, hashed_word, word_size, start_range, end_range = split_message(message)

            print("[Server Thread]: Start solving")
            original_word = solve(hashed_word, start_range, end_range)

            if original_word is not None:

                print(f"[Server thread]: Solve hash and found: {original_word}")

                server_socket.sendto(build_message(self.team_name,
                                                   "4",
                                                   hashed_word,
                                                   word_size,
                                                   original_word),
                                     address_request)

            else:
                print("[Server thread]: Send NACK")

                server_socket.sendto(send_type(5), address_request)

        except TimeoutError as e:
            print(f"[Server thread]: TimeoutError: {e}")
            server_socket.sendto(send_type(5), address_request)

        except IndexError as e:
            print(f"[Server thread]: IndexError: {e}")
            server_socket.sendto(send_type(5), address_request)

        except Exception as e:
            print(f"[Server thread]: Exception: {e}")
            server_socket.sendto(send_type(5), address_request)

        finally:
            print("[Server thread]: Closing...")
            server_socket.close()
