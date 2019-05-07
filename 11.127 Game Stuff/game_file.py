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

current_screen = screen_list[0]      # Starting screen, adjust to work on specific screen at startup

    # set up pygame and its screen
pygame.init()
screen = pygame.display.set_mode((1920,1080))       # sets display size
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

class Button(pygame.sprite.Sprite):
    def __init__(self,image_file, group, level):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(image_file).convert_alpha()
        self.rect = self.img.get_rect()
        self.level = level
        self.group = group

BackGround = Background('Background.png', [0,0])
start = pygame.sprite.Sprite()
start.image = pygame.image.load("Start.png").convert_alpha()
start.rect = start.image.get_rect()
start.rect.topleft = [360,600]

def level_select(button,point):     # func for selecting level from start screen
    if button.rect.collidepoint(point):     # checks if point is within button space
        print("Group ",button.group," Level ",button.level)
        return (button.group+1,button.level-1)    # returns indices 
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
    def draw(self):
        self.image = pygame.draw.rect(screen,[255,0,0],(self.x,self.y,self.w,self.h))

class Line(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 50
        self.y = 519
        self.w = 630
        self.h = 10
    def draw(self):
        self.image = pygame.draw.rect(screen,[0,255,0],(self.x,self.y,self.w,self.h))
        # self.rect = self.image.get_rect()
    def rotate(self,angle):
        self.image = pygame.transform.rotate(screen,angle)
        # self.rect = self.image.get_rect()
        

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
                pos = pygame.mouse.get_pos();
                if start.rect.collidepoint(pos):   # checks if button click is inside start button
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
        button_1_1 = Button("Button_1.png",1,1)
        button_1_1.rect.topleft = [80,310]
        screen.blit(button_1_1.img,(80,310))
        button_1_2 = Button("Button_2.png",1,2)
        button_1_2.rect.topleft = [170,310]
        screen.blit(button_1_2.img,(170,310))
        button_1_3 = Button("Button_3.png",1,3)
        button_1_3.rect.topleft = [255,310]
        screen.blit(button_1_3.img,(255,310))
        button_2_1 = Button("Button_1.png",2,1)
        button_2_1.rect.topleft = [480,310]
        screen.blit(button_2_1.img,(480,310))
        button_2_2 = Button("Button_2.png",2,2)
        button_2_2.rect.topleft = [570,310]
        screen.blit(button_2_2.img,(570,310))
        button_2_3 = Button("Button_3.png",2,3)
        button_2_3.rect.topleft = [655,310]
        screen.blit(button_2_3.img,(655,310))
        button_3_1 = Button("Button_1.png",3,1)
        button_3_1.rect.topleft = [880,310]
        screen.blit(button_3_1.img,(880,310))
        button_3_2 = Button("Button_2.png",3,2)
        button_3_2.rect.topleft = [970,310]
        screen.blit(button_3_2.img,(970,310))
        button_3_3 = Button("Button_3.png",3,3)
        button_3_3.rect.topleft = [1055,310]
        screen.blit(button_3_3.img,(1055,310))
        buttons = [button_1_1,button_1_2,button_1_3,button_2_1,button_2_2,button_2_3,button_3_1,button_3_2,button_3_3]
        
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                for button in buttons:      # goes through each button and checks
                    selection = level_select(button,posn_of_click)
                    if selection != None:
                        (group,level) = selection
                        current_screen = screen_list[group][level]      # changes to selected level

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
            line_1_1.rotate(50)

    for event in pygame.event.get():        # Checking for quit button
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() # Updating display with each iteration

pygame.quit()  # if quit button was pressed, run is now False so the while loop is exited and the game is stopped

