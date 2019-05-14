import pygame
import sys
import math
import numpy

# define some colors in the RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

group_1 = ["1.1","1.2","1.3"]       # Level Titles
group_2 = ["2.1","2.2","2.3"]
group_3 = ["3.1","3.2","3.3"]

screen_list = ["Title","Select",group_1,group_2,group_3]       # Screen List

######### LEVELS ########

current_screen = screen_list[2][0]   # Starting screen, adjust to work on specific screen at startup

##### TUTORIALS - shows if level has been entered and tutorial has been shown yet
Tutorial_1_1 = False
Tutorial_1_2 = False
Tutorial_2_1 = False
Tutorial_2_3 = False
Tutorial_3_1 = False
Tutorial_3_3 = False

hitYeti = False

# set up pygame and its screen
pygame.init()
screen = pygame.display.set_mode((1200,1200))       # sets display size
pygame.display.set_caption("AVALANCHE")     # Title

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Arial', 30)
myfont2 = pygame.font.SysFont('Arial',20) ## font for squared display in quadratics


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

###### title page setup
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
        self.x = location[0]
        self.y = location[1]
        a = 305 + 77*self.x
        b = 460 - 77*self.y
        self.rect.left, self.rect.top = a,b
        self.xpoints = []
        self.ypoints = []
    def line_animate(self,m,b,cx,cy):
        self.xpoints = numpy.linspace(self.x,cx,10)
        self.ypoints = []
        for x in self.xpoints:
            self.ypoints.append(m*x+b)
    def quad_animate(self,a,b,c,cx,cy):
        self.xpoints = numpy.linspace(self.x,cx,10)
        self.ypoints = []
        for x in self.xpoints:
            self.ypoints.append(a*(x**2)+(b*x)+c)
    def sine_animate(self,a,b,c,cx,cy):
        self.xpoints = numpy.linspace(self.x,cx,10)
        self.ypoints = []
        for x in self.xpoints:
            self.ypoints.append(a*math.sin(b*x+c))
    def new_spot(self,i,j):
        m = int(305 + 77*i)
        n = int(460 - 77*j)
        self.rect.left, self.rect.top = m,n
        print(self.rect)

class Cabin(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cabin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = location[0]
        self.y = location[1]
        a = 300 + 77*self.x
        b = 440 - 77*self.y
        self.rect.left, self.rect.top = a,b

class Flag(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Flag.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = location[0]
        self.y = location[1]
        a = 315 + 77*self.x
        b = 440 - 77*self.y
        self.rect.left, self.rect.top = a,b

class Yeti(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Yeti.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = location[0]
        self.y = location[1]
        a = 300 + 77*self.x
        b = 470 - 77*self.y
        self.rect.left, self.rect.top = a,b

class Slider(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.start = location[0]
        self.bar_start = self.start-110
        self.x = self.start
        self.y = location[1]
        self.bar_height = self.y+25
        self.w = 25
        self.h = 50
        self.value = 0.0
        self.moving = False
    def update(self,new_x):
        pygame.draw.rect(screen,[237,216,223],(self.x,self.y,self.w,self.h))
        if new_x-self.start>120:
            self.x = self.start+120
        elif new_x-self.start<-120:
            self.x = self.start-120
        else:
            self.x = new_x
        self.value = round((self.x-self.start)/20)/2
        self.x = self.value*40 + self.start
        self.draw()
    def draw(self):
        pygame.draw.rect(screen,[255,255,255],(self.bar_start,self.bar_height,245,5))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start,self.bar_height-10,5,25))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+20,self.bar_height-5,5,15))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+40,self.bar_height-10,5,25))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+60,self.bar_height-5,5,15))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+80,self.bar_height-10,5,25))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+100,self.bar_height-5,5,15))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+120,self.bar_height-10,5,25))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+140,self.bar_height-5,5,15))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+160,self.bar_height-10,5,25))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+180,self.bar_height-5,5,15))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+200,self.bar_height-10,5,25))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+220,self.bar_height-5,5,15))
        pygame.draw.rect(screen,[255,255,255],(self.bar_start+240,self.bar_height-10,5,25))
        self.image = pygame.draw.rect(screen,[255,0,0],(self.x,self.y,self.w,self.h))
    def reset(self):
        self.x = self.start
        self.value = 0.0

class Line(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 1200
        self.centerx = 350
        self.centery = 525
        self.x1 = self.centerx-self.length/2
        self.y1 = self.centery
        self.x2 = self.centerx+self.length/2
        self.y2 = self.centery
        point1 = (self.x1,self.y1)
        point2 = (self.x2,self.y2)
        self.points = [point1,point2]
        self.angle = 0
    def draw(self):
        self.image = pygame.draw.polygon(screen,[0,255,0],self.points,10)
    def line_adjust(self,slope=0,intercept=0):
        self.centery = 525 - intercept*77
        self.angle = math.atan(slope)
        self.x2 = self.length/2*math.cos(self.angle)+self.centerx
        self.y2 = -self.length/2*math.sin(self.angle)+self.centery
        self.x1 = -self.length/2*math.cos(self.angle)+self.centerx
        self.y1 = self.length/2*math.sin(self.angle)+self.centery
        point1 = (self.x1,self.y1)
        point2 = (self.x2,self.y2)
        self.points = [point1,point2]
        self.draw()
    def reset(self):
        self.x1 = self.centerx-self.length/2
        self.y1 = self.centery
        self.x2 = self.centerx+self.length/2
        self.y2 = self.centery
        point1 = (self.x1,self.y1)
        point2 = (self.x2,self.y2)
        self.points = [point1,point2]
        self.angle = 0

class Quadratic(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 200
        self.height = 200
        self.centerx = 350
        self.centery = 525
        self.xpoints = numpy.linspace(-5,5,100)
        self.ypoints = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.get_y()
        self.points = []
        for i in range(len(self.xpoints)):
            self.points.append((self.xpoints[i]*77+self.centerx,self.ypoints[i]*-77+self.centery))
    def draw(self):
        self.image = pygame.draw.lines(screen,[0,255,0],False,self.points,10)
    def get_y(self):
        self.ypoints = []
        for x in self.xpoints:
            self.ypoints.append(self.a*(x**2)+(self.b*x)+self.c)
    def quad_adjust(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
        self.get_y()
        self.points = []
        for i in range(len(self.xpoints)):
            self.points.append((self.xpoints[i]*77+self.centerx,self.ypoints[i]*-77+self.centery))
        self.draw()
    def reset(self):
        self.xpoints = numpy.linspace(-5,5,100)
        self.ypoints = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.get_y()
        self.points = []
        for i in range(len(self.xpoints)):
            self.points.append((self.xpoints[i]*77+self.centerx,self.ypoints[i]*-77+self.centery))

class Sine(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 200
        self.height = 200
        self.centerx = 350
        self.centery = 525
        self.xpoints = numpy.linspace(-5,5,100)
        self.ypoints = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.get_y()
        self.points = []
        for i in range(len(self.xpoints)):
            self.points.append((self.xpoints[i]*77+self.centerx,self.ypoints[i]*-77+self.centery))
    def draw(self):
        self.image = pygame.draw.lines(screen,[0,255,0],False,self.points,10)
    def get_y(self):
        self.ypoints = []
        for x in self.xpoints:
            self.ypoints.append(self.a*math.sin(self.b*x+self.c))
    def sine_adjust(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
        self.get_y()
        self.points = []
        for i in range(len(self.xpoints)):
            self.points.append((self.xpoints[i]*77+self.centerx,self.ypoints[i]*-77+self.centery))
        self.draw()
    def reset(self):
        self.xpoints = numpy.linspace(-5,5,100)
        self.ypoints = []
        self.a = 0
        self.b = 0
        self.c = 0
        self.get_y()
        self.points = []
        for i in range(len(self.xpoints)):
            self.points.append((self.xpoints[i]*77+self.centerx,self.ypoints[i]*-77+self.centery))

def linear_solver(m,b,px,py,fx,fy,cx,cy,yx,yy,max_score,level_index):
    score = 0
    if not py == (m*px)+b:
        text = "Not Valid Placement. Try Again!"
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(400,450))
    elif not cy == (m*cx)+b:
        text = "Player didn't arrive home. Try Again!"
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(350,450))
    else:
        if fy == (m*fx)+b:
            score += 1
            print("Yay +1!")
        if yy == (m*yx)+b:
            score -= 1
            print("Ouch -1")
        text = "Congratulations! You've completed the level!  Score:"+str(score)+"/"+str(max_score)
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(225,450))
    level_scores[level_index[0]][level_index[1]] = str(score)+"/"+str(max_score)
    print(level_scores)

def quad_solver(a,b,c,px,py,fx,fy,cx,cy,yx,yy,max_score,level_index):
    score = 0
    if not py == (a*(px**2))+(b*px)+c:
        text = "Not Valid Placement. Try Again!"
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(400,450))
    elif not cy == (a*(cx**2))+(b*cx)+c:
        text = "Player didn't arrive home. Try Again!"
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(350,450))
    else:
        if fy == (a*(fx**2))+(b*fx)+c:
            score += 1
            print("Yay +1!")
        if yy == (a*(yx**2))+(b*yx)+c:
            score -= 1
            print("Ouch -1")
        text = "Congratulations! You've completed the level!  Score:"+str(score)+"/"+str(max_score)
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(225,450))
    level_scores[level_index[0]][level_index[1]] = str(score)+"/"+str(max_score)
    print(level_scores)
    
def sine_solver(a,b,c,px,py,fx,fy,cx,cy,yx,yy,max_score,level_index):
    score = 0
    error = 10**-1
    if not abs(py - a*math.sin(b*px+c))<error:
        text = "Not Valid Placement. Try Again!"
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(400,450))
    elif not abs(cy - a*math.sin(b*cx+c))<error:
        text = "Player didn't arrive home. Try Again!"
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(350,450))
    else:
        print(fy)
        print(a*math.sin(b*fx+c))
        print(fy - a*math.sin(b*fx+c))
        if abs(fy - a*math.sin(b*fx+c))<error:
            score += 1
            
            print("Yay +1!")
        if abs(yy - a*math.sin(b*yx+c))<error:
            score -= 1
            print("Ouch -1")
        text = "Congratulations! You've completed the level!  Score:"+str(score)+"/"+str(max_score)
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface,(225,450))
    level_scores[level_index[0]][level_index[1]] = str(score)+"/"+str(max_score)

def line_animate(m,b,player,cabin):
    xpoints = numpy.linspace(player.x,cabin.x,100)
    # ypoints = []
    for x in xpoints:
        y = m*x+b
        player.x = x
        player.y = y
        a = 305 + 77*player.x
        b = 460 - 77*player.y
        player.rect.left, player.rect.top = a,b
        screen.blit(player.image, player.rect)
        pygame.time.delay(10)
    player.x = cabin.x
    player.y = cabin.y
    a = 305 + 77*player.x
    b = 460 - 77*player.y
    player.rect.left, player.rect.top = a,b
    screen.blit(player.image, player.rect)

##### SCORES
level_scores = [[0,0,0],[0,0,0],[0,0,0]]
# level_scores = [["1/1","0/1","-1/1"],["1/1","1/1","1/1"],["1/1","1/1","1/1"]]

##### Tracks whether the slider is in the process of moving and should continue updating
m_slider_moving = False
b_slider_moving = False
a_slider_moving = False
b2_slider_moving = False
c_slider_moving = False
submit_displaying = False

##### Initiates the 4 sliders used throughout the game, values are reset at level select
m_slider = Slider((915,425))
b_slider = Slider((915,625))
a_slider = Slider((915,380))
b2_slider = Slider((915,515))
c_slider = Slider((915,650))

##### Initializes graphs for each level
line_1_1 = Line()
line_1_2 = Line()
line_1_3 = Line()
quad_2_1 = Quadratic()
quad_2_2 = Quadratic()
quad_2_3 = Quadratic()
sine_3_1 = Sine()
sine_3_2 = Sine()
sine_3_3 = Sine()

##### Holds previous slider value to only change line if value of slider has changed
old_m_slider_val = 0
old_b_slider_val = 0
old_a_slider_val = 0
old_b2_slider_val = 0
old_c_slider_val = 0

index = 0

animated = False


run = True      # will continue to run until quit button hit, loop found farther down
while run:
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
                pos = pygame.mouse.get_pos()
                if start.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True


    elif current_screen == "Select":        # SELECT SCREEN
        animated = False
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)
        select_1 = pygame.image.load("Select_1.png").convert_alpha()        # inserts all button images
        screen.blit(select_1,(50,200))
        select_2 = pygame.image.load("Select_2.png").convert_alpha()        # NOT EFFICIENT SRY, i just started with one and ended up copying and pasting
        screen.blit(select_2,(450,200))
        select_3 = pygame.image.load("Select_3.png").convert_alpha()
        screen.blit(select_3,(850,200))

        buttons = ["Button_1.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png"]


        if level_scores[2][1] == "1/1" or level_scores[2][2]== "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_3.png"]
        elif level_scores[2][0] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_N.png"]
        elif level_scores[1][2] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_N.png","Button_N.png"]
        elif level_scores[1][1] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_3.png","Button_N.png","Button_N.png","Button_N.png"]
        elif level_scores[1][0] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_2.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png"]
        elif level_scores[0][2] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_1.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png"]
        elif level_scores[0][1] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_3.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png"]
        elif level_scores[0][0] == "1/1":
            buttons = ["Button_1.png","Button_2.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png"]
        else:
            buttons = ["Button_1.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png","Button_N.png"]

        if level_scores[0][2] == "1/1":
            button_1_4 = Button("Button_4.png",1,1)
            button_1_4.rect.topleft = [80,350]
            screen.blit(button_1_4.img,(80,395))
        if level_scores[1][2] == "1/1":
            button_2_4 = Button("Button_4.png",1,1)
            button_2_4.rect.topleft = [480,350]
            screen.blit(button_2_4.img,(480,395))
        if level_scores[2][2] == "1/1":
            button_3_4 = Button("Button_4.png",1,1)
            button_3_4.rect.topleft = [880,350]
            screen.blit(button_3_4.img,(879,392))


        button_1_1 = Button(buttons[0],1,1)
        button_1_1.rect.topleft = [80,310]
        screen.blit(button_1_1.img,(80,310))
        button_1_2 = Button(buttons[1],1,2)
        button_1_2.rect.topleft = [170,310]
        screen.blit(button_1_2.img,(170,310))
        button_1_3 = Button(buttons[2],1,3)
        button_1_3.rect.topleft = [255,310]
        screen.blit(button_1_3.img,(255,310))
        button_2_1 = Button(buttons[3],2,1)
        button_2_1.rect.topleft = [480,310]
        screen.blit(button_2_1.img,(480,310))
        button_2_2 = Button(buttons[4],2,2)
        button_2_2.rect.topleft = [570,310]
        screen.blit(button_2_2.img,(570,310))
        button_2_3 = Button(buttons[5],2,3)
        button_2_3.rect.topleft = [655,310]
        screen.blit(button_2_3.img,(655,310))
        button_3_1 = Button(buttons[6],3,1)
        button_3_1.rect.topleft = [880,310]
        screen.blit(button_3_1.img,(880,310))
        button_3_2 = Button(buttons[7],3,2)
        button_3_2.rect.topleft = [970,310]
        screen.blit(button_3_2.img,(970,310))
        button_3_3 = Button(buttons[8],3,3)
        button_3_3.rect.topleft = [1055,310]
        screen.blit(button_3_3.img,(1055,310))
        buttons = [button_1_1,button_1_2,button_1_3,button_2_1,button_2_2,button_2_3,button_3_1,button_3_2,button_3_3]
        m_slider = Slider((915,425))
        b_slider = Slider((915,625))
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
        
        ### Resets all values before entering any levels
        m_slider.reset()
        b_slider.reset()
        a_slider.reset()
        b2_slider.reset()
        c_slider.reset()
        old_m_slider_val = 0.0
        old_b_slider_val = 0.0
        old_a_slider_val = 0.0
        old_b2_slider_val = 0.0
        old_c_slider_val = 0.0
        line_1_1.reset()
        line_1_2.reset()
        line_1_3.reset()
        quad_2_1.reset()
        quad_2_2.reset()
        quad_2_3.reset()
        sine_3_1.reset()
        sine_3_2.reset()
        sine_3_3.reset()

        if level_scores[0][0] != 0:
            text = "Level 1: "+level_scores[0][0]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(120,650))
        if level_scores[0][1] != 0:
            text = "Level 2: "+level_scores[0][1]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(120,700))
        if level_scores[0][2] != 0:
            text = "Level 3: "+level_scores[0][2]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(120,750))

        if level_scores[1][0] != 0:
            text = "Level 1: "+level_scores[1][0]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(520,650))
        if level_scores[1][1] != 0:
            text = "Level 2: "+level_scores[1][1]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(520,700))
        if level_scores[1][2] != 0:
            text = "Level 3: "+level_scores[1][2]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(520,750))

        if level_scores[2][0] != 0:
            text = "Level 1: "+level_scores[2][0]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(920,650))
        if level_scores[2][1] != 0:
            text = "Level 2: "+level_scores[2][1]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(920,700))
        if level_scores[2][2] != 0:
            text = "Level 3: "+level_scores[2][2]
            textsurface = myfont.render(text, False, (0, 0, 0))
            screen.blit(textsurface,(920,750))
        
        
        
        # textsurface = myfont.render(str(level_scores), False, (0, 0, 0))
        # screen.blit(textsurface,(400,800))


    ##### LEVEL 1.1 #####
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
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        line_1_1.draw()
        cabin = Cabin([2,2])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([0,0])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([2,0])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-2,-2])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(235,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("LFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        lock = pygame.image.load("Lock.png").convert_alpha()
        screen.blit(lock,(873,625))
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        m_slider.draw()
        textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,500))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(450,162))
        m_display = myfont.render(str(m_slider.value),False,(255,255,0))
        screen.blit(m_display,(500,162))
        text = myfont.render("x +",False, (0,0,0))
        screen.blit(text,(565,162))
        b_display = myfont.render(str(b_slider.value),False,(255,255,0))
        screen.blit(b_display,(620,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > m_slider.x and x < m_slider.x + m_slider.w and y > m_slider.y and y < m_slider.y+m_slider.h:
                    # m_slider.update(x)
                    m_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                # submit_displaying = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.line_animate(m_slider.value,0,cabin.x,cabin.y)
            print(player.xpoints)
            print(len(player.xpoints))
            player.new_spot(player.xpoints[index],player.ypoints[index])
            if player.xpoints[index] == yeti.x and player.ypoints[index] == yeti.y:
                if not hitYeti:
                    yetiAngle = 0
                hitYeti = True

            if hitYeti:
                yetiAngle += 40
                rot_player = pygame.transform.rotate(player.image,yetiAngle)
                screen.blit(rot_player,player.rect)
                if yetiAngle >= 360:
                    hitYeti = False
                    animated = True
            else:
                screen.blit(player.image,player.rect)
                if index < len(player.xpoints)-1:
                    index += 1
                else:
                    animated = True
            print(player.rect)
        elif submit_displaying == True and animated:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,0,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,0])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if m_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            m_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,500))
            line_1_1.line_adjust(m_slider.value)
        
        m = m_slider.value
        b = 0
        if not submit_displaying:
            if (player.y==m*player.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if (cabin.y==m*cabin.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if (flag.y==m*flag.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if (yeti.y==m*yeti.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    ##### LEVEL 1.2 #####
    elif current_screen == "1.2" and not Tutorial_1_2:
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        tut = pygame.image.load("Tutorial_1_2.png").convert_alpha()
        screen.blit(tut,(100,100))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tutorial_1_2 = True
    elif current_screen == "1.2":       # LEVEL 1
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        line_1_2.draw()
        cabin = Cabin([2,-3])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([-1,0])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([2,0])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-2,1])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(235,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("LFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        m_slider.draw()
        b_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,500))
        textsurface = myfont.render(str(b_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(450,162))
        m_display = myfont.render(str(m_slider.value),False,(255,255,0))
        screen.blit(m_display,(500,162))
        text = myfont.render("x +",False, (0,0,0))
        screen.blit(text,(565,162))
        b_display = myfont.render(str(b_slider.value),False,(255,255,0))
        screen.blit(b_display,(620,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > m_slider.x and x < m_slider.x + m_slider.w and y > m_slider.y and y < m_slider.y+m_slider.h:
                    # m_slider.update(x)
                    m_slider_moving = True
                elif x > b_slider.x and x < b_slider.x + b_slider.w and y > b_slider.y and y < b_slider.y+b_slider.h:
                    # m_slider.update(x)
                    b_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                b_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.line_animate(m_slider.value,b_slider.value,cabin.x,cabin.y)
            print(player.xpoints)
            print(len(player.xpoints))
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            print(player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,b_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,1])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if m_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            m_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,500))
            if not m_slider.value == old_m_slider_val:
                line_1_2.line_adjust(m_slider.value,b_slider.value)
                old_m_slider_val = m_slider.value
        if b_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            b_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
            textsurface = myfont.render(str(b_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,700))
            if not b_slider.value == old_b_slider_val:
                line_1_2.line_adjust(m_slider.value,b_slider.value)
                old_b_slider_val = b_slider.value
        
        m = m_slider.value
        b = b_slider.value
        if not submit_displaying:
            if (player.y==m*player.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if (cabin.y==m*cabin.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if (flag.y==m*flag.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if (yeti.y==m*yeti.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    ##### LEVEL 1.3 #####
    elif current_screen == "1.3":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        line_1_3.draw()
        cabin = Cabin([1,2])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([0,-1])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([2,0])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-0.5,-2.5])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(235,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("LFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        m_slider.draw()
        b_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,500))
        textsurface = myfont.render(str(b_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(450,162))
        m_display = myfont.render(str(m_slider.value),False,(255,255,0))
        screen.blit(m_display,(500,162))
        text = myfont.render("x +",False, (0,0,0))
        screen.blit(text,(565,162))
        b_display = myfont.render(str(b_slider.value),False,(255,255,0))
        screen.blit(b_display,(620,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > m_slider.x and x < m_slider.x + m_slider.w and y > m_slider.y and y < m_slider.y+m_slider.h:
                    # m_slider.update(x)
                    m_slider_moving = True
                elif x > b_slider.x and x < b_slider.x + b_slider.w and y > b_slider.y and y < b_slider.y+b_slider.h:
                    # m_slider.update(x)
                    b_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                b_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.line_animate(m_slider.value,b_slider.value,cabin.x,cabin.y)
            print(player.xpoints)
            print(len(player.xpoints))
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            print(player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,b_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,2])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if m_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            m_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,500))
            if not m_slider.value == old_m_slider_val:
                line_1_3.line_adjust(m_slider.value,b_slider.value)
                old_m_slider_val = m_slider.value
        if b_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            b_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
            textsurface = myfont.render(str(b_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,700))
            if not b_slider.value == old_b_slider_val:
                line_1_3.line_adjust(m_slider.value,b_slider.value)
                old_b_slider_val = b_slider.value

        m = m_slider.value
        b = b_slider.value
        if not submit_displaying:
            if (player.y==m*player.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if (cabin.y==m*cabin.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if (flag.y==m*flag.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if (yeti.y==m*yeti.x+b)==True:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)
    
    ##### LEVEL 2.1 #####
    elif current_screen == "2.1" and not Tutorial_2_1:
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        tut = pygame.image.load("Tutorial_2_1.png").convert_alpha()
        screen.blit(tut,(100,100))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tutorial_2_1 = True
    elif current_screen == "2.1":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        quad_2_1.draw()
        cabin = Cabin([2,3])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([0,-1])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([2,0])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-1,0])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_2_Title.png").convert_alpha()  # Title
        screen.blit(title,(400,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("QFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        lock = pygame.image.load("Lock.png").convert_alpha()
        screen.blit(lock,(873,525))
        a_slider.draw()
        # b2_slider.draw()
        c_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,430))
        # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        # screen.blit(textsurface,(800,565))
        textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(400,162))
        m_display = myfont.render(str(a_slider.value),False,(255,255,0))
        screen.blit(m_display,(450,162))
        text = myfont.render("x  +",False, (0,0,0))
        screen.blit(text,(515,162))
        squared = myfont2.render(str(2),False,(0,0,0))
        screen.blit(squared,(532,155))
        b_display = myfont.render(str(b2_slider.value),False,(255,255,0))
        screen.blit(b_display,(580,162))
        text = myfont.render("x  +",False, (0,0,0))
        screen.blit(text,(655,162))
        c_display = myfont.render(str(c_slider.value),False,(255,255,0))
        screen.blit(c_display,(720,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > a_slider.x and x < a_slider.x + a_slider.w and y > a_slider.y and y < a_slider.y+a_slider.h:
                    # m_slider.update(x)
                    a_slider_moving = True
                # elif x > b2_slider.x and x < b2_slider.x + b2_slider.w and y > b2_slider.y and y < b2_slider.y+b2_slider.h:
                #     # m_slider.update(x)
                #     b2_slider_moving = True
                elif x > c_slider.x and x < c_slider.x + c_slider.w and y > c_slider.y and y < c_slider.y+c_slider.h:
                    # m_slider.update(x)
                    c_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                a_slider_moving = False
                # b2_slider_moving = False
                c_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.quad_animate(a_slider.value,0,c_slider.value,cabin.x,cabin.y)
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            quad_solver(a_slider.value,0,c_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[1,0])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if a_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            a_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not a_slider.value == old_a_slider_val:
                quad_2_1.quad_adjust(a_slider.value,0,c_slider.value)
                old_a_slider_val = a_slider.value
        # if b2_slider_moving == True:
        #     pos = pygame.mouse.get_pos()
        #     x = pos[0]
        #     b2_slider.update(x)
        #     # pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
        #     # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        #     # screen.blit(textsurface,(800,700))
        #     if not b2_slider.value == old_b2_slider_val:
        #         quad_2_1.quad_adjust(a_slider.value,b2_slider.value,c_slider.value)
        #         old_b2slider_val = b2_slider.value
        if c_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            c_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not c_slider.value == old_c_slider_val:
                quad_2_1.quad_adjust(a_slider.value,0,c_slider.value)
                old_c_slider_val = c_slider.value
        
        a = a_slider.value
        b = 0
        c = c_slider.value
        if not submit_displaying:
            if (player.y==a*(player.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if (cabin.y==a*(cabin.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if (flag.y==a*(flag.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if (yeti.y==a*(yeti.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    ##### LEVEL 2.2 #####            
    elif current_screen == "2.2":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        quad_2_2.draw()
        cabin = Cabin([2,-1])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([1,2])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([0,-1])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-2,-1])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_2_Title.png").convert_alpha()  # Title
        screen.blit(title,(400,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("QFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        lock = pygame.image.load("Lock.png").convert_alpha()
        screen.blit(lock,(873,525))
        a_slider.draw()
        # b2_slider.draw()
        c_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,430))
        # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        # screen.blit(textsurface,(800,565))
        textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(400,162))
        m_display = myfont.render(str(a_slider.value),False,(255,255,0))
        screen.blit(m_display,(450,162))
        text = myfont.render("x  +",False, (0,0,0))
        screen.blit(text,(515,162))
        squared = myfont2.render(str(2),False,(0,0,0))
        screen.blit(squared,(532,155))
        b_display = myfont.render(str(b2_slider.value),False,(255,255,0))
        screen.blit(b_display,(580,162))
        text = myfont.render("x  +",False, (0,0,0))
        screen.blit(text,(655,162))
        c_display = myfont.render(str(c_slider.value),False,(255,255,0))
        screen.blit(c_display,(720,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > a_slider.x and x < a_slider.x + a_slider.w and y > a_slider.y and y < a_slider.y+a_slider.h:
                    # m_slider.update(x)
                    a_slider_moving = True
                # elif x > b2_slider.x and x < b2_slider.x + b2_slider.w and y > b2_slider.y and y < b2_slider.y+b2_slider.h:
                #     # m_slider.update(x)
                #     b2_slider_moving = True
                elif x > c_slider.x and x < c_slider.x + c_slider.w and y > c_slider.y and y < c_slider.y+c_slider.h:
                    # m_slider.update(x)
                    c_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                a_slider_moving = False
                # b2_slider_moving = False
                c_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.quad_animate(a_slider.value,0,c_slider.value,cabin.x,cabin.y)
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            quad_solver(a_slider.value,0,c_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[1,1])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if a_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            a_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not a_slider.value == old_a_slider_val:
                quad_2_2.quad_adjust(a_slider.value,0,c_slider.value)
                old_a_slider_val = a_slider.value
        # if b2_slider_moving == True:
        #     pos = pygame.mouse.get_pos()
        #     x = pos[0]
        #     b2_slider.update(x)
        #     # pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
        #     # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        #     # screen.blit(textsurface,(800,700))
        #     if not b2_slider.value == old_b2_slider_val:
        #         quad_2_1.quad_adjust(a_slider.value,b2_slider.value,c_slider.value)
        #         old_b2slider_val = b2_slider.value
        if c_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            c_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not c_slider.value == old_c_slider_val:
                quad_2_2.quad_adjust(a_slider.value,0,c_slider.value)
                old_c_slider_val = c_slider.value
        
        a = a_slider.value
        b = 0
        c = c_slider.value
        if not submit_displaying:
            if (player.y==a*(player.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if (cabin.y==a*(cabin.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if (flag.y==a*(flag.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if (yeti.y==a*(yeti.x**2)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    ##### LEVEL 2.3 #####
    elif current_screen == "2.3" and not Tutorial_2_3:
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        tut = pygame.image.load("Tutorial_2_3.png").convert_alpha()
        screen.blit(tut,(100,100))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tutorial_2_3 = True
    elif current_screen == "2.3":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        quad_2_3.draw()
        cabin = Cabin([3,3])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([1,-1])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([1,1])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-1,3])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_2_Title.png").convert_alpha()  # Title
        screen.blit(title,(400,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("QFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        a_slider.draw()
        b2_slider.draw()
        c_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,430))
        textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,565))
        textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(400,162))
        m_display = myfont.render(str(a_slider.value),False,(255,255,0))
        screen.blit(m_display,(450,162))
        text = myfont.render("x  +",False, (0,0,0))
        screen.blit(text,(515,162))
        squared = myfont2.render(str(2),False,(0,0,0))
        screen.blit(squared,(532,155))
        b_display = myfont.render(str(b2_slider.value),False,(255,255,0))
        screen.blit(b_display,(580,162))
        text = myfont.render("x  +",False, (0,0,0))
        screen.blit(text,(655,162))
        c_display = myfont.render(str(c_slider.value),False,(255,255,0))
        screen.blit(c_display,(720,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > a_slider.x and x < a_slider.x + a_slider.w and y > a_slider.y and y < a_slider.y+a_slider.h:
                    # m_slider.update(x)
                    a_slider_moving = True
                elif x > b2_slider.x and x < b2_slider.x + b2_slider.w and y > b2_slider.y and y < b2_slider.y+b2_slider.h:
                    # m_slider.update(x)
                    b2_slider_moving = True
                elif x > c_slider.x and x < c_slider.x + c_slider.w and y > c_slider.y and y < c_slider.y+c_slider.h:
                    # m_slider.update(x)
                    c_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                a_slider_moving = False
                b2_slider_moving = False
                c_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.quad_animate(a_slider.value,b2_slider.value,c_slider.value,cabin.x,cabin.y)
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            quad_solver(a_slider.value,b2_slider.value,c_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[1,2])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if a_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            a_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not a_slider.value == old_a_slider_val:
                quad_2_3.quad_adjust(a_slider.value,b2_slider.value,c_slider.value)
                old_a_slider_val = a_slider.value
        if b2_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            b2_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
            # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,700))
            if not b2_slider.value == old_b2_slider_val:
                quad_2_3.quad_adjust(a_slider.value,b2_slider.value,c_slider.value)
                old_b2slider_val = b2_slider.value
        if c_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            c_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not c_slider.value == old_c_slider_val:
                quad_2_3.quad_adjust(a_slider.value,b2_slider.value,c_slider.value)
                old_c_slider_val = c_slider.value
        
        a = a_slider.value
        b = b2_slider.value
        c = c_slider.value
        if not submit_displaying:
            if (player.y==a*(player.x**2)+(b*player.x)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if (cabin.y==a*(cabin.x**2)+(b*cabin.x)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if (flag.y==a*(flag.x**2)+(b*flag.x)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if (yeti.y==a*(yeti.x**2)+(b*yeti.x)+c)==True:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)
    
    ##### LEVEL 3.1 #####
    elif current_screen == "3.1" and not Tutorial_3_1:
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        tut = pygame.image.load("Tutorial_3_1.png").convert_alpha()
        screen.blit(tut,(100,100))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tutorial_3_1 = True
    elif current_screen == "3.1":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        sine_3_1.draw()
        cabin = Cabin([3,-1])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([0,0])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([1,-2])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([-3,1])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_3_Title.png").convert_alpha()  # Title
        screen.blit(title,(325,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("SFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        lock = pygame.image.load("Lock.png").convert_alpha()
        screen.blit(lock,(873,660))
        a_slider.draw()
        b2_slider.draw()
        # c_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,430))
        textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,565))
        textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(400,162))
        m_display = myfont.render(str(a_slider.value),False,(255,255,0))
        screen.blit(m_display,(450,162))
        text = myfont.render("sin(",False, (0,0,0))
        screen.blit(text,(515,162))
        b_display = myfont.render(str(b2_slider.value),False,(255,255,0))
        screen.blit(b_display,(580,162))
        text = myfont.render("x +",False, (0,0,0))
        screen.blit(text,(655,162))
        c_display = myfont.render(str(c_slider.value),False,(255,255,0))
        screen.blit(c_display,(700,162))
        text = myfont.render(")",False,(0,0,0))
        screen.blit(text,(760,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > a_slider.x and x < a_slider.x + a_slider.w and y > a_slider.y and y < a_slider.y+a_slider.h:
                    # m_slider.update(x)
                    a_slider_moving = True
                elif x > b2_slider.x and x < b2_slider.x + b2_slider.w and y > b2_slider.y and y < b2_slider.y+b2_slider.h:
                    # m_slider.update(x)
                    b2_slider_moving = True
                # elif x > c_slider.x and x < c_slider.x + c_slider.w and y > c_slider.y and y < c_slider.y+c_slider.h:
                #     # m_slider.update(x)
                #     c_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                    index = 0
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                a_slider_moving = False
                b2_slider_moving = False
                # c_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.sine_animate(a_slider.value,b2_slider.value,0,cabin.x,cabin.y)
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            sine_solver(a_slider.value,b2_slider.value,0,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[2,0])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if a_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            a_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not a_slider.value == old_a_slider_val:
                sine_3_1.sine_adjust(a_slider.value,b2_slider.value,0)
                old_a_slider_val = a_slider.value
        if b2_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            b2_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
            # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,700))
            if not b2_slider.value == old_b2_slider_val:
                sine_3_1.sine_adjust(a_slider.value,b2_slider.value,0)
                old_b2slider_val = b2_slider.value
        # if c_slider_moving == True:
        #     pos = pygame.mouse.get_pos()
        #     x = pos[0]
        #     c_slider.update(x)
        #     # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
        #     # textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        #     # screen.blit(textsurface,(800,500))
        #     if not c_slider.value == old_c_slider_val:
        #         sine_3_1.sine_adjust(a_slider.value,b2_slider.value,c_slider.value)
        #         old_c_slider_val = c_slider.value

        a = a_slider.value
        b = b2_slider.value
        c = 0
        error = 10**-1
        if not submit_displaying:
            if abs(player.y - (a*math.sin(b*player.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if abs(cabin.y - (a*math.sin(b*cabin.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if abs(flag.y - (a*math.sin(b*flag.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if abs(yeti.y - (a*math.sin(b*yeti.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    ##### LEVEL 3.2 #####
    elif current_screen == "3.2":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        sine_3_2.draw()
        cabin = Cabin([3,2])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([1,1])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([3,-2])
        screen.blit(yeti.image, yeti.rect)
        if not submit_displaying: 
            player = Player([-3,-2])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_2_Title.png").convert_alpha()  # Title
        screen.blit(title,(325,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("SFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        lock = pygame.image.load("Lock.png").convert_alpha()
        screen.blit(lock,(873,660))
        a_slider.draw()
        b2_slider.draw()
        # c_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,430))
        textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,565))
        textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(400,162))
        m_display = myfont.render(str(a_slider.value),False,(255,255,0))
        screen.blit(m_display,(450,162))
        text = myfont.render("sin(",False, (0,0,0))
        screen.blit(text,(515,162))
        b_display = myfont.render(str(b2_slider.value),False,(255,255,0))
        screen.blit(b_display,(580,162))
        text = myfont.render("x +",False, (0,0,0))
        screen.blit(text,(655,162))
        c_display = myfont.render(str(c_slider.value),False,(255,255,0))
        screen.blit(c_display,(700,162))
        text = myfont.render(")",False,(0,0,0))
        screen.blit(text,(760,162))

        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > a_slider.x and x < a_slider.x + a_slider.w and y > a_slider.y and y < a_slider.y+a_slider.h:
                    # m_slider.update(x)
                    a_slider_moving = True
                elif x > b2_slider.x and x < b2_slider.x + b2_slider.w and y > b2_slider.y and y < b2_slider.y+b2_slider.h:
                    # m_slider.update(x)
                    b2_slider_moving = True
                # elif x > c_slider.x and x < c_slider.x + c_slider.w and y > c_slider.y and y < c_slider.y+c_slider.h:
                #     # m_slider.update(x)
                #     c_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                a_slider_moving = False
                b2_slider_moving = False
                # c_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.sine_animate(a_slider.value,b2_slider.value,0,cabin.x,cabin.y)
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            sine_solver(a_slider.value,b2_slider.value,0,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[2,1])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if a_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            a_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not a_slider.value == old_a_slider_val:
                sine_3_2.sine_adjust(a_slider.value,b2_slider.value,0)
                old_a_slider_val = a_slider.value
        if b2_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            b2_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
            # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,700))
            if not b2_slider.value == old_b2_slider_val:
                sine_3_2.sine_adjust(a_slider.value,b2_slider.value,0)
                old_b2slider_val = b2_slider.value
        # if c_slider_moving == True:
        #     pos = pygame.mouse.get_pos()
        #     x = pos[0]
        #     c_slider.update(x)
        #     # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
        #     # textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        #     # screen.blit(textsurface,(800,500))
        #     if not c_slider.value == old_c_slider_val:
        #         sine_3_2.sine_adjust(a_slider.value,b2_slider.value,c_slider.value)
        #         old_c_slider_val = c_slider.value

        a = a_slider.value
        b = b2_slider.value
        c = 0
        error = 10**-1
        
        if not submit_displaying:
            if abs(player.y - (a*math.sin(b*player.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if abs(cabin.y - (a*math.sin(b*cabin.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if abs(flag.y - (a*math.sin(b*flag.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if abs(yeti.y - (a*math.sin(b*yeti.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    ##### LEVEL 3.3 #####
    elif current_screen == "3.3" and not Tutorial_3_3:
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        tut = pygame.image.load("Tutorial_3_3.png").convert_alpha()
        screen.blit(tut,(100,100))
        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tutorial_3_3 = True
    elif current_screen == "3.3":
        screen.fill([0,0,0])
        screen.blit(BackGround.image,BackGround.rect)       # Background
        pygame.draw.rect(screen,[237,216,223],(35,210,630,630))
        pygame.draw.rect(screen,[255,255,255],(40,215,620,620))
        grid = pygame.image.load("Grid.png").convert_alpha()        # Grid
        screen.blit(grid,(25,200))
        sine_3_3.draw()
        cabin = Cabin([2,2])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([1,0])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([3,-2])
        screen.blit(yeti.image, yeti.rect) 
        if not submit_displaying:
            player = Player([0,-2])
            screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_3_Title.png").convert_alpha()  # Title
        screen.blit(title,(325,50))
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load("Back_Button.png").convert_alpha()
        back.rect = back.image.get_rect()
        back.rect.topleft = [10,10]
        screen.blit(back.image,back.rect)
        func_box = pygame.image.load("SFunc_Box.png").convert_alpha()
        screen.blit(func_box,(700,200))
        a_slider.draw()
        b2_slider.draw()
        c_slider.draw()
        submit = pygame.sprite.Sprite()
        submit.image = pygame.image.load("Submit.png").convert_alpha()
        submit.rect = submit.image.get_rect()
        submit.rect.topleft = [805,775]
        screen.blit(submit.image,submit.rect)
        textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,430))
        textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,565))
        textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
        screen.blit(textsurface,(800,700))

        text = myfont.render("y = ",False,(0,0,0))
        screen.blit(text,(400,162))
        m_display = myfont.render(str(a_slider.value),False,(255,255,0))
        screen.blit(m_display,(450,162))
        text = myfont.render("sin(",False, (0,0,0))
        screen.blit(text,(515,162))
        b_display = myfont.render(str(b2_slider.value),False,(255,255,0))
        screen.blit(b_display,(580,162))
        text = myfont.render("x +",False, (0,0,0))
        screen.blit(text,(655,162))
        c_display = myfont.render(str(c_slider.value),False,(255,255,0))
        screen.blit(c_display,(700,162))
        text = myfont.render(")",False,(0,0,0))
        screen.blit(text,(760,162))


        x_button = pygame.sprite.Sprite()
        x_button.image = pygame.image.load("X_Button.png").convert_alpha()
        x_button.rect = x_button.image.get_rect()
        x_button.rect.topleft = [192,402]
        forward = pygame.sprite.Sprite()
        forward.image = pygame.image.load("Forward_Button.png").convert_alpha()
        forward.rect = forward.image.get_rect()
        forward.rect.topleft = [950,402]

        for event in pygame.event.get():        # checking for mouse click
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posn_of_click = event.dict["pos"]
                print(posn_of_click)
                x = posn_of_click[0]
                y = posn_of_click[1]
                pos = pygame.mouse.get_pos()
                if x > a_slider.x and x < a_slider.x + a_slider.w and y > a_slider.y and y < a_slider.y+a_slider.h:
                    # m_slider.update(x)
                    a_slider_moving = True
                elif x > b2_slider.x and x < b2_slider.x + b2_slider.w and y > b2_slider.y and y < b2_slider.y+b2_slider.h:
                    # m_slider.update(x)
                    b2_slider_moving = True
                elif x > c_slider.x and x < c_slider.x + c_slider.w and y > c_slider.y and y < c_slider.y+c_slider.h:
                    # m_slider.update(x)
                    c_slider_moving = True
                elif back.rect.collidepoint(pos):   # checks if button click is inside start button
                    current_screen = screen_list[1] # changes to Select screen if True
                elif submit.rect.collidepoint(pos):
                    submit_displaying = True
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    animated = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                a_slider_moving = False
                b2_slider_moving = False
                c_slider_moving = False
        if submit_displaying == True and not animated:
            # [86,115,186]
            print("entered")
            player.sine_animate(a_slider.value,b2_slider.value,c_slider.value,cabin.x,cabin.y)
            player.new_spot(player.xpoints[index],player.ypoints[index])
            screen.blit(player.image,player.rect)
            if index < len(player.xpoints)-1:
                index += 1
            else:
                animated = True
        elif submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            sine_solver(a_slider.value,b2_slider.value,c_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[2,2])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
            index = 0
        if a_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            a_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(a_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not a_slider.value == old_a_slider_val:
                sine_3_3.sine_adjust(a_slider.value,b2_slider.value,c_slider.value)
                old_a_slider_val = a_slider.value
        if b2_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            b2_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,700,50,50))
            # textsurface = myfont.render(str(b2_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,700))
            if not b2_slider.value == old_b2_slider_val:
                sine_3_3.sine_adjust(a_slider.value,b2_slider.value,c_slider.value)
                old_b2slider_val = b2_slider.value
        if c_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            c_slider.update(x)
            # pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            # textsurface = myfont.render(str(c_slider.value), False, (0, 0, 0))
            # screen.blit(textsurface,(800,500))
            if not c_slider.value == old_c_slider_val:
                sine_3_3.sine_adjust(a_slider.value,b2_slider.value,c_slider.value)
                old_c_slider_val = c_slider.value

        a = a_slider.value
        b = b2_slider.value
        c = c_slider.value
        error = 10**-1

        if not submit_displaying:
            if abs(player.y - (a*math.sin(b*player.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(player.x*77+353),int(player.y*-77+534)),7,0)
            if abs(cabin.y - (a*math.sin(b*cabin.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(cabin.x*77+348),int(cabin.y*-77+516)),7,0)
            if abs(flag.y - (a*math.sin(b*flag.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(flag.x*77+352),int(flag.y*-77+529)),7,0)
            if abs(yeti.y - (a*math.sin(b*yeti.x+c)))<error:
                pygame.draw.circle(screen,[255,255,0],(int(yeti.x*77+349),int(yeti.y*-77+525)),7,0)

    for event in pygame.event.get():        # Checking for quit button
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() # Updating display with each iteration

pygame.quit()  # if quit button was pressed, run is now False so the while loop is exited and the game is stopped
