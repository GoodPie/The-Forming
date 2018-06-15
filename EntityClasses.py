import pygame, sys, os, functions
from pygame.locals import *

#Main Entity Class
class Entity(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#The Player Class
class Player(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image_cache = image_cache
        self.pos_x = x
        self.pos_y = y
        self.in_shop = False
        self.image = functions.get_image("data/images/Character.png", self.image_cache)
        self.image.convert()
        self.rect = Rect(self.pos_x, self.pos_y, 32, 32)

    def update(self, up, down, left, right, position_check,
               obsticles, trees, level_width, level_height):
        if up:
            self.pos_y = -8
        elif down:
            self.pos_y = 8
        elif left:
            self.pos_x = -8
        elif right:
            self.pos_x = 8

        if not (up or down):
            self.pos_y = 0
        if not (left or right):
            self.pos_x = 0

        #Moving the character
        self.rect.left += self.pos_x
        self.rect.top += self.pos_y

        #Collision Detection and animations
        self.Collision_Test(level_width, level_height, trees, obsticles)

        if position_check:
            print "Player Pos: %s " % (self.rect)

    def Collision_Test(self, level_width, level_height, trees, obsticles):
        if self.rect.top < 0 :
            self.pos_y = 0
            self.rect.top = 0

        if self.rect.bottom > level_height:
            self.pos_y = 0
            self.rect.bottom = level_height

        if self.rect.left < 0:
            self.pos_x = 0
            self.rect.left = 0

        if self.rect.right > level_width:
            self.pos_x = 0
            self.rect.right = level_width

        for t in trees:
            if pygame.sprite.collide_rect(self, t):
                if self.pos_x > 0:
                    self.rect.right = t.rect.left
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_x < 0:
                    self.rect.left = t.rect.right
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y > 0:
                    self.rect.bottom = t.rect.top
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y < 0:
                    self.rect.top = t.rect.bottom
                    self.pos_x = 0
                    self.pos_y = 0
        for o in obsticles:
            if pygame.sprite.collide_rect(self, o):
                if self.pos_x > 0:
                    self.rect.right = o.rect.left
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_x < 0:
                    self.rect.left = o.rect.right
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y > 0:
                    self.rect.bottom = o.rect.top
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y < 0:
                    self.rect.top = o.rect.bottom
                    self.pos_x = 0
                    self.pos_y = 0

                 
    def Walking_Animation(self, walking, up, down, left, right):
        walk = walking
        if down:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character.png", self.image_cache)
        elif up:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_Back_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character_Back.png", self.image_cache)
        elif left:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_Left_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character_Left.png", self.image_cache)
        elif right:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_Right_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character_Right.png", self.image_cache)
                                    
        return walk

    def get_pos(self):
        return (self.pos_x, self.pos_y)

#mouse Class
class Mouse(Entity):

    def __init__(self, pos):
        Entity.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.rect = Rect(pos[0], pos[1], 32, 32)

    def update(self, pos, check=False):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.top = pos[1]
        self.rect.left = pos[0]

        if check:
            print "Mouse Pos: %s" %(self.rect)
            print self.x, self.y

    def get_rect(self):
        return (self.x, self.y)

#Grass Class
class Grass(Entity):
    
    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.name = "Grass"
        self.image = functions.get_image("data/images/Grass1.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect

#Plain Grass
class Plain_Grass(Entity):
        
    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.name = "Plain_Grass"
        self.image = functions.get_image("data/images/Grass_Plain.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect

#Grass With Flower
class Grass_Flower(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.name = "Grass_Flower"
        self.image = functions.get_image("data/images/Grass_Flower.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect

#Grass To Sand (Directly, no angles)
class Grass_To_SandD(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Grass_To_SandD"
        self.image = functions.get_image("data/images/Grass_To_SandD.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height) 

#Trees
class Tree(Entity):

    def __init__(self, x, y, image_cache):
        global rect, image
        Entity.__init__(self)
        self.name = "Tree"
        self.image = functions.get_image("data/images/Tree.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 64)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect
#Paths
class Path(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Path"
        self.image = functions.get_image("data/images/Path.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect

#Sands
class Sand(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Sand"
        self.image = functions.get_image("data/images/Sand.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
            return self.rect

#Sand With Dead Tree
class Sand_Dead(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Sand_Dead"
        self.image = functions.get_image("data/images/Dead_Branch.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect


#Sand To Water Direct (Shore Line)
class Sand_To_Water(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Sand_To_Water"
        self.image = functions.get_image("data/images/Sand_To_Water.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect


#Water
class Water(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Water"
        self.image = functions.get_image("data/images/Water.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect

#Planks
class Planks(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.name = "Planks"
        self.image = functions.get_image("data/images/Wood.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect


class Dug_Out(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image = functions.get_image("data/images/Dug_Out.png", image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
    def hit_test(self, x, y):
        return (self.rect.x <= x < self.rect.x+self.rect.width and 
                self.rect.y <= y < self.rect.y+self.rect.height)
    def get_rect(self):
        return self.rect


#Start Menu New Game
class New_Game(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image_cache = image_cache
        self.image = functions.get_image("data/images/New_Game.png", self.image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 200, 50)

    def update(self, mousepos):
        if self.rect.collidepoint(mousepos):
            self.image = functions.get_image("data/images/New_Game_Hover.png", self.image_cache)
        else:
            self.image = functions.get_image("data/images/New_Game.png", self.image_cache)

    def check_click(self, clicked, mousepos):
        if self.rect.collidepoint(mousepos):
            if clicked:
                self.image = functions.get_image("data/images/New_Game_Hover.png", self.image_cache)
                start = True
            else:
                start = False
        else:
            start = False
        return start

#Start Menu Quit Button
class Quit_Game(Entity):

    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image_cache = image_cache
        self.image = functions.get_image("data/images/Quit.png", self.image_cache)
        self.image.convert()
        self.rect = Rect(x, y, 200, 50)

    def update(self, mousepos, clicked):
        if self.rect.collidepoint(mousepos):
            self.image = functions.get_image("data/images/Quit_Hover.png", self.image_cache)
            if clicked:
                pygame.quit()
                sys.exit()
        else:
            self.image = functions.get_image("data/images/Quit.png", self.image_cache)
           
