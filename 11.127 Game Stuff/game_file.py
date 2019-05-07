import pygame
import sys

# define some colors in the RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

group_1 = ["1.1","1.2","1.3"]       # Level Titles
group_2 = ["2.1","2.2","2.3"]
group_3 = ["3.1","3.2","3.3"]
free = ["4.1","4.2","4.3"]
screen_list = ["Title","Select",group_1,group_2,group_3,free]       # Screen List

current_screen = screen_list[2][0]      # Starting screen, adjust to work on specific screen at startup

    # set up pygame and its screen
pygame.init()
screen = pygame.display.set_mode((1200,1200))       # sets display size
pygame.display.set_caption("AVALANCHE")     # Title

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Arial', 30)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background('Background.png', [0,0])
start = pygame.sprite.Sprite()
start.image = pygame.image.load("Start.png").convert_alpha()
start.rect = start.image.get_rect()
start.rect.topleft = [360,600]

def level_select(button,point):     # func for selecting level from start screen
    (px,py) = point
    if button == "button_1_1":      # sets x and y boundaries for each button on the screen
        x,y = 80,310
        group = 2                   # sets which group of levels and which specific level for indexing
        level = 0
    elif button == "button_1_2":
        x,y = 170,310
        group = 2
        level = 1
    elif button == "button_1_3":
        x,y = 255,310
        group = 2
        level = 2
    elif button == "button_2_1":
        x,y = 480,310
        group = 3
        level = 0
    elif button == "button_2_2":
        x,y = 570,310
        group = 3
        level = 1
    elif button == "button_2_3":
        x,y = 655,310
        group = 3
        level = 2
    elif button == "button_3_1":
        x,y = 880,310
        group = 4
        level = 0
    elif button == "button_3_2":
        x,y = 970,310
        group = 4
        level = 1
    elif button == "button_3_3":
        x,y = 1055,310
        group = 4
        level = 2
    else:
        print("ELSE")
        x,y = 0,0

    if px >= x and px < x + 70 and py >= y and py < y + 70:     # checks if point is within button space
        print("entered")
        return (group,level)    # returns indices 
    else:
        return None

class Player(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Cabin(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cabin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Slider(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def start(self,location):
        self.start = location[0]
        self.x = self.start
        self.y = location[1]
        self.w = 25
        self.h = 50
        self.value = 0
        self.image = pygame.draw.rect(screen,[255,0,0],(self.start,self.y,self.w,self.h))
        self.moving = False
    def update(self,new_x):
        pygame.draw.rect(screen,[237,216,223],(self.x,self.y,self.w,self.h))
        if new_x-self.start>120:
            self.x = self.start+120
        elif new_x-self.start<-120:
            self.x = self.start-120
        else:
            self.x = new_x
        self.value = round((self.x-self.start)/24)
        self.draw()
        print(self.value)
    def draw(self):
        self.image = pygame.draw.rect(screen,[255,0,0],(self.x,self.y,self.w,self.h))

class Line(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 50
        self.y = 519
        self.w = 630
        self.h = 10
    def draw(self):
        self.image = pygame.image.load("Cabin.png").convert_alpha()
        self.rect = self.image.get_rect()

        
        # self.rect = self.image.get_rect()
    def rotate(self,angle):
        # self.image = pygame.transform.rotate(screen,angle)
        # self.rect = self.image.get_rect()
        pygame.transform.rotate(self.image,angle)
        
Tutorial_1_1 = False
Tutorial_1_2 = False
Tutorial_2_1 = False
Tutorial_2_2 = False
Tutorial_3_1 = False
Tutorial_3_2 = False

slider_moving = False

m_slider = Slider()
m_slider.start((915,425))
line_1_1 = Line()

run = True      # will continue to run until quit button hit, loop found farther down
while run:
    # pygame.time.delay(10)  # idk a website online kept advising using delays because it flickers but probably can remove later
    screen.fill([255, 255, 255]) 
    if current_screen == "Title":       # each level is an if statement so the levels can be adjusted independently
        screen.blit(BackGround.image, BackGround.rect)  # adds background
        screen.blit(start.image, start.rect)        # adds start button
        title = pygame.image.load("Title.png").convert_alpha()      # adds title
        screen.blit(title,(170,50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                if x >= 360 and x < 360 + 500 and y >= 500 and y < 500 + 155:   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True


    elif current_screen == "Select":        # SELECT SCREEN
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)
        select_1 = pygame.image.load("Select_1.png").convert_alpha()        # inserts all button images
        screen.blit(select_1,(50,200))
        select_2 = pygame.image.load("Select_2.png").convert_alpha()        # NOT EFFICIENT SRY, i just started with one and ended up copying and pasting
        screen.blit(select_2,(450,200))
        select_3 = pygame.image.load("Select_3.png").convert_alpha()
        screen.blit(select_3,(850,200))
        button_1_1 = pygame.image.load("Button_1.png").convert_alpha()
        screen.blit(button_1_1,(80,310))
        button_1_2 = pygame.image.load("Button_2.png").convert_alpha()
        screen.blit(button_1_2,(170,310))
        button_1_3 = pygame.image.load("Button_3.png").convert_alpha()
        screen.blit(button_1_3,(255,310))
        button_2_1 = pygame.image.load("Button_1.png").convert_alpha()
        screen.blit(button_2_1,(480,310))
        button_2_2 = pygame.image.load("Button_2.png").convert_alpha()
        screen.blit(button_2_2,(570,310))
        button_2_3 = pygame.image.load("Button_3.png").convert_alpha()
        screen.blit(button_2_3,(655,310))
        button_3_1 = pygame.image.load("Button_1.png").convert_alpha()
        screen.blit(button_3_1,(880,310))
        button_3_2 = pygame.image.load("Button_2.png").convert_alpha()
        screen.blit(button_3_2,(970,310))
        button_3_3 = pygame.image.load("Button_3.png").convert_alpha()
        screen.blit(button_3_3,(1055,310))
        buttons = ["button_1_1","button_1_2","button_1_3","button_2_1","button_2_2","button_2_3","button_3_1","button_3_2","button_3_3"]
        
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                for button in buttons:      # goes through each button and checks
                    print(button)
                    if level_select(button,posn_of_click) != None:
                        (group,level) = level_select(button,posn_of_click)
                        current_screen = screen_list[group][level]      # changes to selected level
    
    elif current_screen == "1.1" and not Tutorial_1_1:
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        tut = pygame.image.load("Tutorial_1_1.png").convert_alpha()
        screen.blit(tut,(100,100))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tutorial_1_1 = True
    elif current_screen == "1.1":       # LEVEL 1
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        title = pygame.image.load("Level_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(110,50))
        cabin1 = Cabin([150,440])
        screen.blit(cabin1.image, cabin1.rect) 
        player = Player([150,455])
        screen.blit(player.image, player.rect)
        func_box = pygame.image.load("LFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        lock = pygame.image.load("Lock.png").convert_alpha()
        screen.blit(lock,(873,625))
        pygame.draw.rect(screen,[255,255,255],(800,450,250,5))
        m_slider.draw()
        line_1_1.draw()
        textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,500))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                x = posn_of_click[0]
                y = posn_of_click[1]
                if x > m_slider.x and x < m_slider.x + m_slider.w and y > m_slider.y and y < m_slider.y+m_slider.h:
                    print("clicked")
                    # m_slider.update(x)
                    slider_moving = True
            if event.type == pygame.MOUSEBUTTONUP:
                slider_moving = False
        if slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            m_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,500))
            line_1_1.rotate(m_slider.value)


        





    for event in pygame.event.get():        # Checking for quit button
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() # Updating display with each iteration

pygame.quit()  # if quit button was pressed, run is now False so the while loop is exited and the game is stopped

