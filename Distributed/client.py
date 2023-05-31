import pygame
from pygame.locals import *
import random
from network import Network
from player import PlayerVehicle , Vehicle

pygame.init()
print("here pygame")



def main():

    # create window 
    width = 500
    height = 500 
    screen_size = (width,height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Asphalt 1')

    # colors
    gray = (100, 100, 100)
    green = (76, 208, 56)
    red = (200,0,0)
    white = (255,255,255)
    yellow = (255,232,0)

    #game settings
    game_over=False
    speed=2
    #score=0

    #marker size 
    marker_width=10
    marker_height=50

    #road and road egde markers rectangles
    road=(100,0,300,height) # road rectangle x,y,width,height
    left_edge_marker=(95,0,marker_width,height)
    right_edge_marker=(395,0,marker_width,height)

    # x coordinates of lanes
    left_lane=150
    centre_lane= 250
    right_lane= 350
    lanes=[left_lane,centre_lane,right_lane]

    #animate movement of lane markers
    lane_marker_move_y=0


    image = pygame.image.load('cars/pitstop_car_14.png')
    image1 = pygame.image.load('cars/pitstop_car_13.png')
    image2 = pygame.image.load('cars/pitstop_car_12.png')

    players = [PlayerVehicle(image,250,400),
            PlayerVehicle(image1,250,400),
            PlayerVehicle(image2,250,400)]

    #create the player's car
    player_group=pygame.sprite.Group()

    #load the other vehicle images
    image_filenames=['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
    vehicle_images=[]
    for image_filename in image_filenames:
        image=pygame.image.load('images/'+image_filename)
        vehicle_images.append(image)

    #sprite group for vehicles
    vehicle_group= pygame.sprite.Group()

    #load crash image
    crash = pygame.image.load('images/crash.png')
    crash_rect=crash.get_rect()
    running = True
    '''
    making run false until receiving tru form server and server
    only sends true if 2 clients are connected.
    '''
    n = Network()
    player_id = n.getPLayer_id()
    print('pid',player_id)
    player = players[player_id]
    player_group.add(player)
    clock = pygame.time.Clock()
    fps=60
    player2_id = n.getPLayer_id()
    print("player 2 id: ", player2_id)
    player2= players[player2_id]

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        #moving player's car using left and right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 10
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 10

            #check if there is a side swipe collision after changing the lane
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player,vehicle):
                    game_over=True
                    #place the player's car next to the other vehicle and 
                    #determine where to position the crash image 
                    if event.key == K_LEFT:
                        player.rect.left=vehicle.rect.right
                        crash_rect.center= [player.rect.left,(player.rect.center[1]+vehicle.rect.center[1])/2]
                    elif event.key == K_RIGHT:
                        player.rect.right=vehicle.rect.left
                        crash_rect.center= [player.rect.right,(player.rect.center[1]+vehicle.rect.center[1])/2]
    
        #draw the grass
        screen.fill(green)

        #draw the road
        pygame.draw.rect(screen,gray,road) #screen,color,rect

        #darw road edge markers
        pygame.draw.rect(screen,yellow,left_edge_marker)
        pygame.draw.rect(screen,yellow,right_edge_marker)


        #moving the lane markers
        lane_marker_move_y += speed *2
        if lane_marker_move_y>= marker_height*2:
            lane_marker_move_y=0
        #drawing the lane marker
        for y in range(marker_height * -2,height,marker_height*2):
            pygame.draw.rect(screen,white,(left_lane +45,y+lane_marker_move_y,marker_width,marker_height))
            pygame.draw.rect(screen,white,(centre_lane +45,y+lane_marker_move_y,marker_width,marker_height))
    
        #draw the player's car
        player_group.draw(screen)

        # add up to two vehicles
        if len(vehicle_group) < 2:
            #ensure there is enough gap between vehicles
            add_vehicle=True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False

            if add_vehicle:
                # select a random lane
                lane= random.choice(lanes)

                # select a random vehicle image
                image= random.choice(vehicle_images)
                vehicle=Vehicle(image,lane,height/-2)
                vehicle_group.add(vehicle)

        # make the vehicles move
        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            # remove the vehicle once it goes off screen
            if vehicle.rect.top >= height:
                vehicle.kill()

                # add to score
                player.incrementScore()
                player2.score=n.send(player.score)

                #speed up the game after passing 5 vehicles
                if player.score> 0 and player.score % 5 ==0:
                    speed+=1

        #draw the vehicles
        vehicle_group.draw(screen)

        #display the score 
        font=pygame.font.Font(pygame.font.get_default_font(),16)
        text = font.render('score: '+str(player.score),True,white)
        text_rect=text.get_rect()
        text_rect.center=(50,450)
        screen.blit(text,text_rect)

        #check if there is a head on collision
        if pygame.sprite.spritecollide(player,vehicle_group,True):
            game_over=True
            crash_rect.center=[player.rect.center[0],player.rect.top]

        #display gameover
        if game_over:
            screen.blit(crash,crash_rect)
            pygame.draw.rect(screen,red,(0,50,width,100))
            font=pygame.font.Font(pygame.font.get_default_font(),16)
            text=font.render("game over. Play again? enter y or n",True,white)
            text_rect=text.get_rect()
            text_rect.center=(width/2,100)
            screen.blit(text,text_rect)
        pygame.display.update()

        #check if player wants to play again
        while game_over:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over=False
                    running=False
                #get the players input
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        #reset the game
                        game_over=False
                        speed=2
                        player.resetScore()
                        vehicle_group.empty()
                        player.rect.center=[players[player_id].x,400]
                    elif event.key == K_n:
                        game_over=False
                        running=False
                        pygame.quit()

    pygame.quit()


main()