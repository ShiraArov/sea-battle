# ******************************************************** import packages

import socket
import select


# ******************************************************** functions

def print_client_sockets(client_sockets_function):
    # print the clients
    for c in client_sockets_function:
        print("\t", c.getpeername())


def receive_message_from_client(client_socket):
    # receive and return a message from the server
    print("before receiving a message")
    # receiving the length of the message
    len_msg = client_socket.recv(4)
    print("the length of the message: " + str(len_msg))
    # receiving the message
    msg = client_socket.recv(int(len_msg.decode()))
    print("message received = " + msg.decode())
    return msg.decode()


def send_message_to_client(message, client_socket):
    # send a message to the server
    print("before sending a message")
    # sending the length of the message
    len_msg = len(message.encode())
    client_socket.send(str(len_msg).zfill(4).encode())
    print("the length of the message: " + str(len_msg))
    # sending the message
    client_socket.send(message.encode())
    print("message sent = " + message)


def receive_location_xy_from_client(client_socket):
    # receive and return a x,y location from the server
    # receive x location
    x_location = int(receive_message_from_client(client_socket))
    # receive y location
    y_location = int(receive_message_from_client(client_socket))
    print("(x, y) received = (" + str(x_location) + ", " + str(y_location) + ")")
    return x_location, y_location


def send_location_xy2client(client_socket, x_location, y_location):
    # send a x,y location to the server
    # send x location
    send_message_to_client(str(x_location), client_socket)
    # send y location
    send_message_to_client(str(y_location), client_socket)
    print("(x, y) sent = (" + str(x_location) + ", " + str(y_location) + ")")


# ******************************************************** constants

# sockets constants
MAX_MSG_LENGTH = 1024
SERVER_PORT = 8820
SERVER_IP = "0.0.0.0"


# ******************************************************** variables

finish = False
mouse_pos_list = []
pos_from = []
client_sockets = []
messages_to_send = []
count = 0
player = 0
opponent = 1

# ******************************************************** main

# setting the connection with the clients
print("Setting up server...")
server_socket = socket.socket()
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

# main loop
while not finish:
    # select
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    if len(client_sockets) < 2:
        # limit the connection for 2 clients
        for current_socket in rlist:
            if current_socket is server_socket:
                # add another client
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
                print_client_sockets(client_sockets)
    else:
        # send 'your turn' and 'not your turn' messages to clients
        send_message_to_client("your turn", client_sockets[player])
        send_message_to_client("not your turn", client_sockets[opponent])

        # receive location from the player
        x_board_player, y_board_player = receive_location_xy_from_client(client_sockets[player])

        # send location to opponent
        send_location_xy2client(client_sockets[opponent], x_board_player, y_board_player)

        # receive if ship in location from the opponent
        ship_in_location = receive_message_from_client(client_sockets[opponent])

        # send if ship in location to player
        send_message_to_client(ship_in_location, client_sockets[player])

        # switch the player and the opponent if necessary
        if ship_in_location == "false":
            if player == 0:
                player = 1
                opponent = 0
            else:
                player = 0
                opponent = 1

# close connection
client_sockets[0].close()
client_sockets[1].close()
server_socket.close()