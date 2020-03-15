

import math
from random import random

from wyggles.sprite.sprite import Sprite
from wyggles.sprite.engine import *
from wyggles.sprite.body import *
from wyggles.sprite.beacon import *

class WyggleSeg(Sprite):
    def __init__(self, layer):
        Sprite.__init__(self, layer)
        self.setSize(22,22)
        self.next = None
        self.trackNdx = 0
        self.trackMax = 132
        self.onTrack = False
        self.track = None

    def putOnTrack(self, track):
        self.track = track
        self.onTrack = True
        self.materializeAt(track[self.trackNdx*2], track[self.trackNdx*2+1])

    def step(self):
        self.move()

    def move(self):
        self._move()

    def _move(self):
        self.setPos(self.track[self.trackNdx*2], self.track[self.trackNdx*2+1])    
        self.trackNdx += 1
        if(self.trackNdx >= self.trackMax):
            self.trackNdx = 0
        if(self.next == None):
            return ; #early out.
        #else
        if(self.next.onTrack == True):#another early out.
            self.next.step()
            return
        #else if there is a next wig and not on the track yet...
        if(self.trackNdx > 16):
              self.next.putOnTrack(self.track)
        return True ;
#
class WyggleTail(WyggleSeg):
    def __init__(self, layer, type):
        WyggleSeg.__init__(self, layer)
        self.type = type
        self.name = spriteEngine.genId(type)                
        self.createSprite(self.name, type + 'tail')
#////////////////
wigglySteering = [
    0, -1,
    1, -1,
    1, 0,
    #
    -1, -1,
    0, -1,
    1, -1,
    #
    -1, 0,
    -1, -1,
    0, -1,
    #
    -1, 1,
    -1, 0,
    -1, -1,
    #
    0, 1,
    -1, 1,
    -1, 0,
    #
    1, 1,
    0, 1,
    -1, 1,
    #
    1, 0,
    1, 1,
    0, 1,
    #
    1, -1,
    1, 0,
    1, 1
]
#
class WyggleHead(WyggleSeg):
    def __init__(self, layer):
        WyggleSeg.__init__(self, layer)
        self.face = 'happy'

    def happyFace(self):
        self.face = 'happy'
        self.setImageSrc(self.type + 'head')

    def munchyFace(self):
        self.face = 'munchy'
        self.setImageSrc(self.type + 'munch')

    def openMouth(self):
        self.munchyFace()

    def closeMouth(self):
        self.happyFace()
#
class Wyggle(WyggleHead):                                                                 
    def __init__(self, layer, type):
        WyggleHead.__init__(self, layer)
        self.type = type
        self.name = spriteEngine.genId(type)
        self.lengthMax = 6 
        self.segs = []
        self.preLoad()
        self.createSprite(self.name, type + 'head')
        self.sensorRange = 128
        self.wheel = 0
        self.state = 'wanderer'
        #
        self.segs.append(self)        
        self.track = [None] * self.trackMax*2
        self.length = 1
        self.butt = None
        #
        self.considerMax = 10
        self.considerTimer = self.considerMax
        self.focus = None
        #
        self.munchTimer = 10
        #
        self.grow()
        self.grow()
        self.grow()
        self.grow()
        self.grow()
        #
        spriteEngine.addActor(self)

    def preLoad(self):
        pass

    def grow(self):
        length = len(self.segs)
        if(length == self.lengthMax):
            return
        seg = WyggleTail(self.layer, self.type)
        self.segs.append(seg)
        length = len(self.segs)
        self.length = length
        #seg.setZ(-length)
        seg.setZ(-.001 * length)
        
        wasButt = self.butt
        self.butt = seg
        if(wasButt != None):
            wasButt.next = self.butt ;
        else:
            self.next = self.butt ;

    def changeState(self, state):
        self.state = state

    def microLeftTurn(self):
        ph = self.wheel - 1
        if(ph < 0 ):
            ph = 0
        self.wheel = ph ;

    def microRightTurn(self):
        ph = self.wheel + 1
        if(ph > 2):
            ph = 2
        self.wheel = ph ;

    def step(self):
        state = self.state
        if(state == 'wanderer'):
            self.wander()
        elif(state == 'hunter'):
            self.hunt() ;
        elif(state == 'eater'):
            self.eat()
        elif(state == 'kicker'):
            self.kick()

    def wander(self):
        if(self.atGoal()):
            pt = math.floor(random()*3)
            pd = math.floor(random()*45)
            if(pt == 0):
                self.turnLeft(pd)
            elif(pt == 2):
                self.turnRight(pd)
            else:
                pass
            self.project(self.sensorRange)
        self.move()
        self.consider()

    def hunt(self):
        if(self.intersects(self.focus)):
            self.changeState('eater')
        self.move()
        self.consider()

    def eat(self):
        if(self.focus.isMunched()):
            self.closeMouth() ;
            self.energy = self.energy + self.focus.energy
            self.changeState('wanderer')
            return
        #else
        self.munch()

    def munch(self):
        if(self.munchTimer > 0):
            self.munchTimer -=1 
            return
        else:
            self.munchTimer = 10
            
        if(self.face != 'munchy'):
            self.openMouth()
        else:
            self.closeMouth()
            self.focus.receiveMunch()

    def kick(self):
        self.moveTo(self.focus.x, self.focus.y) #fixme: add--> follow(sprite)
        if(self.intersects(self.focus)):
            self.focus.receiveKick(self.heading, self.sensorRange)            
        elif(distance2d(self.x, self.y, self.focus.x, self.focus.y) > self.sensorRange):
            self.changeState('wanderer') 
        self.move()

    def move(self):
        x = self.getX()
        y = self.getY()        
        steeringNdx = 0
        bCompass = math.pi+(math.atan2(y - self.toY, x - self.toX))
        if(bCompass != 0):
            steeringNdx = 8 - int(round(bCompass/self.octant))
        if(steeringNdx < 0):
            steeringNdx = 0            
        elif(steeringNdx > 7):
            steeringNdx = 7
        #
        pd = math.floor(random()*3)
        #
        if(pd == 0):
            self.microLeftTurn() ;
        elif(pd == 2):
            self.microRightTurn() ;
        else:
            pass
        #
        steeringNdx = steeringNdx*6
        steeringNdx = steeringNdx + (self.wheel * 2)
        #
        deltaX = wigglySteering[steeringNdx]
        deltaY = wigglySteering[steeringNdx + 1]

        self.tryMove(deltaX, deltaY)

    def tryMove(self, deltaX, deltaY):
        nextX = 0
        nextY = 0
        needTurn = False
        #
        if(self.minX < worldMinX):
            deltaX = -self.minX
            needTurn = True
        elif(self.maxX > worldMaxX):
            deltaX = worldMaxX - self.maxX
            needTurn = True
        #
        if(self.minY < worldMinY):
            deltaY = worldMinY - self.minY
            needTurn = True
        elif(self.maxY > worldMaxY):
            deltaY = worldMaxY - self.maxY
            needTurn = True
        #        
        if(needTurn):
            self.turnRight(45)
            self.project(self.sensorRange)
        #
        nextX = self.getX() + deltaX
        nextY = self.getY() + deltaY                    
        #
        self.track[self.trackNdx*2] = nextX
        self.track[self.trackNdx*2+1] = nextY
        self._move()

    def consider(self):
        if(self.considerTimer > 0):
            self.considerTimer -= 1
            return ;
        #else
        self.considerTimer = self.considerMax
        beacons = spriteEngine.query(self.x, self.y, self.sensorRange)
        #
        state = self.state
        if(state == 'wanderer'):
            if(not self.considerEating(beacons)):
                self.considerKicking(beacons)
        elif(state == 'hunter'):
            pass
        elif(state == 'eater'):
            pass
        elif(state == 'kicker'):
            pass
        #cleanup
        if(beacons != None):
            del beacons

    def considerEating(self, beacons):
        if(beacons == None):
            return False
        #else
        apple = None
        for beacon in beacons:  
            if(beacon.type == 'apple'):
                apple = beacon.sprite
                break
        #
        if(apple == None):
            return False
        #else
        self.focus = apple
        self.moveTo(apple.x, apple.y)
        self.changeState('hunter')
        return True

    def considerKicking(self, beacons):
        if(beacons == None):
            return False
        #else
        ball = None ;
        for beacon in beacons:
            if(beacon.type == 'ball'):
                ball = beacon.sprite
                break
        #
        if(ball == None):
            return False
        #else
        self.focus = ball
        self.moveTo(ball.x, ball.y)
        self.changeState('kicker')
        return True
