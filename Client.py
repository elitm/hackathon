import time
import socket
# import tty
# import termios
import sys
import select

class Client:
    def __init__(self, name):
        self.team_name = name
        self.RECEIVED_PORT = 13117  # UDP
        self.SEND_PORT = 2026  # TCP
        self.DEFAULT_TIMEOUT = 10

    def start_game(self, TCP_Client_socket):
        # start the game
        # settings_before_game = termios.tcgetattr(sys.stdin)
        try:
            # tty.setcbreak(sys.stdin.fileno())
            begin_timer = time.time()
            while time.time() - begin_timer <= 10:
                data = select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
                if data:
                    client_type = sys.stdin.read(1)
                    try:
                        # self.TCP_Client_socket.send(inp.encode('utf-8'))
                        TCP_Client_socket.send(bytes(client_type, "utf-8"))  # tcp socket
                    except Exception as e:
                        break
                time.sleep(0.02)
        finally:
            print("Client")
            # to play in linux, delete the comment in next line:
            # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings_before_game)

        # Getting summary message from server
        try:
            message = (self.CP_Client_socket.recv(1024)).decode('utf-8')
            print(message)
        except Exception as e:
            print("oops! something wrong happened...")
        print("Server disconnected, listening for offer requests...\n")

    def run_Client(self):
        UDP_Client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_Client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDP_Client_socket.bind(('', self.RECEIVED_PORT))
        print(f"[Main Client]: Created main socket binded to port: {self.RECEIVED_PORT}")
        print("[Client]: Client started, listening for offer requests...")
        message, address_broadcaster = UDP_Client_socket.recvfrom(1024)
        print(f"[Main Client]: message: {message}")
        print(f"[Client]: address_broadcaster: {address_broadcaster}")

        while True:
            TCP_Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            magic_cookie, message_type, dest_port = self.split_message(message)
            is_legal = self.check_legal_offer(magic_cookie, message_type, dest_port)
            print(f"magic cookie: {magic_cookie}")
            print(f"type: {message_type}")
            print(f"port: {dest_port}")
            TCP_Client_socket.connect((address_broadcaster[0], int(dest_port)))  # todo right place?

            if is_legal:
                message = self.team_name + '\n'
                print(f"Client send message:", {message})
                TCP_Client_socket.send(bytes(message, "utf-8"))  # tcp socket
                data = TCP_Client_socket.recv(1024).decode("utf-8")  # welcome message
                print(data)
                # self.start_game()
                time.sleep(1)
        else:
            print("[Client]: Client got a message but it wasn't a BROADCAST")

    def split_message(self, m):
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
        if not dest_port == '2026':  # todo change
            flag3 = False
        return flag1 and flag2 and flag3

    def run(self):
        self.run_Client()
