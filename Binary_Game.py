#!/usr/bin/env python3
# coding: utf-8

# In[1]:
import pygame
import os
from random import randint

# Add string to list
# one = False
# i = 0
# while one == False:
#     if s[i] == "1":
#         one = True
#         break
#     i += 1
# for c in s[i:]:
#     li.append(c)
    
#function to check if string contains 1's and 0's only
# def check_bin(string):
#     for i in string:
#         if i != '0' or i != '1':
#             print("Not a binary number")
#             return ""
#     return string
    
#recursive function that takes in arguments (string of binary number, length of string, current position, sum)
#returns int of decimal equivalent of binary
def bin_to_dec(li, n, s):
    #base condition
    if (n == 0):
        return s
    l = len(li)
    _sum = 0
    if li[n-1] == '1':
        _sum += (2**(l-n))
    return str(bin_to_dec(li, n-1, s + _sum))

# # prints out the binary value
# def printb(li):
#     string = ""
#     for i in li:
#         string += i
#     print("Binary: ", string)

# # prints out the decimal value
# def printd(li):
#     print("Decimal: ", bin_to_dec(li, len(li), 0))

# #shifts one bit to the right
# def right_shift(li):  
#     del li[-1]
#     if not li:
#         li.append("0")

# # shifts one bit to the left
# def left_shift(li):
#     if len(li) == 1 and li[0] == "0":
#         return
#     li.append("0")

#switches 1 and 0 in li
def switch_digit(index):
    num = li[index]
    if num == "0":
        li[index] = "1"
    elif num == "1":
        li[index] = "0"

# function to print text s with alignment (r or l) at position (x, y) on screen
def print_text(s, text_color, bg_color,size, screen, x, y, side):
    #create font object
    font = pygame.font.Font('freesansbold.ttf', size)
    #create text surface object
    text = font.render(s, True, text_color, bg_color)
    #create rect object for text surface object
    textRect = text.get_rect()
    if side == "r":
        textRect.bottomright = (x,y)
    elif side == "l":
        textRect.bottomleft = (x,y)
    elif side == "c":
        textRect.center = (x,y)

    # print onto screen
    screen.blit(text, textRect)
    
def print_question(num, text_color, bg_color ,screen):
    s = "make: " + num
    x = WIDTH/2
    y = 150
    # print_text(s, black, 30, screen, x, y, "l")
    # #create font object
    font = pygame.font.Font('freesansbold.ttf', 30)
    #create text surface object
    text = font.render(s, True, text_color, bg_color)
    #create rect object for text surface object
    textRect = text.get_rect()
    textRect.center = (x,y) 
    #print onto screen
    screen.blit(text, textRect)

# colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (240, 240, 240)
green = (0, 255, 0)

# record high score
# f = open("high_score.txt", "w")
# print(os.path.isfile("high_score.txt"))
# def write_hs(new_score):
#     hs = 

#initialize pygame
pygame.init()

page = "menu" # menu, instructions, easy_mode, hard_mode, end_screen, calculator, 

#initialize list to 16 "0"s
li = []  #list that stores binary digits
# for i in range(8):
#     li.append("0")

# dimensions
BORDER_W = 50
WIDTH = 800 + 2*BORDER_W
HEIGHT = 500

# set up drawing window
screen = pygame.display.set_mode([WIDTH,HEIGHT])

# folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'sprites')

# images
img_zero = pygame.image.load(os.path.join(img_folder, 'zero.png'))
img_one = pygame.image.load(os.path.join(img_folder, 'one.png'))

# ------------ class declarations ------------
class Digit(pygame.sprite.Sprite):
    def __init__(self, num, index, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_zero
        self.rect = self.image.get_rect()
        self.num = num
        self.index = index
        self.rect.left = x
        self.rect.top = y
 
    def set_image(self, i):
        self.image = i

    def update(self):
        self.num = li[self.index]
        if self.num == "0":
            self.image = img_zero
        elif self.num == "1":
            self.image = img_one

class Button:
    def __init__(self, s, position, size, link):
        #create font object
        self.name = s
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.bg_color = grey
        #create text surface object
        self.text = self.font.render(s, True, black, self.bg_color)
        #create rect object for text surface object
        self.textRect = self.text.get_rect()
        self.textRect.center = position
        self.size = size
        self.position = position
        self.link = link

        self.button_surface = pygame.Surface(size)
        self.button_surface.fill(self.bg_color)
        self.rect = self.button_surface.get_rect()
        self.rect.center = position

    def draw(self, screen):
        screen.blit(self.button_surface, self.rect)
        screen.blit(self.text, self.textRect)
# --------------------------------------------

# # create digit sprites group and add Digit objects
digit_sprites = pygame.sprite.Group()
separation = 4          # distance between digits

# create button sprites group and add Button objects
button_sprites = []
def set_objects(page):
    global button_sprites
    global digit_sprites
    button_sprites.clear()
    for sprite in digit_sprites:
        sprite.kill()
    if page == "menu":
        button_sprites.append(Button("Easy", (WIDTH/2, HEIGHT/2+40), (150,40), "easy_mode"))
        button_sprites.append(Button("Hard", (WIDTH/2, HEIGHT/2+90), (150,40), "hard_mode"))
    elif page == "easy_mode" or page == "hard_mode" or page == "end_screen":
        button_sprites.append(Button("Menu", (85, HEIGHT-30), (150,40), "menu"))

# clock
clock = pygame.time.Clock()
FPS = 30
time = 2            # seconds
time_left = time   
frame = 0           # for timer
def bonus_time(d):
    if d == "easy_mode":
        return int(5)
    elif d == "hard_mode":
        return int(15)

dp_time = 2*FPS     # how long to display bonus time for
frame1 = dp_time    # for bonus time

# generate random number
new_randn = True
maxn = 0
currn = 0
samen = 0

correct = False
score_added = False
score = 0

def reset():
    global time_left
    global time
    global correct
    global score_added
    global score
    global currn
    global samen
    time_left = time
    correct = False
    score_added = False
    score = 0
    while currn == samen:
        currn = str(randint(0,maxn))
    samen = currn

# game loop
running = True
set_objects("menu")
while running:
    pygame.display.set_caption('Binary Game ' + str(WIDTH) + "x" + str(HEIGHT))
    mouse = pygame.mouse.get_pos()

    # ------------- Menu -------------
    if page == "menu":
        bg_color = white

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                for button in button_sprites:
                    left = button.rect.left
                    right = left + button.rect.width
                    top = button.rect.top
                    bottom = top + button.rect.height
                    if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom): # is mouse over button
                        diff = 0
                        if button.link == "easy_mode":
                            diff = 8
                        elif button.link == "hard_mode":
                            diff = 16

                        digits_width = (diff * img_zero.get_width()) + (diff-1) * separation
                        digit_x = WIDTH/2 - digits_width/2 
                        digit_y = HEIGHT/2 - 60

                        maxn = (2**diff) - 1
                        currn = str(randint(1,maxn))
                        samen = currn

                        li.clear()
                        set_objects(button.link)
                        for i in range(diff):
                            li.append("0")
                            new_digit = Digit(li[i], i, digit_x, digit_y)
                            digit_sprites.add(new_digit)
                            digit_x += new_digit.image.get_width() + separation
                        
                        reset()
                        page = button.link
        
        #print background 
        screen.fill(bg_color)
        print_text("Binary Game", black, bg_color, 100, screen, WIDTH/2, HEIGHT/2 - 100, "c")

    # ------------- Easy/Hard Mode -------------
    elif page == "easy_mode" or page == "hard_mode":
        bg_color = white

        # timer
        if time_left < 0:
            page = "end_screen"
        if frame == FPS:
            frame = 0
            time_left -= 1
        frame += 1

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                # if correct answer, go to next question
                if correct:
                    correct = False
                    frame1 = 0

                    bt = bonus_time(page)
                    time_left += bt
                    score_added = False
                    while currn == samen:
                        currn = str(randint(0,maxn))
                    samen = currn

                    # set all digits to 0
                    for i in range(len(li)):
                        li[i] = "0"
                    for _digit in digit_sprites:
                        _digit.update()

                else:  # check for any buttons pressed
                    for _digit in digit_sprites:
                        left = _digit.rect.left
                        right = left + _digit.rect.width
                        top = _digit.rect.top
                        bottom = top + _digit.rect.height
                        if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom): # is mouse over digit
                            switch_digit(_digit.index)
                            _digit.update()
                    
                    for button in button_sprites:
                        left = button.rect.left
                        right = left + button.rect.width
                        top = button.rect.top
                        bottom = top + button.rect.height
                        if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom): # is mouse over button
                            if button.link == "menu":
                                set_objects("menu")
                                page = "menu"

        ans = bin_to_dec(li, len(li), 0)
        
        # Draw background, print text
        if ans == currn:
            correct = True 
            bg_color = green
            if not score_added:
                score += 1
                score_added = True
        screen.fill(bg_color)
        print_text("Score: " + str(score), black, bg_color, 30, screen, 15, 40, "l")
        if time_left >= 0:
            print_text("Time: " + str(time_left), black, bg_color, 30, screen, WIDTH-140, 40, "l")
        print_question(currn, black, bg_color, screen)
        print_text(ans, black, bg_color, 80, screen, WIDTH/2, HEIGHT-70, "c")

        if frame1 < (dp_time):
            print_text("+" + str(bt), green, bg_color, 30, screen, WIDTH-53, 70, "l")
            frame1 += 1

        # render sprites
        digit_sprites.draw(screen)

    # ------------- End Screen -------------
    elif page == "end_screen":
        pygame.display.set_caption('Binary Game ' + str(WIDTH) + "x" + str(HEIGHT))
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_sprites:
                    left = button.rect.left
                    right = left + button.rect.width
                    top = button.rect.top
                    bottom = top + button.rect.height
                    if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom): # is mouse over button
                        set_objects(button.link)
                        page = button.link
                

        # print background
        screen.fill(white)

        # print score
        print_text("Score: " + str(score), black, white, 90, screen, WIDTH/2, HEIGHT/2, "c")

    for button in button_sprites:   #print buttons
        button.draw(screen)
    # Flip the display
    pygame.display.flip()
    clock.tick(FPS)

f.close()
# Done! Time to quit.
pygame.quit()