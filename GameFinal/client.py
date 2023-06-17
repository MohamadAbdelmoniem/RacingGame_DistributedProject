import pickle
import pygame
from pygame.locals import *
import random
from network import Network
from player import PlayerVehicle, Vehicle
import socket
import sys
from button import Button

pygame.init()
# create window
width = 1280
height = 720
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Asphalt 1")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
BG = pygame.image.load("assets/Background.png")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5550))


def play():
    
    # colors
    gray = (100, 100, 100)
    green = (76, 208, 56)
    red = (200, 0, 0)
    white = (255, 255, 255)
    yellow = (255, 232, 0)

    # game settings
    game_over = False
    speed = 2

    current_frame = 0

    shift_right = 80
    # marker size
    marker_width = 10
    marker_height = 80

    # road and road egde markers rectangles
    road = (100 + shift_right, 0, 300, height)  # road rectangle x,y,width,height
    left_edge_marker = (95 + shift_right, 0, marker_width, height)
    right_edge_marker = (395 + shift_right, 0, marker_width, height)

    # x coordinates of lanes
    left_lane = 150 + shift_right
    centre_lane = 250 + shift_right
    right_lane = 350 + shift_right
    lanes = [left_lane, centre_lane, right_lane]

    # animate movement of lane markers
    lane_marker_move_y = 0

    image = pygame.image.load("cars/pitstop_car_14.png")
    image1 = pygame.image.load("cars/pitstop_car_13.png")
    image2 = pygame.image.load("cars/pitstop_car_12.png")
    image3 = pygame.image.load("cars/pitstop_car_20.png")
    image3.set_alpha(128)

    players = [
        PlayerVehicle(image, 250 + shift_right, 400),
        PlayerVehicle(image1, 250 + shift_right, 400),
        PlayerVehicle(image2, 250 + shift_right, 400),
    ]

    opponent_player = PlayerVehicle(image3, 250 + shift_right, 400)
    opponent_group = pygame.sprite.Group()
    opponent_group.add(opponent_player)

    # create the player's car
    player_group = pygame.sprite.Group()

    # load the other vehicle images
    image_filenames = ["pickup_truck.png", "semi_trailer.png", "taxi.png", "van.png"]
    vehicle_images = []
    for image_filename in image_filenames:
        image = pygame.image.load("images/" + image_filename)
        vehicle_images.append(image)

    # sprite group for vehicles
    vehicle_group = pygame.sprite.Group()

    # load crash image
    crash = pygame.image.load("images/crash.png")
    crash_rect = crash.get_rect()
    running = True
    
    player_id = pickle.loads(client.recv(1024))

    player = players[player_id]
   

    player_group.add(player)
   
    clock = pygame.time.Clock()
    fps = 60

    player_score = 0
    opponent_score = 0
    opponent_position = (330,400)

    opponent_player_pos = (opponent_player.rect.x, opponent_player.rect.y)

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # moving player's car using left and right arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player.rect.center[0] > left_lane:
                    player.rect.x -= 10
                    client.send(pickle.dumps((player.score, (player.rect.x, player.rect.y))))
                    data = pickle.loads(client.recv(1024))
                    #opponent_position = data["positions"][1-player_id]
                    #opponent_player.rect.x, opponent_player.rect.y = opponent_position


                elif event.key == pygame.K_RIGHT and player.rect.center[0] < right_lane:
                    player.rect.x += 10
                    client.send(pickle.dumps((player.score, (player.rect.x, player.rect.y))))
                    data = pickle.loads(client.recv(1024))
                    #opponent_position = data["positions"][1-player_id]
                    #opponent_player.rect.x, opponent_player.rect.y = opponent_position
  
                #opponent_player.rect.x, opponent_player.rect.y = opponent_position
              

                # check if there is a side swipe collision after changing the lane
                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):
                        game_over = True
                        # place the player's car next to the other vehicle and
                        # determine where to position the crash image
                        if event.key == K_LEFT:
                            player.rect.left = vehicle.rect.right
                            crash_rect.center = [
                                player.rect.left,
                                (player.rect.center[1] + vehicle.rect.center[1]) / 2,
                            ]
                        elif event.key == K_RIGHT:
                            player.rect.right = vehicle.rect.left
                            crash_rect.center = [
                                player.rect.right,
                                (player.rect.center[1] + vehicle.rect.center[1]) / 2,
                            ]

        # draw the grass
        screen.fill(green)

        # draw the road
        pygame.draw.rect(screen, gray, road)  # screen,color,rect

        # darw road edge markers
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)

        # moving the lane markers
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        # drawing the lane marker
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(
                screen,
                white,
                (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
            )
            pygame.draw.rect(
                screen,
                white,
                (centre_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
            )

            

        # draw the player's car
        player_group.draw(screen)

        # add up to two vehicles
        if len(vehicle_group) < 2:
            # ensure there is enough gap between vehicles
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False

            if add_vehicle:
                # select a random lane
                lane = random.choice(lanes)

                # select a random vehicle image
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)

        # make the vehicles move
        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            # remove the vehicle once it goes off screen
            if vehicle.rect.top >= height:
                vehicle.kill()
                player.incrementScore()
                #client.send(pickle.dumps(player.score))
                client.send(pickle.dumps((player.score, (player.rect.x, player.rect.y))))
                #scores =list(pickle.loads(client.recv(1024)).values())
                #positions = list(pickle.loads(client.recv(1024)).values())
                data = pickle.loads(client.recv(1024))
                #print(scores)
                #print(positions)
                print(data)
                player.score = data["scores"][player_id]
                opponent_position = data["positions"][1-player_id]
                opponent_score = data["scores"][1-player_id]
                opponent_player_pos = opponent_position
                    
                

                # speed up the game after passing 5 vehicles
                if player.score > 0 and player.score % 5 == 0:
                    speed += 1

        opponent_player.rect.x, opponent_player.rect.y = opponent_player_pos

        # draw the vehicles
        vehicle_group.draw(screen)

        opponent_group.draw(screen)


        # display the score
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render("score: " + str(player.score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 450)
        screen.blit(text, text_rect)

        # display the opponent's score
        opponent_text = font.render("opponent score: " + str(opponent_score), True, white)
        opponent_text_rect = opponent_text.get_rect()
        opponent_text_rect.center = (80, 470)
        screen.blit(opponent_text, opponent_text_rect)

        # check if there is a head on collision
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            game_over = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

        # display gameover
        if game_over:
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, red, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render("game over. Play again? enter y or n", True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
    

        pygame.display.update()

        # check if player wants to play again
        while game_over:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = False
                    running = False
                # get the players input
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        # reset the game
                        game_over = False
                        speed = 2
                        player.resetScore()

                        vehicle_group.empty()
                        player.rect.center = [250, 400]
                    elif event.key == K_n:
                        player.resetScore()
                        game_over = False
                        running = False
                        pygame.quit()

    pygame.quit()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

main_menu()
