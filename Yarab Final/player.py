import pygame
import os
import pickle

class Vehicle(pygame.sprite.Sprite):

    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)

        #scale the image down so it fits the lane
        image_scale = 45 /image.get_rect().width
        new_width= image.get_rect().width *image_scale
        new_height= image.get_rect().height*image_scale
        self.image = pygame.transform.scale(image,(new_width,new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    """ 
        temp_filename = 'temp_image.png'
        pygame.image.save(self.image, temp_filename)
        self.image_path = temp_filename

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']
        image_path = "temp_image.png"
        pygame.image.save(self.image, image_path)
        state['image_path'] = image_path
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = pygame.image.load(state['image_path']).convert_alpha()
        self.rect = self.image.get_rect()
        os.remove(state['image_path'])
        
        """

class PlayerVehicle(Vehicle):

    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.score=0

    def incrementScore(self):
        self.score = self.score + 1

    def resetScore(self):
        self.score=0

    '''def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
            return "moved left"

        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
            return "moved right"'''
        



class Vehiclez(pygame.sprite.Sprite):

    def __init__(self,x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


class PlayerVehiclez(Vehiclez):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
            return "moved left"

        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
            return "moved right"
        

'''image=pygame.image.load('Distributed/cars/pitstop_car_3.png')
player=PlayerVehicle(image,250,400)
player.incrementScore()
player.incrementScore()
player.incrementScore()
print(player.score)
player.resetScore()
print(player.score)
print(1<1)'''