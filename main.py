import cv2
from PIL import ImageGrab
import numpy as np
from logic import Object, record_screen
import pyautogui as gui
import time

start_time = time.time()
prev_time = time.time()
speed_rate = 1.8
player_index = 0
enemy_index = 0
distance_to_jump = 120

player = [Object("images/dino.png"), Object("images/dino_b.png")]
enemies = [
    [Object("images/bird.png"), Object("images/cact1.png"), Object("images/cact2.png")],
    [Object("images/bird_b.png"), Object("images/cact1_b.png"), Object("images/cact2_b.png")]
]

while 1:
    img = record_screen()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if player[0].match(img):
        top_left_x = int(player[0].location[0][0] - player[0].width)
        top_left_y = int(player[0].location[0][1] - 3*player[0].height)
        bottom_right_x = int(player[0].location[1][0] + 14*player[0].width)
        bottom_right_y = int(player[0].location[1][1] + 0.5*player[0].height)
        screen_start = (top_left_x, top_left_y)
        screen_end = (bottom_right_x, bottom_right_y)
        break


gui.press("up")


while 1:
    img_o = record_screen(bbox=(*screen_start, *screen_end))
    img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)

    if player[0].match(img):
        player_index = 0
        enemy_index = 0
    elif player[1].match(img):
        player_index = 1
        enemy_index = 1

    if time.time() - prev_time > 1:
        if time.time() - start_time < 180 and player[player_index].location:
            distance_to_jump += speed_rate

        prev_time = time.time()

    if player[player_index].location:
        cv2.rectangle(img_o, player[player_index].location[0], player[player_index].location[1], (255, 0, 0), 2)

    for enemy in enemies[enemy_index]:
        if enemy.match(img):
            cv2.rectangle(img_o, enemy.location[0], enemy.location[1], (0, 0, 255), 2)

            horizontal_distance = enemy.location[0][0] - player[player_index].location[1][0]
            vertical_distance = player[player_index].location[0][1] - enemy.location[1][1]

            if player[player_index].location:
                if horizontal_distance < distance_to_jump and vertical_distance < 2:
                    gui.press('up')
                    break

    cv2.imshow("Screen", img_o)
    if cv2.waitKey(1) == ord('q'):
        break
