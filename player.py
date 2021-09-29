# ******************************************************** import packages

import pygame
import socket
import time


# ******************************************************** class

class Ship:
    # class that represent one ship
    def __init__(self, img_name, size, top_left, on_board, hit):
        self.img_name = img_name  # the name of the ship's image
        self.size = size  # the length of the ships in pixels (40/80/120/160)
        self.top_left = top_left  # the location of the top left corner of the image
        self.on_board = on_board  # is the ship on the board? (True/False)
        self.hit = hit  # ship's length list, 0 = hasn't hit, 1 = got hit


# ******************************************************** functions

def print_screen1(screen_function, ships_list_function):
    # a function that print the first screen, the choosing screen
    # reset screen and upload image
    screen_function.set_colorkey((0, 0, 0))
    screen_function.blit(CHOOSING_SCREEN, (0, 0))
    pygame.display.flip()

    # print the black table
    for i in range(20, 461, 40):
        pygame.draw.line(screen_function, BLACK, [i, 200], [i, 640], 2)
        pygame.draw.line(screen_function, BLACK, [20, 180 + i], [460, 180 + i], 2)
    pygame.display.flip()

    # print the ships
    for obj in ships_list_function:
        obj.img_name.set_colorkey(WHITE)
        screen_function.blit(obj.img_name, obj.top_left)
    pygame.display.flip()


def print_screen2(screen_function, ships_list_function, hits_function, not_hits_function):
    # a function that print the second screen, the main screen
    # reset screen and upload image
    screen_function.set_colorkey((0, 0, 0))
    screen_function.blit(MAIN_SCREEN, (0, 0))
    pygame.display.flip()

    # print the players black table
    for i in range(20, 461, 40):
        pygame.draw.line(screen_function, BLACK, [i, 200], [i, 640], 2)
        pygame.draw.line(screen_function, BLACK, [20, 180 + i], [460, 180 + i], 2)
    pygame.display.flip()

    # print the opponent black table
    for i in range(540, 981, 40):
        pygame.draw.line(screen_function, BLACK, [i, 200], [i, 640], 2)
        pygame.draw.line(screen_function, BLACK, [540, i-340], [980, i-340], 2)
    pygame.display.flip()

    # print the ships
    for obj in ships_list_function:
        obj.img_name.set_colorkey(WHITE)
        screen_function.blit(obj.img_name, obj.top_left)
    pygame.display.flip()

    # print v's in the location that got hit
    for location in hits_function:
        TRUE_LOCATION.set_colorkey(WHITE)
        screen_function.blit(TRUE_LOCATION, location)
    pygame.display.flip()

    # print x's in the location that got hit
    for location in not_hits_function:
        FALSE_LOCATION.set_colorkey(WHITE)
        screen_function.blit(FALSE_LOCATION, location)
    pygame.display.flip()


def which_ship(ships_list_function, location):
    # return a ship type object that has been pressed, return 0 if no ship has been pressed
    for obj in ships_list_function:
        if obj.top_left[0] <= location[0] <= obj.top_left[0] + obj.size:
            if obj.top_left[1] <= location[1] <= obj.top_left[1] + 40:
                return obj
    return 0


def receive_message_from_server(my_socket_function):
    # receive and return a message from the server
    print("before receiving a message")
    # receiving the length of the message
    len_msg = my_socket_function.recv(4)
    print("the length of the message: " + str(len_msg))
    # receiving the message
    msg = my_socket_function.recv(int(len_msg.decode()))
    print("message received = " + msg.decode())
    return msg.decode()


def receive_xy_from_server(my_socket_function):
    # receive and return a x,y location from the server
    # receive x location
    x_location = int(receive_message_from_server(my_socket_function))
    # receive y location
    y_location = int(receive_message_from_server(my_socket_function))
    print("(x, y) received = (" + str(x_location) + ", " + str(y_location) + ")")
    return x_location, y_location


def send_message_to_server(my_socket_function, message):
    # send a message to the server
    print("before sending a message")
    # sending the length of the message
    len_msg = len(message.encode())
    my_socket_function.send(str(len_msg).zfill(4).encode())
    print("the length of the message: " + str(len_msg))
    # sending the message
    my_socket_function.send(str(message).encode())
    print("message sent = " + message)


def send_location_xy_to_server(my_socket_function, x_location, y_location):
    # send a x,y location to the server
    # send x location
    send_message_to_server(my_socket_function, str(x_location))
    # send y location
    send_message_to_server(my_socket_function, str(y_location))
    print("(x, y) sent = (" + str(x_location) + ", " + str(y_location) + ")")


def check_if_theres_ships(x_location, y_location):
    # check if there is a ship in the location and return true or false
    # the location in the players board
    location = (x_location - 520, y_location)
    for obj in ships_list:
        if obj.top_left[1] <= location[1] <= obj.top_left[1] + 40:
            if obj.top_left[0] <= location[0] <= obj.top_left[0] + obj.size:
                # change the hit lists according to the hit
                if obj.size == 40:
                    obj.hit[0] = 1
                if obj.size == 80:
                    if location[0] - 40 < obj.top_left[0]:
                        obj.hit[0] = 1
                    else:
                        obj.hit[1] = 1
                if obj.size == 120:
                    if location[0] - 80 > obj.top_left[0]:
                        obj.hit[2] = 1
                    elif location[0] - 40 > obj.top_left[0]:
                        obj.hit[1] = 1
                    else:
                        obj.hit[0] = 1
                if obj.size == 160:
                    if location[0] - 120 > obj.top_left[0]:
                        obj.hit[3] = 1
                    elif location[0] - 80 > obj.top_left[0]:
                        obj.hit[2] = 1
                    elif location[0] - 40 > obj.top_left[0]:
                        obj.hit[1] = 1
                    else:
                        obj.hit[0] = 1
                return "true"
    return "false"


def where_got_hit(location_received):
    # find and return the top left corner of the square of hit
    for i in range(540, 941, 40):
        if i < location_received[0] < i + 40:
            x_location = i
        if i - 340 < location_received[1] < i - 300:
            y_location = i - 340
    top_left_of_hit = (x_location, y_location)
    return top_left_of_hit


def winner(ships_list_function):
    # check if the player has won (you are the opponent)
    # True if the player won, False if they didn't won
    for obj in ships_list_function:
        for i in obj.hit:
            if i == 0:
                return False
    return True


def ships_on_board(ships_list_function):
    # check if all the ships on board
    for obj in ships_list_function:
        if not obj.on_board:
            return False
    return True


# ******************************************************** constants

# pygame constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 660
REFRESH_RATE = 1
clock = pygame.time.Clock()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# images names
CHOOSING_SCREEN = "choosing_screen.png"
MAIN_SCREEN = "main_screen.png"
WINNER = "winner.png"
LOSER = "loser.png"
SHIP4 = "4ship.jpeg"
SHIP3 = "3ship.jpeg"
SHIP2 = "2ship.jpeg"
SHIP1 = "1ship.jpeg"
SHIP4_ROTATE = "4ship_rotate.jpeg"
SHIP3_ROTATE = "3ship_rotate.jpeg"
SHIP2_ROTATE = "2ship_rotate.jpeg"
SHIP1_ROTATE = "1ship_rotate.jpeg"
FALSE_LOCATION = "false.jpeg"
TRUE_LOCATION = "true.jpeg"

# sockets constants
SERVER_PORT = 8820
SERVER_IP = "127.0.0.1"


# ******************************************************** variables

pressed_ship = 0
last_ship = 0
over = False
finish = False
hits = []
not_hits = []


# ******************************************************** main

# first pygame board
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("game")
screen.set_colorkey((0, 0, 0))
pygame.display.flip()

# upload images to pygame
CHOOSING_SCREEN = pygame.image.load(CHOOSING_SCREEN)
MAIN_SCREEN = pygame.image.load(MAIN_SCREEN)
WINNER = pygame.image.load(WINNER)
LOSER = pygame.image.load(LOSER)
SHIP4 = pygame.image.load(SHIP4).convert()
SHIP3 = pygame.image.load(SHIP3).convert()
SHIP2 = pygame.image.load(SHIP2).convert()
SHIP1 = pygame.image.load(SHIP1).convert()
SHIP4_ROTATE = pygame.image.load(SHIP4_ROTATE).convert()
SHIP3_ROTATE = pygame.image.load(SHIP3_ROTATE).convert()
SHIP2_ROTATE = pygame.image.load(SHIP2_ROTATE).convert()
SHIP1_ROTATE = pygame.image.load(SHIP1_ROTATE).convert()
FALSE_LOCATION = pygame.image.load(FALSE_LOCATION).convert()
TRUE_LOCATION = pygame.image.load(TRUE_LOCATION).convert()

# ship objects
ship_1 = Ship(SHIP4, 160, (820, 200), False, [0, 0, 0, 0])
ship_2 = Ship(SHIP3, 120, (860, 280), False, [0, 0, 0])
ship_3 = Ship(SHIP3, 120, (700, 280), False, [0, 0, 0])
ship_4 = Ship(SHIP2, 80, (900, 360), False, [0, 0])
ship_5 = Ship(SHIP2, 80, (780, 360), False, [0, 0])
ship_6 = Ship(SHIP2, 80, (660, 360), False, [0, 0])
ship_7 = Ship(SHIP1, 40, (940, 440), False, [0])
ship_8 = Ship(SHIP1, 40, (860, 440), False, [0])
ship_9 = Ship(SHIP1, 40, (780, 440), False, [0])
ship_10 = Ship(SHIP1, 40, (700, 440), False, [0])

# list of ship objects
ships_list = [ship_1, ship_2, ship_3, ship_4, ship_5, ship_6, ship_7, ship_8, ship_9, ship_10]


# first screen's loop
while not finish:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            # close
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            # buttons
            mouse_point = pygame.mouse.get_pos()
            if 800 <= mouse_point[0] <= 920 and 580 <= mouse_point[1] <= 640 and ships_on_board(ships_list):
                # start button
                finish = True
            else:
                # rotate button
                pressed_ship = which_ship(ships_list, mouse_point)
                if pressed_ship != 0 and not (600 <= mouse_point[0] <= 720 and 580 <= mouse_point[1] <= 640 and last_ship != 0):
                    pressed_ship.top_left = (20, 200)
                    last_ship = pressed_ship
                if 600 <= mouse_point[0] <= 720 and 580 <= mouse_point[1] <= 640 and last_ship != 0:
                    if last_ship.size == 40:
                        last_ship.img_name = SHIP1_ROTATE
                    if last_ship.size == 80:
                        last_ship.img_name = SHIP2_ROTATE
                    if last_ship.size == 120:
                        last_ship.img_name = SHIP3_ROTATE
                    if last_ship.size == 160:
                        last_ship.img_name = SHIP4_ROTATE
        elif event.type == pygame.KEYDOWN and last_ship != 0:
            # keyboard
            x, y = last_ship.top_left
            # move the ships
            if event.key == pygame.K_RIGHT and not last_ship.on_board and not last_ship.top_left[0] + last_ship.size == 460:
                last_ship.top_left = (x+40, y)
            if event.key == pygame.K_LEFT and not last_ship.on_board and not last_ship.top_left[0] == 20:
                last_ship.top_left = (x-40, y)
            if event.key == pygame.K_DOWN and not last_ship.on_board and not last_ship.top_left[1] == 600:
                last_ship.top_left = (x, y+40)
            if event.key == pygame.K_UP and not last_ship.on_board and not last_ship.top_left[1] == 200:
                last_ship.top_left = (x, y-40)
            if event.key == pygame.K_SPACE:
                last_ship.on_board = True

    print_screen1(screen, ships_list)

    pygame.display.flip()
    clock.tick(REFRESH_RATE)

pygame.quit()


# second pygame board
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("game")
screen.set_colorkey((0, 0, 0))
pygame.display.flip()

# second screen, only if the start button has been pressed
if 800 <= mouse_point[0] <= 920 and 580 <= mouse_point[1] <= 640 and ships_on_board(ships_list):
    print_screen2(screen, ships_list, hits, not_hits)

    # connect to server
    my_socket = socket.socket()
    my_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to server")

    # second screen's loop
    while not over:
        print_screen2(screen, ships_list, hits, not_hits)
        # stage = 0 for send/receive location
        # stage = 1 for send/receive if ship in location
        stage = 0

        # the first message of every loop: 'your turn' or 'not your turn'
        # player_or_opponent = 0 for player
        # player_or_opponent = 1 for opponent
        first_message_from_server = receive_message_from_server(my_socket)
        if first_message_from_server == "your turn":
            player_or_opponent = 0
        if first_message_from_server == "not your turn":
            player_or_opponent = 1

        # for players only, send location
        while player_or_opponent == 0 and stage == 0:
            events1 = pygame.event.get()
            for event in events1:
                if event.type == pygame.QUIT:
                    over = True
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                    if player_or_opponent == 0 and stage == 0:
                        mouse_point = pygame.mouse.get_pos()
                        send_location_xy_to_server(my_socket, str(mouse_point[0]), str(mouse_point[1]))
                        stage += 1

        # for opponent only, receive location, send if ship in location
        if player_or_opponent == 1 and stage == 0:
            x_player, y_player = receive_xy_from_server(my_socket)
            ship_in_location = check_if_theres_ships(x_player, y_player)
            stage = 1
            if ship_in_location == "true" and winner(ships_list):
                # if the player found all your ships
                send_message_to_server(my_socket, "player won")
                # open loser screen
                screen.blit(LOSER, (0, 0))
                pygame.display.flip()
                time.sleep(15)
                over = True
            else:
                # otherwise
                send_message_to_server(my_socket, ship_in_location)

        # for players only, receive if ship in location, check if won, add x's and v's
        if player_or_opponent == 0 and stage == 1:
            ship_in_location = receive_message_from_server(my_socket)
            if ship_in_location == "player won":
                # open winner screen
                screen.blit(WINNER, (0, 0))
                pygame.display.flip()
                time.sleep(15)
                over = True
            elif ship_in_location == "true":
                hits.append(where_got_hit(mouse_point))
            else:
                not_hits.append(where_got_hit(mouse_point))

    pygame.quit()

# close connection to server
my_socket.close()
