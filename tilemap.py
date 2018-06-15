#This is the map layout folder. Feel free to edit it to your hearts desire,
#just be careful not to destroy the entire game (your loss not mine). Also,
#Feel free to change the textures...

import random

"""
	KEY:
        Screen Size = 640x640
	G = Grass
	P = Plain Grass (less detail)
	F = Grass Flower (Includes A Flower...)
	Y = Grass -> Sand (Direct)
	L = Grass -> Sand (From Left)
	R = Grass -> Sand (From Right)
	T = Grass -> Sand (Tiny Grass)
	S = Sand
	Q = Sand -> Water (Direct)
	W = Water
	O = Stone Path
	H = House (Decoration)
	M = Armor Shop
	N = Weapon Shop
	B = Potion Shop
	C = Dungeon Entrance
	D = Sand (Dead)
"""

def Checker(area="generation"):
    if area == "testPlace":
        level = testPlace()
    elif area == "generation":
        level = tileMapGeneration()

    return level


def testPlace():

    #This is where all the testing happens...
    
    tilemap = [
            'TTTTTTTTTTTTTTTTTTTTTTTTTT',
            'TGFGGGGPPFPGGGGGGGGGGGGGGT',
            'TGGGGGGGFGPGGGGGGGGGGGGGGT',
            'TGGGGGGGGFPFFGFGGGGGGGGGGT',
            'OOOOOOOOOOOOOOOOOOOOOOOOOO',
            'OOOOOOOOOOOOOOOOOOOOOOOOOO',
            'GGFGGGGGGOOFGGGGGGGGGGGGGG',
            'FGFTGGGGTOOFGGGGGGGGGGGGGG',
            'TGGGGGGGGOOTGGGGFGPGGGGGGG',
            'GGGTFGGGGOOGGGGGGGTGGGGGGG',
            'GGGGGGGGGGGGGFGGGTGGGGGGGG',
            'YYYYYYYYYYYYYYYYYYYYYYYYYY',
            'SSSSSSSSSSSSSSSSSSSSSSSSSS',
            'SSSSSSSSSSSSSSSSSSSSSSSSSS',
            'SSSSSSSSSSSSSSSSSSSSSSSSSS',
            'QQQQQQQQQQQQQQQQQQQQQQQQQQ',
            'WWWWWWWWWWWWWWWWWWWWWWWWWW',
            'WWWWWWWWWWWWWWWWWWWWWWWWWW',
            'WWWWWWWWWWWWWWWWWWWWWWWWWW',
            'WWWWWWWWWWWWWWWWWWWWWWWWWW',
            'WWWWWWWWWWWWWWWWWWWWWWWWWW',
]

    return tilemap


def tileMapGeneration():

    tilemap = []
    levelString = ""

    biome = random.randint(1,3)
    if biome == 1:
        biome = "forest"
    if biome == 2:
        biome = "plains"
    if biome == 3:
        biome = "desert"

    waterAmount = random.randint(1,20)

    print biome
    while len(tilemap) != 100:
        structure = random.randint(1,10)
        if biome != "desert":
            if biome == "plains" and (structure == 1 or
                                      structure == 6 or
                                      structure == 7 or
                                      structure == 8 or
                                      structure == 9 or
                                      structure == 10):
                    levelString += "G"
            elif biome != "plains" and structure == 1:
                levelString += "G"
            
        if biome != "desert":
            if biome == "forest" and (structure == 2 or
                                      structure == 6 or
                                      structure == 7 or
                                      structure == 8 or
                                      structure == 9 or
                                      structure == 10):
                    levelString += "T"
            elif biome != "forest" and structure == 2:
                levelString += "T"

        if biome == "desert" and (structure == 3 or
                                   structure == 6 or
                                   structure == 7 or
                                   structure == 8 or
                                   structure == 9 or
                                   structure == 10):
            randomSand = random.randint(1,1000)
            if randomSand < 990:
                levelString += "S"
            elif randomSand == 991 and waterAmount > 0:
                levelString += "W"
                waterAmount -= 1
            elif randomSand > 991:
                levelString += "D"
        if biome != "desert":
            if structure == 4:
                levelString += "P"
        if biome != "desert":
            if structure == 5:
                levelString += "F"
            
        if len(levelString) == 100:
            tilemap.append(levelString)
            levelString = ""

    return tilemap
        
            
