#!/usr/bin/python

import pygame, sys, os, datetime, time, random, tilemap
from pygame.locals import *

#Always ensure that the height and width are devisible by 32!
windowSize = windowWidth, windowHeight = 640, 640
HALF_WIDTH = windowWidth/2
HALF_HEIGHT = windowHeight/2
DEPTH = 0
FLAGS = 32
CAMERA_SLACK = 30

miniMap = mapWidth, mapHeight = 80, 80
map_half_width = mapWidth/2
map_half_height = mapHeight/2


#Ensuring width and height can take 32x32 blocks
if windowWidth%32 == 0 and windowHeight%32 == 0:
    blocksInX = windowWidth/32
    blocksInY = windowHeight/32
else:
    raise SystemExit, "Too Much Space To Fit 32x32 Blocks in X and Y"

#Frames Per Second (MAX, not what it is going to be)
FPS = 60
    
#Colours
black = [ 0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [ 0, 255, 0]
blue = [ 0, 0, 255]
orange = [ 255, 122, 0]
cyan = [ 0, 155, 255]
purple = [ 155, 0, 255]
lime = [155, 255, 0]

def main():
    global cameraX, cameraY, screen, clock
    
    #Setting initial needed variables
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    clock = pygame.time.Clock()

    #Start Screen  
    startMenu(screen, clock)

    #Current level
    currentLevel = currentLevelChecker()
    level = tilemap.Checker(currentLevel)

    mainGameLoop(level, clock, screen)
    
def mainGameLoop(level, clock, screen):
    #Defaulting the all controlls to "off" upon first starting (no button is being pushed)
    up = down = left = right = False
    
    #Assuming everything including player is an entity (including the grass)
    entities = pygame.sprite.Group()
    mapentities = pygame.sprite.Group()
    players = pygame.sprite.Group()
    player = Player(32, 32)
    player_map = Player_Map(8, 8)
    obsticles = []

    #upadting the background
    background = pygame.Surface((32, 32))
    background.convert()
    background.fill(black)

    #NPC Control
    george = George(64, 64)
    
    #Placing all the blocks needed to be displayed
    x = y = 0
    for row in level:
        for col in row:
            levelPasser(x,y,col, obsticles, entities)
            x += 32 
        y += 32
        x = 0

    map_block_width = float(windowWidth)/len(level[0])
    map_block_height = float(windowHeight)/len(level)

    x = y = 0
    for map_row in level:
        for map_col in map_row:
            mapPasser(x, y, map_col, mapentities, map_block_width, map_block_height)
            x+=map_block_width
        y+=map_block_height
        x=0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    total_map_width = len(level[0])*8
    total_map_height = len(level)*8
    camera = Camera(complex_camera, total_level_width, total_level_height)
    map_camera = MiniMap(complexMap, total_map_width, total_map_height)
    
    entities.add(player)
    players.add((player, george))
    mapentities.add(player_map)

    walk = True
        
    while True:
        clock.tick(FPS)
        FPS_Current = clock.get_fps()
        pygame.display.set_caption("The Forming. FPS:" + str(FPS_Current)) 

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type ==  KEYDOWN:
                if event.key == K_ESCAPE:
                    startMenu(screen, clock)
                #Passing commands for keydown events
                #UP = "-", down = "+", Left = "-", right = "+"
                elif event.key == K_UP:
                    up = True
                elif event.key == K_DOWN:
                    down = True
                elif event.key == K_LEFT:
                    left = True
                elif event.key == K_RIGHT:
                    right = True
                #Adding screenshot capabilities.
                elif event.key == K_F1:
                    takeScreenShot(screen)                    
                        
            if event.type == KEYUP:
                if event.key == K_UP:
                    up = False
                elif event.key == K_DOWN:
                    down = False
                elif event.key == K_LEFT:
                    left = False
                elif event.key == K_RIGHT:
                    right = False


        for l in range(32):
            for k in range(32):
                screen.blit(background,(l*32,k*32))
                        
        #Redrawing all other objects
        camera.update(player)
        map_camera.update(player_map)
        
        walk = player.Walking(walk, up, down, left, right)
        player.update(up, down, left, right, obsticles, total_level_width, total_level_height)
        george.update(total_level_width, total_level_height, player.get_pos())
        player_map.update(up, down, left, right, total_map_width, total_map_height)
        
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        for p in players:
            screen.blit(p.image, camera.apply(p))
        for m in mapentities:
            screen.blit(m.image, camera.apply(m))

        pygame.display.update()

def initiate_combat():
    print "Combat Started"

def takeScreenShot(screen):
    timeTaken = time.asctime(time.localtime(time.time()))
    timeTaken = timeTaken.replace(" ","_")
    timeTaken = timeTaken.replace(":", ".")
    saveFile = "screenshots/" + timeTaken + ".png"
    pygame.image.save(screen, saveFile)
    print "ScreenShot Taken"

def currentLevelChecker(area="generation"):
    return area

def startMenu(screen, clock):
    
    #Game start menu
    start = False
    title = Title(0, 50)

    #Positions for start menu ents
    newGame = New_Game(HALF_WIDTH, HALF_HEIGHT-50)
    quitGame = Quit_Game(HALF_WIDTH, HALF_HEIGHT + 10)

    #Initial Blitting Of Start Menu Objects
    background = pygame.image.load("data/images/Menu_Background.png")
    screen.blit(background, (0, 0))
    Credits = pygame.image.load("data/images/Credits.png")
    screen.blit(Credits, (20, windowHeight-50))

    #Adding Entities
    startMenuEnts = pygame.sprite.Group()
    startMenuEnts.add((newGame, quitGame, title))

    #Standard main Game Loop
    while start == False:
        clock.tick(FPS)
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True

        #Getting the mouse Position
        mousePos = pygame.mouse.get_pos()

        #Blitting The Background Of The Start Menu
        screen.blit(background, (0, 0))
        screen.blit(Credits, (20, windowHeight-50))

        #Checking If Mouse Is Clicked Over newGame
        newGame.update(mousePos)
        quitGame.update(mousePos, mouseClick)
        start = newGame.checkClick(mouseClick, mousePos)

        #Drawing start menu entities onto the screen
        startMenuEnts.draw(screen)
        
        pygame.display.update()

    startMenuEnts.empty()

#This passes all the entities to the game.
def levelPasser(x,y,col, obsticles, entities):
    
    if col == "G":
        '''Grass'''
        g = Grass(x,y)
        obsticles.append(g)
        entities.add(g)
    elif col == "P":
        '''Plain Grass'''
        p = Plain_Grass(x,y)
        obsticles.append(p)
        entities.add(p)
    elif col == "F":
        '''Flower Grass'''
        f = Grass_Flower(x,y)
        obsticles.append(f)
        entities.add(f)
    elif col == "Y":
        '''Grass To Sand Direct'''
        q = Grass_To_SandD(x,y)
        obsticles.append(q)
        entities.add(q)
    elif col == "T":
        '''Tree'''
        t = Tree(x, y)
        obsticles.append(t)
        entities.add(t)
    elif col==" ":
        '''Checking For Spaces in Level'''
        x -= 32
    elif col == "O":
        '''Path'''
        o = Path(x, y)
        obsticles.append(o)
        entities.add(o)
    elif col == "S":
        '''Sand'''
        s = Sand(x, y)
        obsticles.append(s)
        entities.add(s)
    elif col == "Q":
        '''Sand To Water (Shore)'''
        q = Sand_To_Water(x, y)
        obsticles.append(q)
        entities.add(q)
    elif col == "W":
        '''Water'''
        w = Water(x, y)
        obsticles.append(w)
        entities.add(w)
    elif col == "D":
        '''Dead Branch In Sand'''
        d = Sand_Dead(x, y)
        obsticles.append(d)
        entities.add(d)

def mapPasser(x,y,col,mapentities, height, width):
    
    if col == "G":
        g = Grass_Map(x,y,height,width)
        mapentities.add(g)
    elif col == "P":
        p = Grass_Map(x,y,height,width)
        mapentities.add(p)
    elif col == "F":
        f = Grass_Map(x,y,height,width)
        mapentities.add(f)
    elif col == "Y":
        q = Grass_Map(x,y,height,width)
        mapentities.add(q)
    elif col == "T":
        t = Tree_Map(x, y,height,width)
        mapentities.add(t)
    elif col==" ":
        '''Checking For Spaces in Level'''
        x -= 8
    elif col == "O":
        o = Path_Map(x, y,height,width)
        mapentities.add(o)
    elif col == "S":
        s = Sand_Map(x, y,height,width)
        mapentities.add(s)
    elif col == "Q":
        q = Sand_Map(x, y,height,width)
        mapentities.add(q)
    elif col == "W":
        w = Water_Map(x, y,height,width)
        mapentities.add(w)
    elif col == "D":
        d = Sand_Map(x, y,height,width)
        mapentities.add(d)

#Main Entity Class
class Entity(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#This is the main Player class.
#It controlls the players movement and other stuff
#like collisions
class Player(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.xPos = x
        self.yPos = y
        self.inShop = False
        self.image = pygame.image.load("data/images/Character.png")
        self.image.convert()
        self.rect = Rect(self.xPos, self.yPos, 32, 32)
        
    def update(self, up, down, left, right, obsticles, levelWidth, levelHeight):
        if up:
            self.yPos = -8
        if down:
            self.yPos = 8
        if left:
            self.xPos = -8
        if right:
            self.xPos = 8

        if not up and not down:
            self.yPos = 0
        if not left and not right:
            self.xPos = 0

        self.rect.left += self.xPos
        self.rect.top += self.yPos
        #Collision Detection (for x axis)
        self.collide(levelWidth, levelHeight)

    def Walking(self, walk, up, down, left, right):
        if down:
            if walk == True:
                walk = False
                self.image = pygame.image.load("data/images/Character_W.png")
            elif walk == False:
                walk = True
                self.image = pygame.image.load("data/images/Character.png")
        elif up:
            if walk == True:
                walk = False
                self.image = pygame.image.load("data/images/Character_Back_W.png")
            elif walk == False:
                walk = True
                self.image = pygame.image.load("data/images/Character_Back.png")
        elif left:
            if walk == True:
                walk = False
                self.image = pygame.image.load("data/images/Character_Left.png")
            elif walk == False:
                walk = True
                self.image = pygame.image.load("data/images/Character_Left_W.png")
        elif right:
            if walk == True:
                walk = False
                self.image = pygame.image.load("data/images/Character_Right_W.png")
            elif walk == False:
                walk = True
                self.image = pygame.image.load("data/images/Character_Right.png")

        return walk
        
    def collide(self, levelWidth, levelHeight):

        if self.rect.top < 0:
            self.yPos = 0
            self.rect.top = 0

        if self.rect.bottom > levelHeight:
            self.yPos = 0
            self.rect.bottom = levelHeight

        if self.rect.left < 0:
            self.xPos = 0
            self.rect.left = 0

        if self.rect.right > levelWidth:
            self.xPos = 0
            self.rect.right = 0

    def get_pos(self):
        return (self.rect.left, self.rect.top)


class Player_Map(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.xPos = x
        self.yPos = y
        self.inShop = False
        self.image = pygame.Surface((8,8))
        self.image.convert()
        self.image.fill([255, 0, 0])
        self.rect = Rect(self.xPos, self.yPos, 8, 8)
        
    def update(self, up, down, left, right, levelWidth, levelHeight):
        if up:
            self.yPos = -2
        if down:
            self.yPos = 2
        if left:
            self.xPos = -2
        if right:
            self.xPos = 2

        if not up and not down:
            self.yPos = 0
        if not left and not right:
            self.xPos = 0

        self.rect.left += self.xPos
        self.rect.top += self.yPos
        #Collision Detection (for x axis)
        self.collide(levelWidth, levelHeight)
        
    def collide(self, levelWidth, levelHeight):

        if self.rect.top < 0:
            self.yPos = 0
            self.rect.top = 0

        if self.rect.bottom > levelHeight:
            self.yPos = 0
            self.rect.bottom = levelHeight

        if self.rect.left < 0:
            self.xPos = 0
            self.rect.left = 0

        if self.rect.right > levelWidth:
            self.xPos = 0
            self.rect.right = 0


#This is george, a test npc. Controls random
#Movements made by george
class George(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.xPos = x
        self.yPos = y
        self.inShop = False
        self.image = pygame.Surface((32, 32))
        self.image.fill(blue)
        self.image.convert()
        self.rect = Rect(self.xPos, self.yPos, 32, 32)

    def update(self, levelWidth, levelHeight, player):
        move = random.randint(1,15)
        if move < 2:
            direction = random.randint(1,4)
            if direction == 1:
                self.xPos = -32
            if direction == 2:
                self.xPos = 32
            if direction == 3:
                self.yPos = -32
            if direction == 4:
                self.yPos = 32
        else:
            self.xPos = self.yPos = 0

        self.rect.left += self.xPos
        self.rect.top += self.yPos

        self.collide(levelWidth, levelHeight, player)

    def collide(self, levelWidth, levelHeight, player):
        if self.rect.top < 0:
            self.yPos = 0
            self.rect.top = 0

        if self.rect.bottom > levelHeight:
            self.yPos = 0
            self.rect.bottom = levelHeight

        if self.rect.left < 0:
            self.xPos = 0
            self.rect.left = 0

        if self.rect.right > levelWidth:
            self.xPos = 0
            self.rect.right = 0

        if self.rect.collidepoint(player):
            initiate_combat()
            
#The camera (not my code)
class MiniMap(object):

    def __init__(self, miniMap_func, width, height):
        self.miniMap_func = miniMap_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.miniMap_func(self.state, target.rect)

def complexMap(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+map_half_width, -t+map_half_height, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-mapWidth), l)   # stop scrolling at the right edge
    t = max(-(camera.height-mapHeight), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)
            
class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-windowWidth), l)   # stop scrolling at the right edge
    t = max(-(camera.height-windowHeight), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

#The following classes are all sprite classes.                
class Grass(Entity):
    
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Grass.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Grass_Map(Entity):

    def __init__(self, x, y ,width, height):
        Entity.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill([0, 255, 0])
        self.image.set_alpha(150)
        self.rect = Rect(x, y ,width, height)

class Plain_Grass(Entity):
        
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Grass_Plain.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Grass_Flower(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Grass_Flower.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
                
class Grass_To_SandD(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Grass_To_SandD.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Tree(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Tree.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Tree_Map(Entity):

    def __init__(self, x, y,width, height):
        Entity.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill([0, 100, 0])
        self.image.set_alpha(150)
        self.rect = Rect(x, y,width, height)

class Path(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Path.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Path_Map(Entity):

    def __init__(self, x, y,width, height):
        Entity.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill([139, 137, 137])
        self.image.set_alpha(150)
        self.rect = Rect(x, y,width, height)

class Sand(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Sand.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Sand_Map(Entity):

    def __init__(self, x, y,width, height):
        Entity.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill([255, 215, 0])
        self.image.set_alpha(150)
        self.rect = Rect(x, y,width, height)

class Sand_Dead(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Dead_Branch.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Sand_To_Water(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Sand_To_Water.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Water(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Water.png")
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

class Water_Map(Entity):

    def __init__(self, x, y,width, height):
        Entity.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.convert()
        self.image.fill([0, 0, 205])
        self.rect = Rect(x, y, width, height)

class Title(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Title.png")
        self.image.convert()
        self.rect = Rect(x, y, 576, 100)

class New_Game(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/New_Game.png")
        self.image.convert()
        self.rect = Rect(x, y, 200, 50)

    def update(self, mousepos):
        if self.rect.collidepoint(mousepos):
            self.image = pygame.image.load("data/images/New_Game_Hover.png")
        else:
            self.image = pygame.image.load("data/images/New_Game.png")

    def checkClick(self, clicked, mousepos):
        if self.rect.collidepoint(mousepos):
            if clicked:
                self.image = pygame.image.load("data/images/New_Game_Pressed.png")
                start = True
            else:
                start = False
        else:
            start = False
        return start

class Quit_Game(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("data/images/Quit.png")
        self.image.convert()
        self.rect = Rect(x, y, 200, 50)

    def update(self, mousepos, mouseClick):
        if self.rect.collidepoint(mousepos):
            self.image = pygame.image.load("data/images/Quit_Hover.png")
            if mouseClick:
                self.image = pygame.image.load("data/images/Quit_Pressed.png")
                pygame.quit()
                sys.exit()
        else:
            self.image = pygame.image.load("data/images/Quit.png")


if __name__ == "__main__":
    main()
