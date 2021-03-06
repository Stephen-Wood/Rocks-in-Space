# Rocks in Space!
# Stephen Wood
# 4/20/16


import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BROWN = (139, 69, 19)
LIGHTBLUE = (0, 191, 255)

#Classes go here
class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super().__init__()
        
        self.image = pygame.image.load('Asteroid 23.png').convert()
        #self.image.set_colorkey(WHITE)
        

        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.y += 1
        self.rect.x += 1
        if self.rect.y >=400:
            self.rect.y = 0   
        if self.rect.x >=700:
            self.rect.x = 0

class Ship(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
 
       # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
 
        # Load the image looking up
        self.image_original = pygame.image.load("spaceship1_small-Black.png").convert()
        self.image_original.set_colorkey(WHITE)
        
        self.image_rotate_right = pygame.transform.rotate(self.image_original, -90)
        self.image_rotate_right.set_colorkey(WHITE)
        
        self.image_rotate_left = pygame.transform.rotate(self.image_original, 90)
        self.image_rotate_left.set_colorkey(WHITE) 
        
        self.image_rotate_down = pygame.transform.rotate(self.image_original, 180)
        self.image_rotate_down.set_colorkey(WHITE)
        
        self.image_rotate_up = pygame.transform.rotate(self.image_original, 360)
        self.image_rotate_up.set_colorkey(WHITE)      
        
        # By default, point up
        
        self.image = self.image_original

        
        self.rect = self.image.get_rect()
 
      
        self.heading_x = 1
        self.heading_y = 1
        
        self.rect.x = x
        self.rect.y = y
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        

 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
        
        if self.change_x > 0:
            self.image = self.image_rotate_right
 
        if self.change_x < 0:
            self.image = self.image_rotate_left
            
        if self.change_y > 0:
            self.image = self.image_rotate_down

        if self.change_y < 0:
            self.image = self.image_rotate_up

            
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("Green_laser.png").convert()
        self.image.set_colorkey(WHITE)
        
        self.change_x = ship.heading_x
        self.change_y = ship.heading_y
            
        self.rect = self.image.get_rect()
        print(self.change_x, self.change_y)
        
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        

# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

asteroid_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

laser_list = pygame.sprite.Group()


for i in range(25):
     #This represents an asteroid
    asteroid = Asteroid()
 
     #Set a random location for the asteroid
    asteroid.rect.x = random.randrange(screen_width)
    asteroid.rect.y = random.randrange(screen_height)
     
     #Add the asteroid to the list of objects
    asteroid_list.add(asteroid)
    all_sprites_list.add(asteroid)
    
ship = Ship(350, 200)
all_sprites_list.add(ship)

laser = Laser()
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
lives = 5

 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
# Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.changespeed(-3, 0)
                ship.heading_x = -3
                ship.heading_y = 0
            elif event.key == pygame.K_RIGHT:
                ship.changespeed(3, 0)
                ship.heading_x = 3
                ship.heading_y = 0
                print(ship.heading_x)
                print(ship.heading_y)
            elif event.key == pygame.K_UP:
                ship.changespeed(0, -3)
                ship.heading_x = 0
                ship.heading_y = -3
            elif event.key == pygame.K_DOWN:
                ship.changespeed(0, 3)
                ship.heading_x = 0
                ship.heading_y = 3
            elif event.key == pygame.K_SPACE:
                laser.change_x = ship.heading_x
                laser.change_y = ship.heading_y
                laser.rect.x = ship.rect.x
                laser.rect.y = ship.rect.y
                all_sprites_list.add(laser)
                laser_list.add(laser)

    # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ship.changespeed(3, 0)
                
            elif event.key == pygame.K_RIGHT:
                ship.changespeed(-3, 0)
                
            elif event.key == pygame.K_UP:
                ship.changespeed(0, 3)
               
            elif event.key == pygame.K_DOWN:
                ship.changespeed(0, -3)             
                
   
    # Clear the screen
    screen.fill(BLACK)
    
    all_sprites_list.update()
    
    for laser in laser_list:
        asteroids_hit_list = pygame.sprite.spritecollide(laser, asteroid_list, True)
        
        for asteroid in asteroids_hit_list:
            laser_list.remove(laser)
            all_sprites_list.remove(laser)
            score += 10
              
       
    asteroids_hit_list = pygame.sprite.spritecollide(ship, asteroid_list, True) 
    
    for asteroid in asteroids_hit_list:
        lives -= 1
        if lives <= 0:
            done = True
        
    all_sprites_list.draw(screen)
 
    # Limit to 60 frames per second
    clock.tick(60)
     
    pygame.display.flip()
     
pygame.quit()