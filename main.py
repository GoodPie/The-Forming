#!/usr/bin/python
#Created and maintained by Brandyn Britton


import pygame, sys, os, datetime, time, glob, tilemap, math
from pygame.locals import *
from functions import *
from EntityClasses import *

#Screen Settings and variables
windowSize = window_width, window_height = 640, 640
half_width = window_width/2
half_height = window_height/2
block_size = block_width, block_height = 32, 32
depth = 0
flags = 32

#Mini map settings and variables
miniMap = map_width, map_height = 80, 80
half_map_width = map_width/2
half_map_height = map_height/2


#Ensuring the screen isn't to big for the amount of blocks
if window_width%block_width != 0 and window_height%block_height != 0:
    print "Screen is to big for the amount of blocks"

fps = 25 #Setting the maximum frames per second

#Colors (used mainly for minimap), [RRR, GGG, BBB]
#All colors should be added here instead of typing the color in a single piece
#of code
black = [000, 000, 000]
white = [255, 255, 255]
gray = [155, 155, 155]
red = [255, 000, 000]
green = [000, 255, 000]
blue = [000, 000, 255]

#loading all variables and what not to prepare the game#
def main():
    global screen, trees, obsticles, grass, buildables, clock, level, image_cache, camera, background_entities, player_entities, player, map_entities

    #Initiating everything needed for the game
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    clock = pygame.time.Clock()

    image_cache = {}
    all_images = glob.glob("data/images/*.png")
    print "All Images Loaded!"
    for image in all_images:
        get_image(image, image_cache)

    #Creating Entity Groups
    background_entities = pygame.sprite.Group() #The background image entities
    player_entities = pygame.sprite.Group() #Holds NPC's and Player
    map_entities = pygame.sprite.Group() #Holds minimap entities
    obsticles = [] #Everything the player stops at...
    trees = [] #Gets all the trees
    grass = [] #Gets all the grass and sand and st00f
    buildables = [] #blocks that are buidable on

    player = Player(32, 32, image_cache)
    player_entities.add(player)

    #Initiating constants for the game
    current_level = currentLevelChecker()
    level = tilemap.Checker(current_level)

    #This is the main process of the game (order of events that usually take place)
    start_menu() 
    main_game_loop(level, obsticles, player)


#This is used to display and load the entire game#
def main_game_loop(level, obsticles, player):
    global total_level_height, total_level_width

    #defaulting everything
    #up = -, down = +, left = -, right = +#
    up = down = left = right = False

    total_level_width = len(level[0])*block_width
    total_level_height = len(level)*block_height
    
    building_blocks_placed = []

    camera = Camera(main_camera, total_level_width, total_level_height)
    
    #Setting up the background of the level
    back_x = back_y = 0
    for back_row in level:
        for back_col in back_row:
            Draw_Level( back_x, back_y, back_col, obsticles, background_entities, image_cache )
            back_x += 32
        back_y += 32
        back_x = 0

    #Setting up the inventory layout (for design mode), will be replaced
    inventory_entities = pygame.sprite.Group()
    invent_layout = [
        "GTOSW",
        "FPL__",
        ]
    inv_x = inv_y = 0
    for inv_row in invent_layout:
        for inv_col in inv_row:
            Draw_Level(inv_x, inv_y, inv_col, obsticles, inventory_entities, image_cache)
            inv_x += 32
        inv_y += 32
        inv_x = 0

    #Used for the walking animation of the character
    walking = False

    #Inventory Image (when q is pressed)
    inv_image = get_image("data/images/Inventory.png", image_cache)
    inventory_show = False
    selected_block = ""

    #Setting up the mouse for game and initial variables
    mouse_pos = pygame.mouse.get_pos()
    mouse = Mouse(mouse_pos)
    mouse_clicked = False
    mouse_right_clicked = False

    #Set to check position of player when "p" is pressed
    position_check = False

    #Setting up lighting
    game_alpha = 4 #Keeping it simple for now
    game_time = 15300
    time_increment = -1
    alpha_increment = 1

    while True:
        
        mouse_clicked = False
        clock.tick(fps)
        fps_current = float(clock.get_fps())
        if float(game_time)%game_alpha == 0:
            game_alpha += alpha_increment
            print "Game Alpha: ",game_alpha
            print "Game Time: ", game_time
        if game_time < 0:
            time_increment = 1
            alpha_increment = -1
        elif game_time >= 15300:
            time_increment = -1
            alpha_increment = 1
        
        #Enables constant monitoring of FPS
        pygame.display.set_caption("The Forming FPS:" + str(fps_current))

        #Event handling
        for event in pygame.event.get():
            #Quit the game, for those who can't handle it#
            if event.type == QUIT:
                pygame.quit()
            #All keydown events (pushing down keys on keyboard...)#
            if event.type == KEYDOWN:
                
                if event.key == K_UP or event.key == K_w:
                    up = True
                elif event.key == K_DOWN or event.key == K_s:
                    down = True
                elif event.key == K_LEFT or event.key == K_a:
                    left = True
                elif event.key == K_RIGHT or event.key == K_d:
                    right = True
                elif event.key == K_F1:
                    take_screen_shot(screen)
                elif event.key == K_F2:
                    pygame.display.toggle_fullscreen()
                #This allows for the user to check the player position (x, y)
                elif event.key == K_q:
                    inventory_show = True
                #Displays Inventory
                elif event.key == K_p:
                    position_check = True
                    
            #All keyup events (keys popup on keyboard...)#
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    up = False
                elif event.key == K_DOWN or event.key == K_s:
                    down = False
                elif event.key == K_LEFT or event.key == K_a:
                    left = False
                elif event.key == K_RIGHT or event.key == K_d:
                    right = False
                    
                elif event.key == K_p:
                    position_check = False
                elif event.key == K_q:
                    inventory_show = False
                    
            #All mouse events
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
                elif event.button == 3:
                    mouse_right_clicked = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_clicked = False
                elif event.button == 3:
                    mouse_right_clicked = False

        #Updating the player
        camera.update(player)
        player.update(up, down, left, right, position_check, obsticles, trees,
                      total_level_width, total_level_height)
        walking = player.Walking_Animation(walking, up, down, left, right)

        #Drawing each entity to the screen
        for be in background_entities:
            screen.blit(be.image, camera.apply(be))
        for pe in player_entities:
            screen.blit(pe.image, camera.apply(pe))

        #Setting up mouse positions on screen and map
        mouse_pos = pygame.mouse.get_pos()
        pos = camera.reverse(mouse_pos)

        game_shadow = pygame.Surface((640, 640))
        game_shadow.fill(pygame.Color(0, 0, 0))
        game_shadow.set_alpha(game_alpha)
        game_shadow.convert_alpha()
        screen.blit(game_shadow, (0, 0))
        
        #Checking for mouse clicks on screen and inventory
        if inventory_show:
            screen.blit(inv_image,(0, 0))
            #draws the images to the inventory
            for inv in inventory_entities:
                inv_x, inv_y = inv.rect[0], inv.rect[1]
                screen.blit(inv.image, (inv_x, inv_y))
            #checks if mouse is clicked in the inventory
            if mouse_clicked:
                selected_block = check_click_inv(mouse_pos, inventory_entities, building_blocks_placed)
        #Checks if you are placing or replacing blocks
        if not inventory_show:
            if mouse_clicked:
                replace_block(pos)
            if mouse_right_clicked:
                place_block(pos, selected_block)

        game_time += time_increment

        pygame.display.flip()

#This is used to display the initial start menu#
def start_menu():

    start_game = False

    #Setting up images for start menu
    new_game = New_Game(half_width, half_height-50, image_cache)
    quit_game = Quit_Game(half_width, half_height + 10, image_cache)

    #Getting all the necessary images
    background = get_image("data/images/Menu_Background.png", image_cache)
    screen.blit(background, (0, 0))
    made_by = get_image("data/images/Credits.png", image_cache)
    screen.blit(made_by, (20, window_height-50))

    #Setting up button entities
    button_entities = pygame.sprite.Group()
    button_entities.add((new_game, quit_game))

    while not start_game:
        clock.tick(fps)
        fps_current = float(clock.get_fps())
        
        pygame.display.set_caption("The Forming FPS:" + str(fps_current))
        mouse_click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    take_screen_shot(screen)

        #Blitting all the background images of the start screen
        screen.blit(background, (0, 0))
        screen.blit(made_by, (20, window_height-50))

        #Gets the mouse position and checks collisions
        mouse_position = pygame.mouse.get_pos()
        new_game.update(mouse_position)
        quit_game.update(mouse_position, mouse_click)

        #Checks if the new game button has been pressed
        start_game = new_game.check_click(mouse_click, mouse_position)

        button_entities.draw(screen)

        pygame.display.flip()

#This passes all the entities to the game for drawing
def Draw_Level( x, y, column, obsticles, entities, image_cache ):

    #Grass#
    if column == "G":
        g = Grass(x, y, image_cache)
        entities.add(g)
        grass.append(g)
    #Plain Grass#
    elif column == "P":
        p = Plain_Grass(x,y, image_cache)
        entities.add(p)
        grass.append(p)
    #Grass with yellow flower#
    elif column == "F":
        f = Grass_Flower(x,y, image_cache)
        entities.add(f)
        grass.append(f)
    #Grass To Sand (50/50 split block) Direct#
    elif column == "Y":
        q = Grass_To_SandD(x,y, image_cache)
        entities.add(q)
        grass.append(q)
    #Tree#
    elif column == "T":
        t = Tree(x, y, image_cache)
        trees.append(t)
        entities.add(t)
    #Path#
    elif column == "O":
        o = Path(x, y, image_cache)
        entities.add(o)
        grass.append(o)
    #Sand#
    elif column == "S":
        s = Sand(x, y, image_cache)
        entities.add(s)
        grass.append(s)
    #Sand To Water (50/50 split block) Direct#
    elif column == "Q":
        q = Sand_To_Water(x, y, image_cache)
        entities.add(q)
    #Water#
    elif column == "W":
        w = Water(x, y, image_cache)
        obsticles.append(w)
        entities.add(w)
    #Dead Branch In Sand#
    elif column == "D":
        d = Sand_Dead(x, y, image_cache)
        entities.add(d)
        grass.append(d)
    elif column  == "L":
        l = Planks(x, y, image_cache)
        obsticles.append(l)
        entities.add(l)
        grass.append(l)
    

#Camera function
def main_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+half_width, -t+half_height, w, h

    l = min(0, l)
    l = max(-(camera.width-window_width), l)
    t = max(-(camera.height-window_height), t)
    t = min(0, t)
    return Rect(l, t, w, h)

#This replaces the blocks with "buildable" blocks
def replace_block(mouse_pos):

    #Checks if the entity is classed as a grass block
    for g in grass:
        rect = g.get_rect()
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            print "A block has been clicked"
            new_image = Dug_Out(g.rect[0], g.rect[1], image_cache)
            grass.remove(g)
            background_entities.remove(g)
            try:
                obsticles.remove(g)
                trees.remove(g)
                print "Grass had collision issues"
            except ValueError:
                pass
            buildables.append(new_image)
            background_entities.add(new_image)

    #checks if the entity is classed as a tree (for collisions and replacing)
    for t in trees:
        rect = t.get_rect()
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            print "Tree has been clicked"
            new_image = Grass(t.rect[0], t.rect[1], image_cache)
            background_entities.remove(t)
            trees.remove(t)
            grass.append(new_image)
            background_entities.add(new_image)

#This checks what item has been clicked in the inventory
def check_click_inv(mouse_pos, invList, placed):

    for inv in invList:
        rect = inv.get_rect()
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            return inv.name

#This is to place objects on top of buildable blocks
def place_block(mouse_pos, selected_block):

    #This ensures blocks can only be placed on the "cement" or dug out blocks
    for b in buildables:
        rect = b.get_rect()
        #Checking collide points between mouse and buildables
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            print "You can build on this block"

            #Checkign whether or not a block from the inventory has been selected
            if not selected_block:
                print "No block has been selected"
            if selected_block:
                block = eval(selected_block)
                new_image = block(b.rect[0], b.rect[1], image_cache)
                buildables.remove(b)
                background_entities.remove(b)
                background_entities.add(new_image)

                #Checking collision properties
                if selected_block == "Tree":
                    trees.append(new_image)
                if selected_block == "Planks" or selected_block == "Water":
                    obsticles.append(new_image)
                
            
            
if __name__ == "__main__":
    main()
