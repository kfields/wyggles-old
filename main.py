import sys
import os

sys.path.insert(0, os.path.abspath(__file__))

import data
import math
from random import random

from pyglet.gl import *
from pyglet import clock
from pyglet import font
from pyglet import image
from pyglet import media
from pyglet import window
from pyglet.window import key

from wyggles.sprite.engine import *
from wyggles.sprite.body import *
from wyggles.mathutils import *
from wyggles.box import Box
from wyggles.ball import Ball
from wyggles.apple import *
from wyggles.wyggle import Wyggle
    
#Walls
def spawnWalls():
    minX = worldMinX 
    minY = worldMinY 
    maxX = worldMaxX 
    maxY = worldMaxY
    thickness = 200
    #North Wall
    northWall = BoxBody(None)
    northWall.setMinMax(minX-thickness, minY-thickness, maxX+thickness, minY, floatMax)
    spriteEngine.addBody(northWall)
    #East Wall
    eastWall = BoxBody(None)
    eastWall.setMinMax(maxX, minY-thickness, maxX+thickness, maxY+thickness, floatMax)
    spriteEngine.addBody(eastWall)
    #South Wall
    southWall = BoxBody(None)    
    southWall.setMinMax(minX-thickness, maxY, maxX+thickness, maxY+thickness, floatMax)
    spriteEngine.addBody(southWall)
    #West Wall
    westWall = BoxBody(None)
    westWall.setMinMax(minX-thickness, minY-thickness, minX, maxY+thickness, floatMax)
    spriteEngine.addBody(westWall)

#Balls
def spawnBall(layer):
    ball = Ball(layer)
    ball.materializeAt(random() * (worldMaxX - 100), random() * (worldMaxY - 100))        

def spawnBalls(layer):
    i = 0
    while(i < 10):
        i = i + 1
        spawnBall(layer)
#Boxes
def spawnBox(layer):
    box = Box(layer)
    box.materializeAt(Math.random() * (worldMaxX - 100), Math.random() * (worldMaxY - 100))

def spawnBoxes():
    total = 10
    i = 0
    while(i < total):
        i = i + 1
        spawnBox(layer) ;
#

#Apples
#def spawnApple(layer):
#    apple = Apple(layer)
#    materializeRandomFromCenter(apple)

#Wyggles
def spawnWyggle(layer, color):
    wyggle = Wyggle(layer, color)
    materializeRandomFromCenter(wyggle)

def spawnWyggles(root):
    layer = Layer("wyggles")
    spawnWyggle(layer, "green")
    spawnWyggle(layer, "blue")
    spawnWyggle(layer, "pink")
    root.add_layer(layer)

#
def main():
    #spriteConsole = new Wyggles.Console() ;
    #worldMaxX = document.documentElement.clientWidth - 1
    worldMaxX = 640
    #worldMaxY = document.documentElement.clientHeight - 1
    worldMaxY = 480
    win = window.Window(worldMaxX, worldMaxY, caption='Wyggles')
    #
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glBlendFunc(GL_SRC_ALPHA, GL_DST_ALPHA)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE);
    #
  # Set up rendering state for the offscreen buffer
    #glEnable(GL_DEPTH_TEST)
    #glDepthFunc(GL_LEQUAL)  
    #glClearColor(0.0, 0.0, 0.2, 0.5)
    #glClearDepth(1.0)    
    # Override default Escape key behaviour
    def on_key_press(symbol, modifiers):
        if symbol == key.ESCAPE:
            sys.exit()
    win.on_key_press = on_key_press
    #
    spawnWalls()
    #fixme:boxes need to be spawned before balls.  why?
    root = spriteEngine.get_root()
    #spawnBoxes(root) ;
    spawnBalls(root) ;
    #spawnApple(root) ;
    spawnApple() ;
    spawnWyggles(root) ;
    intervalTime = 10
    #var intervalTime = 1
    #spriteEngineInterval = window.setInterval("spriteEngine_step() ;", intervalTime)
    imgName = "grass"
    imgSrc = data.filepath(imgName + ".png")
    element = image.load(imgSrc)

    while not win.has_exit:
        win.dispatch_events()   
        # Update
        dt = clock.tick()
        #
        win.clear()
        #
        #element.blit(0, 0, 0)
        blitY = 0
        while(blitY < worldMaxY):
            blitX = 0            
            while(blitX < worldMaxX):    
                element.blit(blitX, blitY, 0)
                blitX = blitX + element.width
            blitY = blitY + element.height
        #
        spriteEngine.step(dt)
        win.flip()

    
main()