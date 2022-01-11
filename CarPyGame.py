import pygame
import time
import random
pygame.init() #To initiate PyGame Modules: 1st thing to do always
display_width = 1000
display_height = 750


#Defining colors: As a tuples in form (R,G,B)
black = (0,0,0) 
white = (220,220,220)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

carImg = pygame.image.load('racecar.png')
gameDisp = pygame.display.set_mode((display_width,display_height)) #Resolution in form of tuple
pygame.display.set_caption('PK Game')
clock = pygame.time.Clock() #Clock used in game to set refresh rate

def things_dodged(count):
    font = pygame.font.SysFont(None , 40)
    text = font.render("Dodged: " + str(count) , True , green)
    gameDisp.blit(text , (0,0))  

def things(thingX , thingY , thingW , thingH , color):
    pygame.draw.rect(gameDisp , color , [thingX,thingY,thingW,thingH]) 

def car(x,y): #Function to display car at (x,y) coordinate 
    gameDisp.blit(carImg , (x,y)) #inbuild function to display. Image , ():tuple of (x,y) coordinate

def text_objects(text , font):
    textSurf = font.render(text , True , red) #Render is in pygame. Mid value = True (Just remember)
    return textSurf , textSurf.get_rect() #get_rect() gives us the rectangle to fit in. 

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf' , 115) #For font type and the font Size: 115 (Large)
    textSurf , textRect = text_objects(text , largeText)
    textRect.center = ((display_width/2),(display_height/2))
    gameDisp.blit(textSurf , textRect)
    pygame.display.update()

    

def crash():
    message_display('You Crashed!')
    pygame.display.update()
    gameLoop() #To start the game again. 

def gameLoop():
    x = display_width*0.44
    y = display_height*0.78

    dodged = 0

    car_width = 113
    car_height = 150 #150 is just rand for now.

    xChange = 0

    thing_startx = random.randrange(0,display_width-300)
    thing_starty = -600
    thing_speed = 7 #7 pixels
    thing_width = random.randrange(150,300)
    thing_height = 100

    road_startx = display_width/2 - 12
    road_starty = -600
    road_width = 25
    road_height = 200

    road2_startx = display_width/2 - 12
    road2_starty = -120
    road2_width = 25
    road2_height = 200


    gameExit = False

    while not gameExit:
        for event in pygame.event.get(): #Recives events from the game
            if event.type == pygame.QUIT:
                time.sleep(2)
                gameExit = True 
            
            if event.type == pygame.KEYDOWN: #This Just returns True if a key is pressed
                if event.key == pygame.K_LEFT: #If Left key is pressed
                    xChange = -5 
                if event.key == pygame.K_RIGHT :#If Right key is pressed
                    xChange = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xChange = 0
        
        x += xChange 
        gameDisp.fill(white) #To fill background

        things(road_startx , road_starty , road_width , road_height , black)
        road_starty += thing_speed 

        things(road2_startx , road2_starty , road2_width , road2_height , black)
        road2_starty += thing_speed 

        things(thing_startx , thing_starty , thing_width , thing_height , blue)
        thing_starty += thing_speed 

        car(x,y)
        things_dodged(dodged) 

        if x>(display_width - car_width) or x<0: 
            #At this point our car crashes into the boundaries
            crash()
            gameExit = True 

        carLeftMost = x 
        carRightMost = x+ car_width 
        carTopMost = y 
        carDownMost = y + car_height

        blockLeftMost = thing_startx
        blockRightMost = thing_startx + thing_width 
        blockTopMost = thing_starty
        blockDownMost = thing_starty + thing_height 

        #Below are 4 cases to crash with the object: 
        f1 = False
        f2 = False
        if carLeftMost<blockRightMost and carRightMost>blockRightMost:
            f1 = True

        if carRightMost>blockLeftMost and carLeftMost<blockLeftMost:
            f1 = True

        if carLeftMost>blockLeftMost and carRightMost<blockRightMost:
            f1 = True
        
        if carTopMost < blockDownMost and carDownMost > blockDownMost:
            f2 = True

        if carDownMost > blockTopMost and carTopMost < blockTopMost:
            f2 = True 
        
        if (f1 and f2):
            crash()
            gameExit = True 

        if thing_starty > display_height: #This is case when the doges the block and block passes by the screen
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            thing_width = random.randrange(0,500)
            
            dodged += 1 #Incrementing number of dodged blocks  
            if(dodged %3 == 0): #Increasing speed by 1 after every 3 dodges. 
                thing_speed += 1 
        
        if road_starty > display_height:
            road_starty = 0 - road_height
        
        if road2_starty > display_height:
            road2_starty = 0 - road2_height

        pygame.display.update() #To update the screen of the game
        clock.tick(60) #Refresh Rate
    
gameLoop() 
pygame.quit()
quit() 
