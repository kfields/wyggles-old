import math
import data
from pyglet import image
from wyggles.mathutils import *

class Sprite():
    def __init__(self, layer):
        self.layer = layer
        self.body = None
        self.beacon = None
        self.heading = 0
        self.x = 0
        self.y = 0
        self.z = 0
        #
        self.fromX = 0
        self.fromY = 0
        self.toX = 0
        self.toY = 0    
        #
        self.halfWidth = 0
        self.halfHeight = 0
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0        
        #
        self.energy = 5
        #
        self.octant = (math.pi*2)/8
        #                
        layer.add_sprite(self)

    def createSprite(self, elementId, imgName):
        self.setImageSrc(imgName) ;

    def setImageSrc(self, imgName):
        self.imgSrc = data.filepath(imgName + ".png")
        self.element = image.load(self.imgSrc)
        
    def moveTo(self, x, y):
        self.fromX = self.x
        self.fromY = self.y
        self.toX = x
        self.toY = y                

    def setPos(self, x, y):
        self._setPos(x,y)
        if(self.body != None):
            self.body.setPos(x, y)

    def _setPos(self, x, y):
        self.x = x
        self.y = y
        #
        self.validate()

    def validate(self):
        self._validate()

    def _validate(self):
        self.minX = self.x - self.halfWidth
        self.minY = self.y - self.halfHeight
        self.maxX = self.x + self.halfWidth
        self.maxY = self.y + self.halfHeight
        #
        if(self.beacon != None):
            self.beacon.setPos(self.x, self.y)
        #
        #self.element.style.left = str(int(self.minX)) + "px"
        #self.element.style.top = str(int(self.minY)) + "px"
        #
        #self.render()

    def setOrigin(self, x, y):
        self.setPos(x, y)
        self.fromX = x
        self.fromY = y        
        self.toX = x
        self.toY = y        

    def setZ(self, z):
        self.z = z
        self.layer.depth_sort()
        #self.element.style.zindex = z

    def getZ(self):
        return self.z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setSize(self, width, height):
        self.halfWidth = width / 2
        self.halfHeight = height / 2

    def intersects(self, sprite):
        if(self.minX > sprite.maxX):
            return False
        if(self.minY > sprite.maxY):
            return False
        if(sprite.minX > self.maxX):
            return False
        if(sprite.minY > self.maxY):
            return False        
        return True

    def show(self):
        #self.element.style.display = 'block'
        pass

    def hide(self):
        #self.element.style.display = 'none' ;
        pass

    def materializeAt(self, x, y):
        self.setOrigin(x, y)
        self.show()

    def turnLeft(self, angleDelta):
        angle = self.heading - angleDelta
        if(angle < 0):
            self.heading = 360+angle
        else:
            self.heading = angle

    def turnRight(self, angleDelta):
        angle = self.heading + angleDelta
        if(angle > 359):
            self.heading = angle-360
        else:
            self.heading = angle

    def project(self, distance):
        px = self.x+(distance*(math.cos(self.heading*degRads)))
        py = self.y+(distance*(math.sin(self.heading*degRads)))
        self.moveTo(px, py) ;

    def atGoal(self):
        bDistance = distance2d(self.x, self.y, self.toX, self.toY)
        return bDistance < 5

    def step(self):
        pass
    
    def move(self):
        pass

    def render(self):
        element = self.element
        #self.element.blit(self.x, self.y, self.z)
        #self.element.blit(self.x, self.y, 0)
        #element = self.element
        #element.blit(self.x - element.width / 2, self.y - element.height / 2, 0)
        element.blit(self.x - element.width / 2, self.y - element.height / 2, self.z)