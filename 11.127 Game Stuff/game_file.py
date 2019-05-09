import pygame
import sys
import math

# define some colors in the RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

group_1 = ["1.1","1.2","1.3"]       # Level Titles
group_2 = ["2.1","2.2","2.3"]
group_3 = ["3.1","3.2","3.3"]
free = ["4.1","4.2","4.3"]
screen_list = ["Title","Select",group_1,group_2,group_3,free]       # Screen List

######### LEVELS ########

current_screen = screen_list[0]     # Starting screen, adjust to work on specific screen at startup

Tutorial_1_1 = False
Tutorial_1_2 = False
Tutorial_2_1 = False
Tutorial_2_2 = False
Tutorial_3_1 = False
Tutorial_3_2 = False

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
        self.x = location[0]
        self.y = location[1]
        a = 305 + 77*self.x
        b = 460 - 77*self.y
        self.rect.left, self.rect.top = a,b

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
        self.value = 0
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

class Quadratic(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 200
        self.height = 200
        self.centerx = 350
        self.centery = 525
        self.x1 = -8
        self.x2 = -6
        self.x3 = -6
        self.x4 = -2
        self.x5 = 0
        self.x6 = 2
        self.x7 = 4
        self.x8 = 2

        # self.x1 = self.centerx + self.length/6*-3
        # self.x2 = self.centerx + self.length/6*-2
        # self.x3 = self.centerx + self.length/6*-1
        # self.x4 = self.centerx
        # self.x5 = self.centerx + self.length/6*3
        # self.x6 = self.centerx + self.length/6*2
        # self.x7 = self.centerx + self.length/6*1
        # self.a = 1
        # self.b = 1
        # self.c = 1
        # self.y1 = -self.a*((self.x1-self.centerx)**2)-(self.b*(self.x1-self.centerx))-self.c+self.centery
        # self.y2 = self.a*(self.x2**2)+(self.b*self.x2)+self.c
        # self.y3 = self.a*(self.x3**2)+(self.b*self.x3)+self.c
        # self.y4 = self.a*(self.x4**2)+(self.b*self.x4)+self.c
        # self.y5 = self.a*(self.x5**2)+(self.b*self.x5)+self.c
        # self.y6 = self.a*(self.x6**2)+(self.b*self.x6)+self.c
        # self.y7 = self.a*(self.x7**2)+(self.b*self.x7)+self.c
        # point1 = (self.x1,self.y1)
        # point2 = (self.x2,self.y2)
        # point3 = (self.x3,self.y3)
        # point4 = (self.x4,self.y4)
        # point5 = (self.x5,self.y5)
        # point6 = (self.x6,self.y6)
        # point7 = (self.x7,self.y7)
        point1 = (self.x1,self.y1)
        point2 = (300,400)
        point3 = (300,500)
        point4 = (200,400)
        point5 = (200,500)
        point6 = (200,600)
        point7 = (200,700)
        self.points = [point1,point2,point3,point4,point5,point6,point7]
    def draw(self):
        self.image = pygame.draw.lines(screen,[0,255,0],False,self.points,10)


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
    
level_scores = [[0,0,0],[0,0,0],[0,0,0]]

m_slider_moving = False
b_slider_moving = False
submit_displaying = False

m_slider = Slider((915,425))
b_slider = Slider((915,625))
line_1_1 = Line()
line_1_2 = Line()
line_1_3 = Line()
quad_2_1 = Quadratic()
old_m_slider_val = 0
old_b_slider_val = 0

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
                pos = pygame.mouse.get_pos()
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


    ##### LEVEL 1.1 ######
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
        player = Player([-2,-2])
        screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(110,50))
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
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                # submit_displaying = False
        if submit_displaying == True:
            # [86,115,186]
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,0,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,0])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
        if m_slider_moving == True:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            m_slider.update(x)
            pygame.draw.rect(screen,[237,216,223],(800,500,50,50))
            textsurface = myfont.render(str(m_slider.value), False, (0, 0, 0))
            screen.blit(textsurface,(800,500))
            line_1_1.line_adjust(m_slider.value)


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
        player = Player([-2,1])
        screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(110,50))
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
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                b_slider_moving = False
        if submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,b_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,1])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
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
        player = Player([-0.5,-2.5])
        screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(110,50))
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
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                b_slider_moving = False
        if submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,b_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,2])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
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
        cabin = Cabin([1,2])
        screen.blit(cabin.image, cabin.rect) 
        flag = Flag([0,-1])
        screen.blit(flag.image, flag.rect) 
        yeti = Yeti([2,0])
        screen.blit(yeti.image, yeti.rect) 
        player = Player([-0.5,-2.5])
        screen.blit(player.image, player.rect)
        cover = pygame.image.load("Background_Cover.png").convert_alpha()
        screen.blit(cover,(0,0))
        title = pygame.image.load("Group_1_Title.png").convert_alpha()  # Title
        screen.blit(title,(110,50))
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
                
                if x_button.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                elif forward.rect.collidepoint(pos) and submit_displaying:
                    submit_displaying = False
                    current_screen = screen_list[1]
            if event.type == pygame.MOUSEBUTTONUP:
                m_slider_moving = False
                b_slider_moving = False
        if submit_displaying == True:
            pygame.draw.rect(screen,[240,210,95],(190,400,810,130))
            linear_solver(m_slider.value,b_slider.value,player.x,player.y,flag.x,flag.y,cabin.x,cabin.y,yeti.x,yeti.y,1,[0,2])
            screen.blit(x_button.image,x_button.rect)
            screen.blit(forward.image,forward.rect)
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

    for event in pygame.event.get():        # Checking for quit button
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() # Updating display with each iteration

pygame.quit()  # if quit button was pressed, run is now False so the while loop is exited and the game is stopped

