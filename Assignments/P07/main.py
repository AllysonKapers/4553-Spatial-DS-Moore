from cmath import rect
import pygame, sys, random

#used in game to create points within window, 
#window maxes = x, y
def makePoint(x, y):

    xX = random.randint(0,x)
    yY = random.randint(0,y)

    #returns random tuple
    return (xX,yY)

#define window size
Window = (400,400)

def gamePlay():
    #basic start
    pygame.init()
    screen = pygame.display.set_mode(Window)
    pygame.display.set_caption('P07')

    #create list of points based off window size
    x = Window[0]
    y = Window[1]

    PointsList = []
    Num_of_Points = int((x / 100) * (y / 100) * 2.5)

    #fills in list with random points within the window
    for i in range(Num_of_Points):
        newPoint = makePoint(x,y)
        PointsList.append(newPoint)

    #rectangle 

    #starting coord(starting at top left)
    x_start = 0
    y_start = 0
    #width and height
    r_height = 100
    r_width = 100
    #initializes
    rectangle = pygame.Rect(x_start, y_start, r_width, r_height)

    active = 'true'
    pause = False

    while True:
        #fills screen and draws rectangle 
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color('white'), rectangle, 2)

        radi = 3
        radi_big = 5
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and active == 'true':
                    # pause game if p is pressed
                    active = 'paused'
                    print('Pause is being pressed')
                elif event.key == pygame.K_p and active == 'paused':
                    # unpause the game
                    active = 'true'
                    print('Continue is being pressed')
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)    
        
        
        if active == 'true':
            for i in PointsList:
                if rectangle.collidepoint(i):
                    
                    #draws larger circles for points inside rectangle in yellow
                    pygame.draw.circle(screen,pygame.Color('yellow'), i, radi_big,0)

                    
                else:
                    #draws smaller circles for points outside rectangle in blue
                    pygame.draw.circle(screen, pygame.Color('blue'), i, radi, 0)   
                
            #moves the rectangle from left to right, moves down a row when it reaches the end of the row
            #updates display as necessary
            rectangle.move_ip(1,0)
            if rectangle.right > Window[0]:
                rectangle.move_ip(-Window[0],50)
            pygame.display.update()
            pygame.time.Clock().tick(360)
            if rectangle.bottom > Window[1]:
                rectangle.move_ip(-Window[0],-Window[1])
            pygame.display.update()
            pygame.time.delay(10)
            
            pygame.display.flip()   

          
#runs main
if __name__ == '__main__':
    # go to the function definition, and draw the screen items.
    gamePlay()
    
