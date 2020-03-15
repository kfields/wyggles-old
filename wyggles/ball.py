
import math
 
from wyggles.sprite.sprite import Sprite
from wyggles.sprite.engine import *
from wyggles.sprite.body import *
from wyggles.sprite.beacon import *

class Ball(Sprite):
    def __init__(self, layer):
        Sprite.__init__(self, layer)
        self.setSize(22,22)        
        self.type = 'ball'
        self.name = spriteEngine.genId(self.type) ;                
        self.createSprite(self.name, self.type)
        #
        self.beacon = Beacon(self, self.type)
        spriteEngine.addBeacon(self.beacon)
        #
        self.body = BallBody(self)
        self.body.setSize(22,22,50)
        spriteEngine.addBody(self.body)

    def receiveKick(self, angle, distance):
        px = distance*(math.cos(angle*degRads))
        py = distance*(math.sin(angle*degRads))        
        self.body.addForce(px, py)
