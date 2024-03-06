from lib import engine
import math

###############################################################################################################################################################

class ExplodableTile:
    def __init__(self, xPos, yPos, tileSize, tilemap, sdl):
        self.tileSize = tileSize
        self.active = True
        self.xPos = xPos
        self.yPos = yPos
        self.tilemap = tilemap
        self.sdl = sdl
        self.countDownMax = 200
        self.countDownNum = self.countDownMax

        self.tileObject = engine.GameObject()
        self.tilePhysics = engine.PhysicsComponent()
        self.tileTransform = engine.Transform()
        self.tileTransform.xPos = self.xPos
        self.tileTransform.yPos = self.yPos
        # (width of sprite, height of sprite, start x, start y, max num sprites in a row, total num sprites, numPixelsToTrimFromWidth)
        self.tile_sprite = engine.Sprite(self.tileTransform, True)
        self.tile_sprite.setRectangleDimensions(self.tileSize, self.tileSize)
        self.tile_sprite.setSpriteSheetDimensions(36, 36, 22, 70, 1, 1, 0)
        self.tile_sprite.loadImage('Assets/tilesets/Metroid_Tileset_2.png', self.sdl.getSDLRenderer())
        self.tile_sprite.update(0, 0, 0)
        self.tileObject.addTileMapComponent(self.tilemap)
        self.tileObject.addPhysicsComponent(self.tilePhysics)
        self.tileObject.addTransformComponent(self.tileTransform)
        self.tileObject.addSpriteComponent(self.tile_sprite)
    def decrementCountDown(self, obj):
        if not self.active:
            self.countDownNum -= 1
            if self.countDownNum <= 0:
                if not self.checkIfColliding(obj):
                    self.countDownNum = self.countDownMax
                    self.active = True
    def checkIfColliding(self, obj):
        x1 = self.tileObject.mTransform.xPos
        y1 = self.tileObject.mTransform.yPos
        width1 = self.tileObject.mSprite.getWidth()
        height1 = self.tileObject.mSprite.getHeight()
        x2 = obj.mTransform.xPos
        y2 = obj.mTransform.yPos
        width2 = obj.mSprite.getWidth()
        height2 = obj.mSprite.getHeight()
        if (x1 < x2 + width2 and x1 + width1 > x2 and
                y1 < y2 + height2 and y1 + height1 > y2):
            return True
        return False
    def isActive(self):
        return self.active
    # def getXPos(self):
    #     return self.xPos
    # def getYpos(self):
    #     return self.yPos
    def getTileObject(self):
        return self.tileObject
    def explodeTile(self):
        self.active = False
    
class Bomb:
    def __init__(self, tilemap, sdl):
        self.tilemap = tilemap
        self.sdl = sdl
        self.bombWidth = 16
        self.bombHeight = 16
        self.explosionWidth = 100
        self.explosionHeight = 100
        self.curFrameCount = 0
        self.bombFrameAddition = 0.5
        self.explosionFrameAddition = 0.5
        self.exploding = False
        self.destroy = False
        self.countDownNum = 26
        self.enemyArr = []
        self.bombExplodingSound = engine.Sound()
        self.bombExplodingSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (18).wav")

        self.bombObject = engine.GameObject()
        self.bombPhysics = engine.PhysicsComponent()
        self.bombTransform = engine.Transform()
        # (width of sprite, height of sprite, start x, start y, max num sprites in a row, total num sprites, numPixelsToTrimFromWidth)
        self.ticking_sprite = engine.Sprite(self.bombTransform, True)
        self.ticking_sprite.setRectangleDimensions(self.bombWidth, self.bombHeight)
        self.ticking_sprite.setSpriteSheetDimensions(16, 8, 336, 248, 2, 2, 8)
        self.ticking_sprite.loadImage('Assets/spritesheets/revamped_samus_sprites2.png', self.sdl.getSDLRenderer())
        self.explosion_sprite = engine.Sprite(self.bombTransform, True)
        self.explosion_sprite.setRectangleDimensions(self.explosionWidth, self.explosionHeight)
        self.explosion_sprite.setSpriteSheetDimensions(200, 200, 0, 0, 3, 7, 0)
        self.explosion_sprite.loadImage('Assets/spritesheets/explosion_1.png', self.sdl.getSDLRenderer())
        self.bombObject.addTileMapComponent(self.tilemap)
        self.bombObject.addPhysicsComponent(self.bombPhysics)
        self.bombObject.addTransformComponent(self.bombTransform)
        self.bombObject.addSpriteComponent(self.ticking_sprite)
    def changeToExplosionSprite(self):
        self.bombObject.addSpriteComponent(self.explosion_sprite)
        self.bombObject.mTransform.xPos = int(self.xPos + self.bombWidth/2 - self.explosionWidth/2)
        self.bombObject.mTransform.yPos = int(self.yPos + self.bombHeight/2 - self.explosionHeight/2)
        self.exploding = True
        self.bombExplodingSound.PlaySound()
        self.curFrameCount = -1
    def incrementCurrentFrameCount(self):
        if self.exploding:
            self.curFrameCount += self.explosionFrameAddition
            if int(self.curFrameCount) >= 7:
                self.destroy = True
        else:
            self.curFrameCount += self.bombFrameAddition
            if int(self.curFrameCount) >= 2:
                self.curFrameCount = 0
    def decrementCountDown(self):
        if not self.exploding:
            self.countDownNum -= 1
            if self.countDownNum <= 0:
                self.changeToExplosionSprite()
    def isTimeToDestroy(self):
        # if it is time to destroy, don't update the sprite
        return self.destroy
    def getCurrentFrameCount(self):
        # must convert to int to use for sprite
        return self.curFrameCount
    def isExploding(self):
        return self.exploding
    def getBombWidth(self):
        return self.bombWidth
    def getBombHeight(self):
        return self.bombHeight
    def setBombPosition(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.bombTransform.xPos = xPos
        self.bombTransform.yPos = yPos
    def getBombObject(self):
        return self.bombObject
    def getEnemyArr(self):
        return self.enemyArr
    def addEnemyToHitArray(self, enemyString):
        self.enemyArr.append(enemyString)


class Zoomer:
    def __init__(self, zoomerObject, origOrientation, isClockwise):
        self.zoomerObject = zoomerObject
        self.spriteArr = []
        self.maxFrameCountArr = []
        self.curFrameCount = 0
        self.hitPoints = 4
        self.active = True
        self.origIsClockwise = isClockwise
        self.originalXPos = self.zoomerObject.mTransform.xPos
        self.originalYPos = self.zoomerObject.mTransform.yPos
        self.isClockwise = isClockwise
        self.zoomerSpeed = 3
        self.origOrientation = origOrientation
        self.curOrientation = origOrientation
        self.xVelocityCWArr = [self.zoomerSpeed, -self.zoomerSpeed, -self.zoomerSpeed, self.zoomerSpeed]
        self.yVelocityCWArr = [self.zoomerSpeed, self.zoomerSpeed, -self.zoomerSpeed, -self.zoomerSpeed]
        self.xVelocityCCWArr = [-self.zoomerSpeed, self.zoomerSpeed, self.zoomerSpeed, -self.zoomerSpeed]
        self.yVelocityCCWArr = [self.zoomerSpeed, -self.zoomerSpeed, -self.zoomerSpeed, self.zoomerSpeed]
        self.zoomerHitSound = engine.Sound()
        self.zoomerHitSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (4).wav")
    def addSpriteToList(self, sprite, maxFrameCount):
        self.spriteArr.append(sprite)
        self.maxFrameCountArr.append(maxFrameCount)
    def incrementCurrentFrameCount(self, num, maxFrameCount):
        self.curFrameCount += num
        if int(self.curFrameCount) > maxFrameCount:
            self.curFrameCount = 0
    def decreaseHitPoints(self, posNum):
        self.hitPoints -= posNum
        self.zoomerHitSound.PlaySound()
        if self.hitPoints <= 0:
            self.setActiveStatus(False)
    def isGoingClockwise(self):
        return self.isClockwise
    def isActive(self):
        return self.active
    def setActiveStatus(self, isActive):
        if isActive == True:
            self.setCurrentSprite(0)
            self.zoomerObject.mTransform.xPos = self.originalXPos
            self.zoomerObject.mTransform.yPos = self.originalYPos
            self.curOrientation = self.origOrientation
            self.isClockwise = self.origIsClockwise
            if self.isClockwise:
                self.zoomerObject.xVel = self.xVelocityCWArr[self.curOrientation]
                self.zoomerObject.yVel = self.yVelocityCWArr[self.curOrientation]
            else:
                self.zoomerObject.xVel = self.xVelocityCCWArr[self.curOrientation]
                self.zoomerObject.yVel = self.yVelocityCCWArr[self.curOrientation]
            self.hitPoints = 4
            self.active = True
        else:
            self.active = False
    def reverseClockwiseDirection(self):
        self.isClockwise = not self.isClockwise
    def setCurrentSprite(self, idx):
        self.zoomerObject.addSpriteComponent(self.spriteArr[idx])
    def getCurrentXVelocity(self):
        if self.isClockwise:
            return self.xVelocityCWArr[self.curOrientation]
        else:
            return self.xVelocityCCWArr[self.curOrientation]
    def getCurrentYVelocity(self):
        if self.isClockwise:
            return self.yVelocityCWArr[self.curOrientation]
        else:
            return self.yVelocityCCWArr[self.curOrientation]
    def incrementOrientation(self):
        self.curOrientation += 1
        if self.curOrientation > 3:
            self.curOrientation = 0
    def decrementOrientation(self):
        self.curOrientation -= 1
        if self.curOrientation < 0:
            self.curOrientation = 3
    def getCurrentOrientation(self):
        return self.curOrientation
    def getCurrentFrameCount(self):
        return self.curFrameCount
    def getMaxFrameCount(self, idx):
        return self.maxFrameCountArr[idx]
    def getZoomerObject(self):
        return self.zoomerObject
    def getOriginalYPos(self):
        return self.originalYPos
    def getOriginalXPos(self):
        return self.originalXPos
    def checkIfColliding(self, obj):
        x1 = self.zoomerObject.mTransform.xPos
        y1 = self.zoomerObject.mTransform.yPos
        width1 = self.zoomerObject.mSprite.getWidth()
        height1 = self.zoomerObject.mSprite.getHeight()
        x2 = obj.mTransform.xPos
        y2 = obj.mTransform.yPos
        width2 = obj.mSprite.getWidth()
        height2 = obj.mSprite.getHeight()
        if (x1 < x2 + width2 and x1 + width1 > x2 and
                y1 < y2 + height2 and y1 + height1 > y2):
            return True
        return False


class Bug:
    def __init__(self, bugObject, closeness, jumpHeight):
        self.bugObject = bugObject
        self.spriteArr = []
        self.maxFrameCountArr = []
        self.curFrameCount = 0
        self.hitPoints = 4
        self.curXDirection = 1 # 1 or -1
        self.closeness = closeness
        self.jumpHeight = jumpHeight
        self.active = True
        self.waitOneCycleForJumpUpdate = True
        self.originalXPos = self.bugObject.mTransform.xPos
        self.originalYPos = self.bugObject.mTransform.yPos
        self.bugHitSound = engine.Sound()
        self.bugHitSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (4).wav")
    def addSpriteToList(self, sprite, maxFrameCount):
        self.spriteArr.append(sprite)
        self.maxFrameCountArr.append(maxFrameCount)
    def incrementCurrentFrameCount(self, num, maxFrameCount):
        self.curFrameCount += num
        if int(self.curFrameCount) > maxFrameCount:
            self.curFrameCount = 0
    def decreaseHitPoints(self, posNum):
        self.hitPoints -= posNum
        self.bugHitSound.PlaySound()
        if self.hitPoints <= 0:
            self.setActiveStatus(False)
    def isActive(self):
        return self.active
    def setActiveStatus(self, isActive):
        if isActive == True:
            self.setCurrentSprite(0)
            self.bugObject.mTransform.xPos = self.originalXPos
            self.bugObject.mTransform.yPos = self.originalYPos
            self.bugObject.xVel = 0
            self.bugObject.yVel = 0
            self.bugObject.mJumpComponent.EndJump()
            self.hitPoints = 4
            self.active = True
        else:
            self.active = False
    def setCurrentSprite(self, idx):
        self.bugObject.addSpriteComponent(self.spriteArr[idx])
    def setCurrentXDirection(self, plusMinusDirection):
        self.curXDirection = plusMinusDirection
    def getCurrentXDirection(self):
        return self.curXDirection
    def getCurrentFrameCount(self):
        return self.curFrameCount
    def getMaxFrameCount(self, idx):
        return self.maxFrameCountArr[idx]
    def getCloseness(self):
        return self.closeness
    def getBugObject(self):
        return self.bugObject
    def getOriginalYPos(self):
        return self.originalYPos
    def checkIfColliding(self, obj):
        x1 = self.bugObject.mTransform.xPos
        y1 = self.bugObject.mTransform.yPos
        width1 = self.bugObject.mSprite.getWidth()
        height1 = self.bugObject.mSprite.getHeight()
        x2 = obj.mTransform.xPos
        y2 = obj.mTransform.yPos
        width2 = obj.mSprite.getWidth()
        height2 = obj.mSprite.getHeight()
        if (x1 < x2 + width2 and x1 + width1 > x2 and
                y1 < y2 + height2 and y1 + height1 > y2):
            return True
        return False
    

class BubbleDoor:
    def __init__(self, xPos, yPos, width, height, facingLeft):
        self.mSpriteArr = []
        self.mMaxFrameCountArr = []
        self.mSlowTimer = 0
        self.pauseTimer = 0
        self.maxPauseTimer = 50
        self.mSprite = None
        self.mMaxFrame = 1
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.isFacingLeft_ = facingLeft
        self.isClosed_ = True
        self.isOpening_ = False
        self.isClosing_ = False
        if facingLeft:
            self.cx = self.xPos + width
        else:
            self.cx = self.xPos
        self.cy = self.yPos + int(height/2)
        
    def addSpriteComponent(self, sprite, maxFrameCount):
        self.mSpriteArr.append(sprite)
        self.mMaxFrameCountArr.append(maxFrameCount)
    def getSpriteComponent(self):
        return self.mSprite
    def setCurrentSpriteComponent(self, idx):
        if idx < 0 or idx >= len(self.mSpriteArr):
            idx = 0
        self.mSprite = self.mSpriteArr[idx]
        self.mMaxFrame = self.mMaxFrameCountArr[idx]
    def advanceTimer(self):
        if self.isClosed_ == False: # Door is open
            self.pauseTimer += 1
        if self.isOpening_:
            self.mSlowTimer += 0.25
            if self.mSlowTimer >= self.mMaxFrame:
                self.isOpening_ = False
                self.mSlowTimer = 0
        elif self.isClosing_:
            self.mSlowTimer += 0.25
            if self.mSlowTimer >= self.mMaxFrame:
                self.isClosing_ = False
                self.isClosed_ = True
                self.mSlowTimer = 0
                self.setCurrentSpriteComponent(0)
    def isPauseTimerUp(self):
        return self.pauseTimer > self.maxPauseTimer
    def getFrameCount(self):
        return int(self.mSlowTimer)
    def getXPos(self):
        return self.xPos
    def getYPos(self):
        return self.yPos
    def getWidth(self):
        return self.width
    def openDoor(self):
        self.isOpening_ = True
        self.isClosed_ = False
        self.setCurrentSpriteComponent(1)
    def closeDoor(self):
        self.isClosing_ = True
        self.pauseTimer = 0
    def isClosed(self):
        return self.isClosed_
    def isClosing(self):
        return self.isClosing_
    def isOpening(self):
        return self.isOpening_
    def isFacingLeft(self):
        return self.isFacingLeft_
    def checkIfColliding(self, obj):
        #result = ((x - cx) ** 2) / (radius_x ** 2) + ((y - cy) ** 2) / (radius_y ** 2) <= 1
        h = self.height/2
        if self.isClosed_ == True:
            if self.isFacingLeft_:
                if self.yPos <= obj.mTransform.yPos + obj.mSprite.getHeight() <= self.yPos + h:
                    # top half of door
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = obj.mTransform.yPos + obj.mSprite.getHeight()
                    isColliding = ((x - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) <= 1
                    return isColliding
                elif self.yPos + h <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = obj.mTransform.yPos
                    isColliding = ((x - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) <= 1
                    return isColliding
                elif self.yPos - obj.mSprite.getHeight() + 1 <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # middle of door: use half of height for y
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = self.yPos + h
                    isColliding = ((x - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) <= 1
                    return isColliding
            else:
                # door facing right
                if self.yPos <= obj.mTransform.yPos + obj.mSprite.getHeight() <= self.yPos + h:
                    # top half of door
                    x = obj.mTransform.xPos
                    y = obj.mTransform.yPos + obj.mSprite.getHeight()
                    isColliding = ((x - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) <= 1
                    return isColliding
                elif self.yPos + h <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # bottom half of door
                    x = obj.mTransform.xPos
                    y = obj.mTransform.yPos
                    isColliding = ((x - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) <= 1
                    return isColliding
                elif self.yPos - obj.mSprite.getHeight() + 1 <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # middle of door: use half of height for y
                    x = obj.mTransform.xPos
                    y = self.yPos + h
                    isColliding = ((x - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) <= 1
                    return isColliding
        return False
    def getXDiff(self, obj):
        if self.isClosed_ == True:
            h = self.height/2
            if self.isFacingLeft_:
                # top half of door
                if self.yPos <= obj.mTransform.yPos + obj.mSprite.getHeight() <= self.yPos + h:
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = obj.mTransform.yPos + obj.mSprite.getHeight()
                    for i in range(1, 36):
                        if ((x - i - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) >= 1:
                            return -i
                elif self.yPos + h <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # bottom half of door
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = obj.mTransform.yPos
                    for i in range(1, 36):
                        if ((x - i - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) >= 1:
                            return -i
                elif self.yPos - obj.mSprite.getHeight() + 1 <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # middle of door: use half of height for y
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = self.yPos + h
                    for i in range(1, 36):
                        if ((x - i - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) >= 1:
                            return -i
            else:
                # top half of door
                if self.yPos <= obj.mTransform.yPos + obj.mSprite.getHeight() <= self.yPos + h:
                    x = obj.mTransform.xPos
                    y = obj.mTransform.yPos + obj.mSprite.getHeight()
                    for i in range(1, 36):
                        if ((x + i - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) >= 1:
                            return i
                elif self.yPos + h <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # bottom half of door
                    x = obj.mTransform.xPos
                    y = obj.mTransform.yPos
                    for i in range(1, 36):
                        if ((x + i - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) >= 1:
                            return i
                elif self.yPos - obj.mSprite.getHeight() + 1 <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # middle of door: use half of height for y
                    x = obj.mTransform.xPos
                    y = self.yPos + h
                    for i in range(1, 36):
                        if ((x + i - self.cx) ** 2) / (self.width ** 2) + ((y - self.cy) ** 2) / (h ** 2) >= 1:
                            return i
        return 0
    def getYDiff(self, obj):
        if self.isClosed_ == True:
            h = self.height/2
            if self.isFacingLeft_:
                # top half of door
                if self.yPos <= obj.mTransform.yPos + obj.mSprite.getHeight() <= self.yPos + h:
                    x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    y = obj.mTransform.yPos + obj.mSprite.getHeight()
                    for i in range(1, 60):
                        if ((x - self.cx) ** 2) / (self.width ** 2) + ((y - i - self.cy) ** 2) / (h ** 2) >= 1:
                            return -i
                elif self.yPos + h <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # bottom half of door
                    # x = obj.mTransform.xPos + obj.mSprite.getWidth()
                    # y = obj.mTransform.yPos
                    # for i in range(1, 60):
                    #     if ((x - self.cx) ** 2) / (self.width ** 2) + ((y + i - self.cy) ** 2) / (h ** 2) >= 1:
                    #         return i
                    return 0
                elif self.yPos - obj.mSprite.getHeight() + 1 <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # middle of door: use half of height for y
                    return 0
            else:
                # top half of door
                if self.yPos <= obj.mTransform.yPos + obj.mSprite.getHeight() <= self.yPos + h:
                    x = obj.mTransform.xPos
                    y = obj.mTransform.yPos + obj.mSprite.getHeight()
                    for i in range(1, 60):
                        if ((x - self.cx) ** 2) / (self.width ** 2) + ((y - i - self.cy) ** 2) / (h ** 2) >= 1:
                            return -i
                elif self.yPos + h <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # bottom half of door
                    # x = obj.mTransform.xPos
                    # y = obj.mTransform.yPos
                    # for i in range(1, 60):
                    #     if ((x - self.cx) ** 2) / (self.width ** 2) + ((y + i - self.cy) ** 2) / (h ** 2) >= 1:
                    #         return i
                    return 0
                elif self.yPos - obj.mSprite.getHeight() + 1 <= obj.mTransform.yPos <= self.yPos + self.height - 1:
                    # middle of door: use half of height for y
                    return 0
        return 0

class PlayerState:
    def __init__(self):
        self.state = "falling"
    def setState(self, s):
        self.state = s
    def getState(self):
        return self.state


# Represents a Metroid Game
class Game:
    # Initialize Game
    def __init__(self, windowWidth, windowHeight):
        # SDL Setup
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth # self.tileSize * 27 = 972
        self.windowHeight = windowHeight # self.tileSize * 20 = 720
        # Tilemap Setup
        self.tilemap1 = engine.TileMapComponent("Assets/Levels/BrinstarTiles/metroid_practice_1.lvl", 21, 70)
        self.tilemap1.loadTileset("Assets/tilesets/Metroid_Tileset_2.bmp", self.sdl.getSDLRenderer())
        self.tilemap2 = engine.TileMapComponent("Assets/Levels/BrinstarTiles/metroid_practice_2.lvl", 21, 70)
        self.tilemap2.loadTileset("Assets/tilesets/Metroid_Tileset_2.bmp", self.sdl.getSDLRenderer())
        self.tilemap3 = engine.TileMapComponent("Assets/Levels/BrinstarTiles/metroid_practice_3.lvl", 21, 70)
        self.tilemap3.loadTileset("Assets/tilesets/Metroid_Tileset_2.bmp", self.sdl.getSDLRenderer())
        self.tilemap4 = engine.TileMapComponent("Assets/Levels/BrinstarTiles/metroid_practice_4.lvl", 21, 70)
        self.tilemap4.loadTileset("Assets/tilesets/Metroid_Tileset_2.bmp", self.sdl.getSDLRenderer())
        # tilemap side or vertical dict
        self.sideOrVertDict = {}
        self.sideOrVertDict[str(self.tilemap1)] = "horizontal"
        self.sideOrVertDict[str(self.tilemap2)] = "horizontal"
        self.sideOrVertDict[str(self.tilemap3)] = "vertical"
        self.sideOrVertDict[str(self.tilemap4)] = "horizontal"
        # tilemap adjacency dict
        self.tilemapAdjacencyDict = {}
        self.tilemapAdjacencyDict[str(self.tilemap1)] = {"left1": None, "right1": self.tilemap2}
        self.tilemapAdjacencyDict[str(self.tilemap2)] = {"left1": self.tilemap1, "right1": self.tilemap3}
        self.tilemapAdjacencyDict[str(self.tilemap3)] = {"left1": self.tilemap2, "right1": self.tilemap4}
        self.tilemapAdjacencyDict[str(self.tilemap4)] = {"left1": self.tilemap3, "right1": None}
        # set self.tilemap
        self.tilemap = self.tilemap1 # TODO: switch back to tilemap1
        self.tileSize = self.tilemap.getSize() # 36

        # Level size
        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        # Physics Setup
        self.physics = engine.PhysicsComponent()
        # Entities to render
        self.entities = []

        # Player Object Setup
        self.player = engine.GameObject()
        self.playerStartXPos = 200
        # self.playerStartXPos = self.tilemap.getCols() * self.tileSize - (self.tileSize * 8)
        # self.playerStartYPos = self.tilemap3.getRows() * self.tileSize - 500 - (self.tileSize * 14)
        self.playerStartYPos = self.tilemap.getRows() * self.tileSize - (self.tileSize * 3) - 50
        # Player Transform Component
        self.playerTransform = engine.Transform()
        self.player.addTransformComponent(self.playerTransform)
        self.playerTransform.xPos = self.playerStartXPos
        self.playerTransform.yPos = self.playerStartYPos
        # Player Tilemap Component
        self.player.addTileMapComponent(self.tilemap)
        # Player Physics Component
        self.player.addPhysicsComponent(self.physics)
        #int _height, int _total_distance, float _xVelocity, int _gravity_factor
        self.playerJump = engine.JumpComponent(-200, 500, 6, -2)
        self.player.addJumpComponent(self.playerJump)
        # Setup PlayerState
        self.playerState = PlayerState()

        self.maxFrameDict = {}
        
        self.createPlayerSprites()

        self.lvlHeight1 = self.tilemap1.getRows() * self.tileSize
        self.lvlWidth1 = self.tilemap1.getCols() * self.tileSize
        self.lvlHeight2 = self.tilemap2.getRows() * self.tileSize
        self.lvlWidth2 = self.tilemap2.getCols() * self.tileSize
        self.lvlHeight3 = self.tilemap3.getRows() * self.tileSize
        self.lvlWidth3 = self.tilemap3.getCols() * self.tileSize
        self.lvlWidth4 = self.tilemap4.getCols() * self.tileSize
        self.lvlHeight4 = self.tilemap4.getRows() * self.tileSize
        # Door objects
        self.createDoorObjects()
        # Bubble Doors
        self.createBubbleDoorObjects()
        # Dictionary containing all monsters for level
        self.enemiesDict = {}
        
        # Flying monsters(bugs)
        self.createBugs()
        # Zoomers
        self.createZoomers()
        # powerup sprites
        self.createPowerUpObjects()
        # explodable tiles
        self.createExplodableTiles()

        # Camera Setup
        self.camera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth, 
                                                 self.lvlHeight, self.player.mSprite)
        #self.camera = engine.SpriteVerticalScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth, 
        #                                        self.lvlHeight, self.player.mSprite)
        self.cameraOffsetX = 0
        self.cameraOffsetY = 0

        '''
        Need to keep track of number of frames in the sprite sheet. 
        '''
        self.currentFrame = 0
        self.currentMaxFrame = self.maxFrameDict[str(self.idle_right)]

        # Sounds
        self.music = engine.Music()
        self.music.SetMusic("Assets/Sounds/78 - Brinstar (Rock Stage).mp3")
        self.bombCreatedSound = engine.Sound()
        self.bombCreatedSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (2).wav")
        self.bulletCreatedSound = engine.Sound()
        self.bulletCreatedSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (3).wav")
        self.doorPoppingSound = engine.Sound()
        self.doorPoppingSound.SetSound("Assets/Sounds/Metroid_sounds/liquid-bubble.wav")
        self.doorInflatingSound = engine.Sound()
        self.doorInflatingSound.SetSound("Assets/Sounds/Metroid_sounds/bubble_single_short.mp3")
        self.playerJumpSound = engine.Sound()
        self.playerJumpSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (6).wav")
        self.powerUpSound = engine.Sound()
        self.powerUpSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (16).wav")
        self.playerHitSound = engine.Sound()
        self.playerHitSound.SetSound("Assets/Sounds/Metroid_sounds/Misc_17.wav")
        

        # Player Settings
        self.playerRunSpeed = 6
        self.playerFallingSpeed = 10
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
        self.diffBetweenStandingAndDucking = abs(self.aim_up_idle_right.getHeight() - self.duck_right.getHeight())
        self.diffBetweenDuckingAndRolling = abs(self.duck_right.getHeight() - self.roll_right.getHeight())
        self.diffBetweenStandingAndFalling = abs(self.idle_right.getHeight() - self.falling_right.getHeight())
        
        self.isFirstRollingFrame = False
        self.waitOneCycleForJumpUpdate = False
        self.waitOneCycleToInitiateJump = False
        self.uprightJump = False
        self.isFirstStandingFrame = False
        self.shootingCounterMax = 10
        self.shootingCounter = self.shootingCounterMax + 1
        self.playerIsHit = False
        self.backupLeft = False
        self.backupRight = False
        self.hitTimer = 0 
        self.maxHitTimer = 15
        self.backupXDiff = 4
        self.hasScrewAttack = False
        self.jumpTimerMax = 10
        self.jumpTimer = 0
        self.playerCannotBeHit = False
        self.playerCannotBeHitTimer = 0
        self.playerCannotBeHitMax = 30

        # Variables for bullets
        self.bulletDict = {}
        self.bulletSpeed = 12
        self.shotPauseMax = 5
        self.shotPauseTimer = self.shotPauseMax + 1
        self.shotLifeMax = 30
        self.bulletIndex = 0
        self.spriteDict = {}
        self.transformDict = {}
        self.physicsDict = {}
        self.waitOneFrameForShot = True

        # Bomb variables
        self.bombArr = []
        self.numFramesBetweenBombs = 8
        self.countDownBetweenBombs = 0

        # Game Variables
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerFallingSpeed
        self.bugFrameIncrement = 0.33334
        self.zoomerFrameIncrement = 0.25
        
        # Frame capping variables
        targetFPS = 40 # TODO: set back to 40
        self.maxTicksPerFrame = int(1000 / targetFPS); # 16.66ms per frame?
        self.frameStartTime = 0
        self.frame_count = 0
        self.startTime = self.sdl.getTimeMS()
        self.frameUpdateDelay = 0
        self.maxFrameUpdateDelay = 2

    def createPlayerSprites(self):
        '''
        CREATE A SPRITE
        Spritesheets should be located in the Assets folder. Use the "loadImage"
        function to import one.
        "setRectangleDimensions" sets the size of the sprite on the screen.
        
        "setSpriteSheetDimensions" is for correctly iterating through the spritesheet.
        (width of sprite, height of sprite, start x, start y, max num sprites in a row, total num sprites, numPixelsToTrimFromWidth)
        numPixelsToTrimFromWidth : this parameter tells how many pixels are to be taken off each sprite image, in case
        there is extra space between images.
        '''
        self.run_right_sprite = engine.Sprite(self.playerTransform, True)
        self.run_right_sprite.setRectangleDimensions(34, 60)
        self.run_right_sprite.setSpriteSheetDimensions(20, 32, 135, 117, 3, 3, 0)
        self.run_right_sprite.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.run_right_sprite)
        self.maxFrameDict[str(self.run_right_sprite)] = 2

        self.run_left_sprite = engine.Sprite(self.playerTransform, True)
        self.run_left_sprite.setRectangleDimensions(34, 60)
        self.run_left_sprite.setSpriteSheetDimensions(20, 32, 68, 117, 3, 3, 0)
        self.run_left_sprite.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_sprite)] = 2

        self.idle_right = engine.Sprite(self.playerTransform, True)
        self.idle_right.setRectangleDimensions(34, 60)
        self.idle_right.setSpriteSheetDimensions(22, 32, 137, 40, 1, 1, 0)
        self.idle_right.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right)] = 0

        self.idle_left = engine.Sprite(self.playerTransform, True)
        self.idle_left.setRectangleDimensions(34, 60) # used to be 30, 40
        self.idle_left.setSpriteSheetDimensions(22, 32, 109, 40, 1, 1, 0) # Change: 109
        self.idle_left.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left)] = 0

        self.duck_right = engine.Sprite(self.playerTransform, True)
        self.duck_right.setRectangleDimensions(34, 40) # used to be 30, 32
        self.duck_right.setSpriteSheetDimensions(22, 23, 181, 50, 1, 1, 0)
        self.duck_right.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.duck_right)] = 0

        self.duck_left = engine.Sprite(self.playerTransform, True)
        self.duck_left.setRectangleDimensions(34, 40)
        self.duck_left.setSpriteSheetDimensions(22, 23, 63, 50, 1, 1, 0)
        self.duck_left.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.duck_left)] = 0

        self.roll_right = engine.Sprite(self.playerTransform, True)
        self.roll_right.setRectangleDimensions(32, 32)
        self.roll_right.setSpriteSheetDimensions(15, 15, 135, 150, 4, 4, 0)
        self.roll_right.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.roll_right)] = 3

        self.roll_left = engine.Sprite(self.playerTransform, False)
        self.roll_left.setRectangleDimensions(32, 32) # used to be 26, 26
        self.roll_left.setSpriteSheetDimensions(15, 15, 131, 150, 4, 4, 0)
        self.roll_left.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.roll_left)] = 3

        self.somersault_right = engine.Sprite(self.playerTransform, True)
        self.somersault_right.setRectangleDimensions(38, 42) # used to be 30, 32
        self.somersault_right.setSpriteSheetDimensions(19, 26, 135, 195, 4, 4, 0)
        self.somersault_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.somersault_right)] = 3

        self.somersault_left = engine.Sprite(self.playerTransform, False)
        self.somersault_left.setRectangleDimensions(38, 42)
        self.somersault_left.setSpriteSheetDimensions(20, 26, 133, 195, 4, 4, 2)
        self.somersault_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.somersault_left)] = 3

        self.falling_right = engine.Sprite(self.playerTransform, True)
        self.falling_right.setRectangleDimensions(34, 55) # used to be 30, 38
        self.falling_right.setSpriteSheetDimensions(22, 27, 135, 168, 1, 1, 0)
        self.falling_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.falling_right)] = 0

        self.falling_left = engine.Sprite(self.playerTransform, False)
        self.falling_left.setRectangleDimensions(34, 55)
        self.falling_left.setSpriteSheetDimensions(22, 27, 131, 168, 1, 1, 0)
        self.falling_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.falling_left)] = 0

        self.aim_up_idle_right = engine.Sprite(self.playerTransform, True)
        self.aim_up_idle_right.setRectangleDimensions(30, 67)
        self.aim_up_idle_right.setSpriteSheetDimensions(16, 37, 137, 76, 1, 1, 0)
        self.aim_up_idle_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.aim_up_idle_right)] = 0

        self.aim_up_idle_left = engine.Sprite(self.playerTransform, True)
        self.aim_up_idle_left.setRectangleDimensions(30, 67)
        self.aim_up_idle_left.setSpriteSheetDimensions(16, 37, 115, 76, 1, 1, 0)
        self.aim_up_idle_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.aim_up_idle_left)] = 0

        self.aim_up_run_right = engine.Sprite(self.playerTransform, True)
        self.aim_up_run_right.setRectangleDimensions(30, 67)
        self.aim_up_run_right.setSpriteSheetDimensions(19, 38, 134, 284, 3, 3, 1)
        self.aim_up_run_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.aim_up_run_right)] = 2

        self.aim_up_run_left = engine.Sprite(self.playerTransform, True)
        self.aim_up_run_left.setRectangleDimensions(30, 67)
        self.aim_up_run_left.setSpriteSheetDimensions(19, 38, 72, 284, 3, 3, 0)
        self.aim_up_run_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.aim_up_run_left)] = 2

        self.aim_up_falling_right = engine.Sprite(self.playerTransform, True)
        self.aim_up_falling_right.setRectangleDimensions(34, 58) # used to be 30, 38
        self.aim_up_falling_right.setSpriteSheetDimensions(22, 31, 135, 325, 1, 1, 0)
        self.aim_up_falling_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.aim_up_falling_right)] = 0

        self.aim_up_falling_left = engine.Sprite(self.playerTransform, False)
        self.aim_up_falling_left.setRectangleDimensions(34, 58)
        self.aim_up_falling_left.setSpriteSheetDimensions(22, 31, 131, 327, 1, 1, 0)
        self.aim_up_falling_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.aim_up_falling_left)] = 0

        self.shooting_run_right = engine.Sprite(self.playerTransform, True)
        self.shooting_run_right = engine.Sprite(self.playerTransform, True)
        self.shooting_run_right.setRectangleDimensions(40, 60)
        self.shooting_run_right.setSpriteSheetDimensions(25, 32, 135, 221, 3, 3, 0)
        self.shooting_run_right.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.shooting_run_right)
        self.maxFrameDict[str(self.shooting_run_right)] = 2

        self.shooting_run_left = engine.Sprite(self.playerTransform, True)
        self.shooting_run_left.setRectangleDimensions(40, 60)
        self.shooting_run_left.setSpriteSheetDimensions(25, 32, 55, 221, 3, 3, 0)
        self.shooting_run_left.loadImage("Assets/spritesheets/MetroidSpritesheet2.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.shooting_run_left)] = 2

        self.shooting_falling_right = engine.Sprite(self.playerTransform, True)
        self.shooting_falling_right.setRectangleDimensions(34, 55) 
        self.shooting_falling_right.setSpriteSheetDimensions(25, 27, 135, 255, 1, 1, 0)
        self.shooting_falling_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.shooting_falling_right)] = 0

        self.shooting_falling_left = engine.Sprite(self.playerTransform, False)
        self.shooting_falling_left.setRectangleDimensions(34, 55)
        self.shooting_falling_left.setSpriteSheetDimensions(25, 27, 131, 255, 1, 1, 0)
        self.shooting_falling_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.shooting_falling_left)] = 0

        self.screw_attack_left = engine.Sprite(self.playerTransform, True)
        self.screw_attack_left.setRectangleDimensions(48, 48)
        self.screw_attack_left.setSpriteSheetDimensions(33, 35, 136, 400, 4, 4, 0)
        self.screw_attack_left.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.screw_attack_left)] = 3

        self.screw_attack_right = engine.Sprite(self.playerTransform, True)
        self.screw_attack_right.setRectangleDimensions(48, 48)
        self.screw_attack_right.setSpriteSheetDimensions(33, 35, 1, 400, 4, 4, 0)
        self.screw_attack_right.loadImage('Assets/spritesheets/MetroidSpritesheet2.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.screw_attack_right)] = 3

    def createDoorObjects(self):
        self.doorObjectsDict = {}

        self.doorObject = engine.GameObject()
        self.doorPhysics = engine.PhysicsComponent()
        self.doorTransform = engine.Transform()
        self.doorTransform.xPos = self.lvlWidth1 - self.tileSize + 1
        self.doorTransform.yPos = self.lvlHeight1 - (self.tileSize * 7)
        self.door_block_sprite = engine.Sprite(self.doorTransform, True)
        self.door_block_sprite.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject.addTileMapComponent(self.tilemap1)
        self.doorObject.addPhysicsComponent(self.doorPhysics)
        self.doorObject.addTransformComponent(self.doorTransform)
        self.doorObject.addSpriteComponent(self.door_block_sprite)

        self.doorObject2 = engine.GameObject()
        self.doorPhysics2 = engine.PhysicsComponent()
        self.doorTransform2 = engine.Transform()
        self.doorTransform2.xPos = self.lvlWidth1 - self.tileSize + 1
        self.doorTransform2.yPos = self.lvlHeight1 - (self.tileSize * 8)
        self.door_block_sprite2 = engine.Sprite(self.doorTransform2, True)
        self.door_block_sprite2.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite2.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject2.addTileMapComponent(self.tilemap1)
        self.doorObject2.addPhysicsComponent(self.doorPhysics2)
        self.doorObject2.addTransformComponent(self.doorTransform2)
        self.doorObject2.addSpriteComponent(self.door_block_sprite2)

        self.doorObject3 = engine.GameObject()
        self.doorPhysics3 = engine.PhysicsComponent()
        self.doorTransform3 = engine.Transform()
        self.doorTransform3.xPos = self.lvlWidth1 - self.tileSize + 1
        self.doorTransform3.yPos = self.lvlHeight1 - (self.tileSize * 9)
        self.door_block_sprite3 = engine.Sprite(self.doorTransform3, True)
        self.door_block_sprite3.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite3.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite3.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject3.addTileMapComponent(self.tilemap1)
        self.doorObject3.addPhysicsComponent(self.doorPhysics3)
        self.doorObject3.addTransformComponent(self.doorTransform3)
        self.doorObject3.addSpriteComponent(self.door_block_sprite3)

        self.doorObjectsDict[str(self.tilemap1)] = [self.doorObject, self.doorObject2, self.doorObject3]

        self.doorObject4 = engine.GameObject()
        self.doorPhysics4 = engine.PhysicsComponent()
        self.doorTransform4 = engine.Transform()
        self.doorTransform4.xPos = 0
        self.doorTransform4.yPos = self.lvlHeight2 - (self.tileSize * 7)
        self.door_block_sprite4 = engine.Sprite(self.doorTransform4, True)
        self.door_block_sprite4.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite4.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite4.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject4.addTileMapComponent(self.tilemap2)
        self.doorObject4.addPhysicsComponent(self.doorPhysics4)
        self.doorObject4.addTransformComponent(self.doorTransform4)
        self.doorObject4.addSpriteComponent(self.door_block_sprite4)

        self.doorObject5 = engine.GameObject()
        self.doorPhysics5 = engine.PhysicsComponent()
        self.doorTransform5 = engine.Transform()
        self.doorTransform5.xPos = 0
        self.doorTransform5.yPos = self.lvlHeight2 - (self.tileSize * 8)
        self.door_block_sprite5 = engine.Sprite(self.doorTransform5, True)
        self.door_block_sprite5.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite5.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite5.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject5.addTileMapComponent(self.tilemap2)
        self.doorObject5.addPhysicsComponent(self.doorPhysics5)
        self.doorObject5.addTransformComponent(self.doorTransform5)
        self.doorObject5.addSpriteComponent(self.door_block_sprite5)

        self.doorObject6 = engine.GameObject()
        self.doorPhysics6 = engine.PhysicsComponent()
        self.doorTransform6 = engine.Transform()
        self.doorTransform6.xPos = 0
        self.doorTransform6.yPos = self.lvlHeight2 - (self.tileSize * 9)
        self.door_block_sprite6 = engine.Sprite(self.doorTransform6, True)
        self.door_block_sprite6.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite6.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite6.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject6.addTileMapComponent(self.tilemap2)
        self.doorObject6.addPhysicsComponent(self.doorPhysics6)
        self.doorObject6.addTransformComponent(self.doorTransform6)
        self.doorObject6.addSpriteComponent(self.door_block_sprite6)

        self.doorObjectsDict[str(self.tilemap2)] = [self.doorObject4, self.doorObject5, self.doorObject6]

        self.doorObject7 = engine.GameObject()
        self.doorPhysics7 = engine.PhysicsComponent()
        self.doorTransform7 = engine.Transform()
        self.doorTransform7.xPos = self.lvlWidth2 - self.tileSize + 1
        self.doorTransform7.yPos = self.lvlHeight2 - (self.tileSize * 7)
        self.door_block_sprite7 = engine.Sprite(self.doorTransform7, True)
        self.door_block_sprite7.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite7.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite7.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject7.addTileMapComponent(self.tilemap2)
        self.doorObject7.addPhysicsComponent(self.doorPhysics7)
        self.doorObject7.addTransformComponent(self.doorTransform7)
        self.doorObject7.addSpriteComponent(self.door_block_sprite7)

        self.doorObject8 = engine.GameObject()
        self.doorPhysics8 = engine.PhysicsComponent()
        self.doorTransform8 = engine.Transform()
        self.doorTransform8.xPos = self.lvlWidth2 - self.tileSize + 1
        self.doorTransform8.yPos = self.lvlHeight2 - (self.tileSize * 8)
        self.door_block_sprite8 = engine.Sprite(self.doorTransform8, True)
        self.door_block_sprite8.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite8.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite8.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject8.addTileMapComponent(self.tilemap2)
        self.doorObject8.addPhysicsComponent(self.doorPhysics8)
        self.doorObject8.addTransformComponent(self.doorTransform8)
        self.doorObject8.addSpriteComponent(self.door_block_sprite8)

        self.doorObject9 = engine.GameObject()
        self.doorPhysics9 = engine.PhysicsComponent()
        self.doorTransform9 = engine.Transform()
        self.doorTransform9.xPos = self.lvlWidth2 - self.tileSize + 1
        self.doorTransform9.yPos = self.lvlHeight2 - (self.tileSize * 9)
        self.door_block_sprite9 = engine.Sprite(self.doorTransform9, True)
        self.door_block_sprite9.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite9.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite9.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject9.addTileMapComponent(self.tilemap2)
        self.doorObject9.addPhysicsComponent(self.doorPhysics9)
        self.doorObject9.addTransformComponent(self.doorTransform9)
        self.doorObject9.addSpriteComponent(self.door_block_sprite9)

        self.doorObjectsDict[str(self.tilemap2)].append(self.doorObject7)
        self.doorObjectsDict[str(self.tilemap2)].append(self.doorObject8)
        self.doorObjectsDict[str(self.tilemap2)].append(self.doorObject9)

        self.doorObject10 = engine.GameObject()
        self.doorPhysics10 = engine.PhysicsComponent()
        self.doorTransform10 = engine.Transform()
        self.doorTransform10.xPos = 0
        self.doorTransform10.yPos = self.lvlHeight3 - (self.tileSize * 7)
        self.door_block_sprite10 = engine.Sprite(self.doorTransform10, True)
        self.door_block_sprite10.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite10.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite10.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject10.addTileMapComponent(self.tilemap3)
        self.doorObject10.addPhysicsComponent(self.doorPhysics10)
        self.doorObject10.addTransformComponent(self.doorTransform10)
        self.doorObject10.addSpriteComponent(self.door_block_sprite10)

        self.doorObject11 = engine.GameObject()
        self.doorPhysics11 = engine.PhysicsComponent()
        self.doorTransform11 = engine.Transform()
        self.doorTransform11.xPos = 0
        self.doorTransform11.yPos = self.lvlHeight3 - (self.tileSize * 8)
        self.door_block_sprite11 = engine.Sprite(self.doorTransform11, True)
        self.door_block_sprite11.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite11.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite11.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject11.addTileMapComponent(self.tilemap3)
        self.doorObject11.addPhysicsComponent(self.doorPhysics11)
        self.doorObject11.addTransformComponent(self.doorTransform11)
        self.doorObject11.addSpriteComponent(self.door_block_sprite11)

        self.doorObject12 = engine.GameObject()
        self.doorPhysics12 = engine.PhysicsComponent()
        self.doorTransform12 = engine.Transform()
        self.doorTransform12.xPos = 0
        self.doorTransform12.yPos = self.lvlHeight3 - (self.tileSize * 9)
        self.door_block_sprite12 = engine.Sprite(self.doorTransform12, True)
        self.door_block_sprite12.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite12.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite12.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject12.addTileMapComponent(self.tilemap3)
        self.doorObject12.addPhysicsComponent(self.doorPhysics12)
        self.doorObject12.addTransformComponent(self.doorTransform12)
        self.doorObject12.addSpriteComponent(self.door_block_sprite12)

        self.doorObject13 = engine.GameObject()
        self.doorPhysics13 = engine.PhysicsComponent()
        self.doorTransform13 = engine.Transform()
        self.doorTransform13.xPos = self.lvlWidth3 - self.tileSize + 1
        self.doorTransform13.yPos = self.tileSize * 7
        self.door_block_sprite13 = engine.Sprite(self.doorTransform13, True)
        self.door_block_sprite13.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite13.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite13.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject13.addTileMapComponent(self.tilemap3)
        self.doorObject13.addPhysicsComponent(self.doorPhysics13)
        self.doorObject13.addTransformComponent(self.doorTransform13)
        self.doorObject13.addSpriteComponent(self.door_block_sprite13)

        self.doorObject14 = engine.GameObject()
        self.doorPhysics14 = engine.PhysicsComponent()
        self.doorTransform14 = engine.Transform()
        self.doorTransform14.xPos = self.lvlWidth3 - self.tileSize + 1
        self.doorTransform14.yPos = self.tileSize * 8
        self.door_block_sprite14 = engine.Sprite(self.doorTransform14, True)
        self.door_block_sprite14.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite14.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite14.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject14.addTileMapComponent(self.tilemap3)
        self.doorObject14.addPhysicsComponent(self.doorPhysics14)
        self.doorObject14.addTransformComponent(self.doorTransform14)
        self.doorObject14.addSpriteComponent(self.door_block_sprite14)

        self.doorObject15 = engine.GameObject()
        self.doorPhysics15 = engine.PhysicsComponent()
        self.doorTransform15 = engine.Transform()
        self.doorTransform15.xPos = self.lvlWidth3 - self.tileSize + 1
        self.doorTransform15.yPos = self.tileSize * 9
        self.door_block_sprite15 = engine.Sprite(self.doorTransform15, True)
        self.door_block_sprite15.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite15.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite15.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject15.addTileMapComponent(self.tilemap3)
        self.doorObject15.addPhysicsComponent(self.doorPhysics15)
        self.doorObject15.addTransformComponent(self.doorTransform15)
        self.doorObject15.addSpriteComponent(self.door_block_sprite15)

        self.doorObjectsDict[str(self.tilemap3)] = [self.doorObject10, self.doorObject11, self.doorObject12, self.doorObject13, self.doorObject14, self.doorObject15]

        self.doorObject16 = engine.GameObject()
        self.doorPhysics16 = engine.PhysicsComponent()
        self.doorTransform16 = engine.Transform()
        self.doorTransform16.xPos = 0
        self.doorTransform16.yPos = self.tileSize * 7
        self.door_block_sprite16 = engine.Sprite(self.doorTransform16, True)
        self.door_block_sprite16.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite16.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite16.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject16.addTileMapComponent(self.tilemap4)
        self.doorObject16.addPhysicsComponent(self.doorPhysics16)
        self.doorObject16.addTransformComponent(self.doorTransform16)
        self.doorObject16.addSpriteComponent(self.door_block_sprite16)

        self.doorObject17 = engine.GameObject()
        self.doorPhysics17 = engine.PhysicsComponent()
        self.doorTransform17 = engine.Transform()
        self.doorTransform17.xPos = 0
        self.doorTransform17.yPos = self.tileSize * 8
        self.door_block_sprite17 = engine.Sprite(self.doorTransform17, True)
        self.door_block_sprite17.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite17.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite17.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject17.addTileMapComponent(self.tilemap4)
        self.doorObject17.addPhysicsComponent(self.doorPhysics17)
        self.doorObject17.addTransformComponent(self.doorTransform17)
        self.doorObject17.addSpriteComponent(self.door_block_sprite17)

        self.doorObject18 = engine.GameObject()
        self.doorPhysics18 = engine.PhysicsComponent()
        self.doorTransform18 = engine.Transform()
        self.doorTransform18.xPos = 0
        self.doorTransform18.yPos = self.tileSize * 9
        self.door_block_sprite18 = engine.Sprite(self.doorTransform18, True)
        self.door_block_sprite18.setRectangleDimensions(self.tileSize, self.tileSize)
        self.door_block_sprite18.setSpriteSheetDimensions(34, 32, 299, 303, 1, 1, 0)
        self.door_block_sprite18.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.doorObject18.addTileMapComponent(self.tilemap4)
        self.doorObject18.addPhysicsComponent(self.doorPhysics18)
        self.doorObject18.addTransformComponent(self.doorTransform18)
        self.doorObject18.addSpriteComponent(self.door_block_sprite18)

        self.doorObjectsDict[str(self.tilemap4)] = [self.doorObject16, self.doorObject17, self.doorObject18]

    def createBubbleDoorObjects(self):
        self.bubbleDoorDict = {}

        # xPos, yPos, width, height, facingLeft
        self.bubbleDoor1 = BubbleDoor(self.lvlWidth1 - self.tileSize - 24, self.lvlHeight1 - (self.tileSize * 9), 
                                      24, self.tileSize * 3, True)
        self.bubbleTransform1 = engine.Transform()
        self.bubbleTransform1.xPos = self.lvlWidth1 - self.tileSize - 24
        self.bubbleTransform1.yPos = self.lvlHeight1 - (self.tileSize * 9)
        self.bubble_sprite1_1 = engine.Sprite(self.bubbleTransform1, False)
        self.bubble_sprite1_1.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite1_1.setSpriteSheetDimensions(19, 97, 1136, 600, 1, 1, 0)
        self.bubble_sprite1_1.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor1.addSpriteComponent(self.bubble_sprite1_1, 0)
        self.bubble_sprite1_2 = engine.Sprite(self.bubbleTransform1, False)
        self.bubble_sprite1_2.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite1_2.setSpriteSheetDimensions(19, 97, 1099, 600, 1, 1, 0)
        self.bubble_sprite1_2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor1.addSpriteComponent(self.bubble_sprite1_2, 1)
        self.bubbleDoor1.setCurrentSpriteComponent(0)

        self.bubbleDoor2 = BubbleDoor(self.tileSize, self.lvlHeight2 - (self.tileSize * 9), 
                                      24, self.tileSize * 3, False)
        self.bubbleTransform2 = engine.Transform()
        self.bubbleTransform2.xPos = self.tileSize
        self.bubbleTransform2.yPos = self.lvlHeight2 - (self.tileSize * 9)
        self.bubble_sprite2_1 = engine.Sprite(self.bubbleTransform2, True)
        self.bubble_sprite2_1.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite2_1.setSpriteSheetDimensions(19, 97, 1140, 600, 1, 1, 0)
        self.bubble_sprite2_1.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor2.addSpriteComponent(self.bubble_sprite2_1, 0)
        self.bubble_sprite2_2 = engine.Sprite(self.bubbleTransform2, True)
        self.bubble_sprite2_2.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite2_2.setSpriteSheetDimensions(19, 97, 1177, 600, 1, 1, 0)
        self.bubble_sprite2_2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor2.addSpriteComponent(self.bubble_sprite2_2, 1)
        self.bubbleDoor2.setCurrentSpriteComponent(0)

        self.bubbleDoorDict[str(self.tilemap1)] = [self.bubbleDoor1]
        self.bubbleDoorDict[str(self.tilemap2)] = [self.bubbleDoor2]

        self.bubbleDoor3 = BubbleDoor(self.lvlWidth2 - self.tileSize - 24, self.lvlHeight2 - (self.tileSize * 9), 
                                      24, self.tileSize * 3, True)
        self.bubbleTransform3 = engine.Transform()
        self.bubbleTransform3.xPos = self.lvlWidth2 - self.tileSize - 24
        self.bubbleTransform3.yPos = self.lvlHeight2 - (self.tileSize * 9)
        self.bubble_sprite3_1 = engine.Sprite(self.bubbleTransform3, False)
        self.bubble_sprite3_1.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite3_1.setSpriteSheetDimensions(19, 97, 1136, 600, 1, 1, 0)
        self.bubble_sprite3_1.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor3.addSpriteComponent(self.bubble_sprite3_1, 0)
        self.bubble_sprite3_2 = engine.Sprite(self.bubbleTransform3, False)
        self.bubble_sprite3_2.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite3_2.setSpriteSheetDimensions(19, 97, 1099, 600, 1, 1, 0)
        self.bubble_sprite3_2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor3.addSpriteComponent(self.bubble_sprite3_2, 1)
        self.bubbleDoor3.setCurrentSpriteComponent(0)
        self.bubbleDoorDict[str(self.tilemap2)].append(self.bubbleDoor3)

        self.bubbleDoor4 = BubbleDoor(self.tileSize, self.lvlHeight3 - (self.tileSize * 9), 
                                      24, self.tileSize * 3, False)
        self.bubbleTransform4 = engine.Transform()
        self.bubbleTransform4.xPos = self.tileSize
        self.bubbleTransform4.yPos = self.lvlHeight3 - (self.tileSize * 9)
        self.bubble_sprite4_1 = engine.Sprite(self.bubbleTransform4, True)
        self.bubble_sprite4_1.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite4_1.setSpriteSheetDimensions(19, 97, 1140, 600, 1, 1, 0)
        self.bubble_sprite4_1.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor4.addSpriteComponent(self.bubble_sprite4_1, 0)
        self.bubble_sprite4_2 = engine.Sprite(self.bubbleTransform4, True)
        self.bubble_sprite4_2.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite4_2.setSpriteSheetDimensions(19, 97, 1177, 600, 1, 1, 0)
        self.bubble_sprite4_2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor4.addSpriteComponent(self.bubble_sprite4_2, 1)
        self.bubbleDoor4.setCurrentSpriteComponent(0)
        self.bubbleDoorDict[str(self.tilemap3)] = [self.bubbleDoor4]

        self.bubbleDoor5 = BubbleDoor(self.lvlWidth3 - self.tileSize - 24, self.tileSize * 7, 
                                      24, self.tileSize * 3, True)
        self.bubbleTransform5 = engine.Transform()
        self.bubbleTransform5.xPos = self.lvlWidth3 - self.tileSize - 24
        self.bubbleTransform5.yPos = self.tileSize * 7
        self.bubble_sprite5_1 = engine.Sprite(self.bubbleTransform5, False)
        self.bubble_sprite5_1.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite5_1.setSpriteSheetDimensions(19, 97, 1136, 600, 1, 1, 0)
        self.bubble_sprite5_1.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor5.addSpriteComponent(self.bubble_sprite5_1, 0)
        self.bubble_sprite5_2 = engine.Sprite(self.bubbleTransform5, False)
        self.bubble_sprite5_2.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite5_2.setSpriteSheetDimensions(19, 97, 1099, 600, 1, 1, 0)
        self.bubble_sprite5_2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor5.addSpriteComponent(self.bubble_sprite5_2, 1)
        self.bubbleDoor5.setCurrentSpriteComponent(0)
        self.bubbleDoorDict[str(self.tilemap3)].append(self.bubbleDoor5)

        self.bubbleDoor6 = BubbleDoor(self.tileSize, self.tileSize * 7, 
                                      24, self.tileSize * 3, False)
        self.bubbleTransform6 = engine.Transform()
        self.bubbleTransform6.xPos = self.tileSize
        self.bubbleTransform6.yPos = self.tileSize * 7
        self.bubble_sprite6_1 = engine.Sprite(self.bubbleTransform6, True)
        self.bubble_sprite6_1.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite6_1.setSpriteSheetDimensions(19, 97, 1140, 600, 1, 1, 0)
        self.bubble_sprite6_1.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor6.addSpriteComponent(self.bubble_sprite6_1, 0)
        self.bubble_sprite6_2 = engine.Sprite(self.bubbleTransform6, True)
        self.bubble_sprite6_2.setRectangleDimensions(24, self.tileSize * 3)
        self.bubble_sprite6_2.setSpriteSheetDimensions(19, 97, 1177, 600, 1, 1, 0)
        self.bubble_sprite6_2.loadImage('Assets/tilesets/Metroid_Tileset_2.bmp', self.sdl.getSDLRenderer())
        self.bubbleDoor6.addSpriteComponent(self.bubble_sprite6_2, 1)
        self.bubbleDoor6.setCurrentSpriteComponent(0)
        self.bubbleDoorDict[str(self.tilemap4)] = [self.bubbleDoor6]

        self.whichDoorToOpenDict = {}
        self.whichDoorToOpenDict[str(self.tilemap1) + str(self.tilemap2)] = self.bubbleDoor2
        self.whichDoorToOpenDict[str(self.tilemap2) + str(self.tilemap1)] = self.bubbleDoor1
        self.whichDoorToOpenDict[str(self.tilemap2) + str(self.tilemap3)] = self.bubbleDoor4
        self.whichDoorToOpenDict[str(self.tilemap3) + str(self.tilemap2)] = self.bubbleDoor3
        self.whichDoorToOpenDict[str(self.tilemap3) + str(self.tilemap4)] = self.bubbleDoor6
        self.whichDoorToOpenDict[str(self.tilemap4) + str(self.tilemap3)] = self.bubbleDoor5

        self.whichDoorToCloseDict = {}
        self.whichDoorToCloseDict[str(self.tilemap1) + str(self.tilemap2)] = self.bubbleDoor1
        self.whichDoorToCloseDict[str(self.tilemap2) + str(self.tilemap1)] = self.bubbleDoor2
        self.whichDoorToCloseDict[str(self.tilemap2) + str(self.tilemap3)] = self.bubbleDoor3
        self.whichDoorToCloseDict[str(self.tilemap3) + str(self.tilemap2)] = self.bubbleDoor4
        self.whichDoorToCloseDict[str(self.tilemap3) + str(self.tilemap4)] = self.bubbleDoor5
        self.whichDoorToCloseDict[str(self.tilemap4) + str(self.tilemap3)] = self.bubbleDoor6

    def createBugs(self):
        self.bugObject1 = engine.GameObject()
        self.bugPhysics1 = engine.PhysicsComponent()
        self.bugTransform1 = engine.Transform()
        #int _height, int _total_distance, float _xVelocity, int _gravity_factor
        self.bugJump1 = engine.JumpComponent(420, 300, 4, -2)
        self.bugTransform1.xPos = 600
        self.bugTransform1.yPos = self.tileSize * 3
        self.bug_sprite_1_1 = engine.Sprite(self.bugTransform1, True)
        self.bug_sprite_1_1.setRectangleDimensions(80, 60)
        self.bug_sprite_1_1.setSpriteSheetDimensions(36, 21, 272, 12, 3, 3, 4)
        self.bug_sprite_1_1.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_1_2 = engine.Sprite(self.bugTransform1, True)
        self.bug_sprite_1_2.setRectangleDimensions(80, 60)
        self.bug_sprite_1_2.setSpriteSheetDimensions(36, 23, 272, 36, 3, 3, 4)
        self.bug_sprite_1_2.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_1_3 = engine.Sprite(self.bugTransform1, True)
        self.bug_sprite_1_3.setRectangleDimensions(80, 60)
        self.bug_sprite_1_3.setSpriteSheetDimensions(36, 24, 272, 62, 3, 3, 4)
        self.bug_sprite_1_3.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bugObject1.addTileMapComponent(self.tilemap2)
        self.bugObject1.addPhysicsComponent(self.bugPhysics1)
        self.bugObject1.addTransformComponent(self.bugTransform1)
        self.bugObject1.addSpriteComponent(self.bug_sprite_1_3)
        self.bugObject1.addJumpComponent(self.bugJump1)
        self.bugObject1.xVel = int(self.bugObject1.mJumpComponent.xVelocity)
        self.bugObject1.yVel = -4
        self.bug1 = Bug(self.bugObject1, 300, 420)
        self.bug1.addSpriteToList(self.bug_sprite_1_1, 2)
        self.bug1.addSpriteToList(self.bug_sprite_1_2, 2)
        self.bug1.addSpriteToList(self.bug_sprite_1_3, 2)
        self.bug1.setActiveStatus(True)


        self.bugObject2 = engine.GameObject()
        self.bugPhysics2 = engine.PhysicsComponent()
        self.bugTransform2 = engine.Transform()
        self.bugJump2 = engine.JumpComponent(420, 300, 4, -2)
        self.bugTransform2.xPos = 1200
        self.bugTransform2.yPos = self.tileSize * 3
        self.bug_sprite_2_1 = engine.Sprite(self.bugTransform2, True)
        self.bug_sprite_2_1.setRectangleDimensions(80, 60)
        self.bug_sprite_2_1.setSpriteSheetDimensions(36, 21, 272, 12, 3, 3, 4)
        self.bug_sprite_2_1.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_2_2 = engine.Sprite(self.bugTransform2, True)
        self.bug_sprite_2_2.setRectangleDimensions(80, 60)
        self.bug_sprite_2_2.setSpriteSheetDimensions(36, 23, 272, 36, 3, 3, 4)
        self.bug_sprite_2_2.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_2_3 = engine.Sprite(self.bugTransform2, True)
        self.bug_sprite_2_3.setRectangleDimensions(80, 60)
        self.bug_sprite_2_3.setSpriteSheetDimensions(36, 24, 272, 62, 3, 3, 4)
        self.bug_sprite_2_3.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bugObject2.addTileMapComponent(self.tilemap2)
        self.bugObject2.addPhysicsComponent(self.bugPhysics2)
        self.bugObject2.addTransformComponent(self.bugTransform2)
        self.bugObject2.addSpriteComponent(self.bug_sprite_2_1)
        self.bugObject2.addJumpComponent(self.bugJump2)
        self.bugObject2.xVel = int(self.bugObject2.mJumpComponent.xVelocity)
        self.bugObject2.yVel = -4
        self.bug2 = Bug(self.bugObject2, 300, 420)
        self.bug2.addSpriteToList(self.bug_sprite_2_1, 2)
        self.bug2.addSpriteToList(self.bug_sprite_2_2, 2)
        self.bug2.addSpriteToList(self.bug_sprite_2_3, 2)
        self.bug2.setActiveStatus(True)

        self.bugObject3 = engine.GameObject()
        self.bugPhysics3 = engine.PhysicsComponent()
        self.bugTransform3 = engine.Transform()
        self.bugJump3 = engine.JumpComponent(420, 300, 4, -2)
        self.bugTransform3.xPos = 1800
        self.bugTransform3.yPos = self.tileSize * 3
        self.bug_sprite_3_1 = engine.Sprite(self.bugTransform3, True)
        self.bug_sprite_3_1.setRectangleDimensions(80, 60)
        self.bug_sprite_3_1.setSpriteSheetDimensions(36, 21, 272, 12, 3, 3, 4)
        self.bug_sprite_3_1.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_3_2 = engine.Sprite(self.bugTransform3, True)
        self.bug_sprite_3_2.setRectangleDimensions(80, 60)
        self.bug_sprite_3_2.setSpriteSheetDimensions(36, 23, 272, 36, 3, 3, 4)
        self.bug_sprite_3_2.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_3_3 = engine.Sprite(self.bugTransform3, True)
        self.bug_sprite_3_3.setRectangleDimensions(80, 60)
        self.bug_sprite_3_3.setSpriteSheetDimensions(36, 24, 272, 62, 3, 3, 4)
        self.bug_sprite_3_3.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bugObject3.addTileMapComponent(self.tilemap2)
        self.bugObject3.addPhysicsComponent(self.bugPhysics3)
        self.bugObject3.addTransformComponent(self.bugTransform3)
        self.bugObject3.addSpriteComponent(self.bug_sprite_3_1)
        self.bugObject3.addJumpComponent(self.bugJump3)
        self.bugObject3.xVel = int(self.bugObject3.mJumpComponent.xVelocity)
        self.bugObject3.yVel = -4
        self.bug3 = Bug(self.bugObject3, 300, 420)
        self.bug3.addSpriteToList(self.bug_sprite_3_1, 2)
        self.bug3.addSpriteToList(self.bug_sprite_3_2, 2)
        self.bug3.addSpriteToList(self.bug_sprite_3_3, 2)
        self.bug3.setActiveStatus(True)

        self.bugObject4 = engine.GameObject()
        self.bugPhysics4 = engine.PhysicsComponent()
        self.bugTransform4 = engine.Transform()
        self.bugJump4 = engine.JumpComponent(420, 300, 4, -2)
        self.bugTransform4.xPos = 2400
        self.bugTransform4.yPos = self.tileSize * 3
        self.bug_sprite_4_1 = engine.Sprite(self.bugTransform4, True)
        self.bug_sprite_4_1.setRectangleDimensions(80, 60)
        self.bug_sprite_4_1.setSpriteSheetDimensions(36, 21, 272, 12, 3, 3, 4)
        self.bug_sprite_4_1.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_4_2 = engine.Sprite(self.bugTransform4, True)
        self.bug_sprite_4_2.setRectangleDimensions(80, 60)
        self.bug_sprite_4_2.setSpriteSheetDimensions(36, 23, 272, 36, 3, 3, 4)
        self.bug_sprite_4_2.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bug_sprite_4_3 = engine.Sprite(self.bugTransform4, True)
        self.bug_sprite_4_3.setRectangleDimensions(80, 60)
        self.bug_sprite_4_3.setSpriteSheetDimensions(36, 24, 272, 62, 3, 3, 4)
        self.bug_sprite_4_3.loadImage('Assets/spritesheets/MetroidEnemiesSpriteSheet.png', self.sdl.getSDLRenderer())
        self.bugObject4.addTileMapComponent(self.tilemap2)
        self.bugObject4.addPhysicsComponent(self.bugPhysics4)
        self.bugObject4.addTransformComponent(self.bugTransform4)
        self.bugObject4.addSpriteComponent(self.bug_sprite_4_1)
        self.bugObject4.addJumpComponent(self.bugJump4)
        self.bugObject4.xVel = int(self.bugObject4.mJumpComponent.xVelocity)
        self.bugObject4.yVel = -4
        self.bug4 = Bug(self.bugObject4, 300, 420)
        self.bug4.addSpriteToList(self.bug_sprite_4_1, 2)
        self.bug4.addSpriteToList(self.bug_sprite_4_2, 2)
        self.bug4.addSpriteToList(self.bug_sprite_4_3, 2)
        self.bug4.setActiveStatus(True)

        self.bugArray = []
        self.bugArray.append(self.bug1)
        self.bugArray.append(self.bug2)
        self.bugArray.append(self.bug3)
        self.bugArray.append(self.bug4)

        self.enemiesDict[str(self.tilemap2)] = {"bugArray" : self.bugArray}

    def createZoomers(self):
        '''
        "setSpriteSheetDimensions" is for correctly iterating through the spritesheet.
        (width of sprite, height of sprite, start x, start y, max num sprites in a row, total num sprites, numPixelsToTrimFromWidth)
        numPixelsToTrimFromWidth : this parameter tells how many pixels are to be taken off each sprite image, in case
        there is extra space between images.
        '''
        self.zoomerSize = 34

        self.zoomerObject1 = engine.GameObject()
        self.zoomerPhysics1 = engine.PhysicsComponent()
        self.zoomerTransform1 = engine.Transform()
        self.zoomerTransform1.xPos = 350
        self.zoomerTransform1.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 9) - self.zoomerSize
        self.zoomer_sprite_1_1 = engine.Sprite(self.zoomerTransform1, True)
        self.zoomer_sprite_1_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_1_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_1_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_1_2 = engine.Sprite(self.zoomerTransform1, True)
        self.zoomer_sprite_1_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_1_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_1_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_1_3 = engine.Sprite(self.zoomerTransform1, True)
        self.zoomer_sprite_1_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_1_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_1_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_1_4 = engine.Sprite(self.zoomerTransform1, True)
        self.zoomer_sprite_1_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_1_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_1_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject1.addTileMapComponent(self.tilemap3)
        self.zoomerObject1.addPhysicsComponent(self.zoomerPhysics1)
        self.zoomerObject1.addTransformComponent(self.zoomerTransform1)
        self.zoomerObject1.addSpriteComponent(self.zoomer_sprite_1_1)
        self.zoomer1 = Zoomer(self.zoomerObject1, 0, True)
        self.zoomer1.addSpriteToList(self.zoomer_sprite_1_1, 1)
        self.zoomer1.addSpriteToList(self.zoomer_sprite_1_2, 1)
        self.zoomer1.addSpriteToList(self.zoomer_sprite_1_3, 1)
        self.zoomer1.addSpriteToList(self.zoomer_sprite_1_4, 1)
        self.zoomer1.setActiveStatus(True)
        self.zoomerObject1.xVel = self.zoomer1.getCurrentXVelocity()
        self.zoomerObject1.yVel = self.zoomer1.getCurrentYVelocity()

        self.zoomerObject2 = engine.GameObject()
        self.zoomerPhysics2 = engine.PhysicsComponent()
        self.zoomerTransform2 = engine.Transform()
        self.zoomerTransform2.xPos = 400
        self.zoomerTransform2.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 3) - self.zoomerSize
        self.zoomer_sprite_2_1 = engine.Sprite(self.zoomerTransform2, True)
        self.zoomer_sprite_2_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_2_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_2_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_2_2 = engine.Sprite(self.zoomerTransform2, True)
        self.zoomer_sprite_2_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_2_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_2_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_2_3 = engine.Sprite(self.zoomerTransform2, True)
        self.zoomer_sprite_2_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_2_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_2_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_2_4 = engine.Sprite(self.zoomerTransform2, True)
        self.zoomer_sprite_2_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_2_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_2_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject2.addTileMapComponent(self.tilemap3)
        self.zoomerObject2.addPhysicsComponent(self.zoomerPhysics2)
        self.zoomerObject2.addTransformComponent(self.zoomerTransform2)
        self.zoomerObject2.addSpriteComponent(self.zoomer_sprite_2_1)
        self.zoomer2 = Zoomer(self.zoomerObject2, 0, False)
        self.zoomer2.addSpriteToList(self.zoomer_sprite_2_1, 1)
        self.zoomer2.addSpriteToList(self.zoomer_sprite_2_2, 1)
        self.zoomer2.addSpriteToList(self.zoomer_sprite_2_3, 1)
        self.zoomer2.addSpriteToList(self.zoomer_sprite_2_4, 1)
        self.zoomer2.setActiveStatus(True)
        self.zoomerObject2.xVel = self.zoomer2.getCurrentXVelocity()
        self.zoomerObject2.yVel = self.zoomer2.getCurrentYVelocity()

        self.zoomerObject3 = engine.GameObject()
        self.zoomerPhysics3 = engine.PhysicsComponent()
        self.zoomerTransform3 = engine.Transform()
        self.zoomerTransform3.xPos = 450
        self.zoomerTransform3.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 16) - self.zoomerSize
        self.zoomer_sprite_3_1 = engine.Sprite(self.zoomerTransform3, True)
        self.zoomer_sprite_3_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_3_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_3_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_3_2 = engine.Sprite(self.zoomerTransform3, True)
        self.zoomer_sprite_3_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_3_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_3_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_3_3 = engine.Sprite(self.zoomerTransform3, True)
        self.zoomer_sprite_3_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_3_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_3_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_3_4 = engine.Sprite(self.zoomerTransform3, True)
        self.zoomer_sprite_3_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_3_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_3_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject3.addTileMapComponent(self.tilemap3)
        self.zoomerObject3.addPhysicsComponent(self.zoomerPhysics3)
        self.zoomerObject3.addTransformComponent(self.zoomerTransform3)
        self.zoomerObject3.addSpriteComponent(self.zoomer_sprite_3_1)
        self.zoomer3 = Zoomer(self.zoomerObject3, 0, True)
        self.zoomer3.addSpriteToList(self.zoomer_sprite_3_1, 1)
        self.zoomer3.addSpriteToList(self.zoomer_sprite_3_2, 1)
        self.zoomer3.addSpriteToList(self.zoomer_sprite_3_3, 1)
        self.zoomer3.addSpriteToList(self.zoomer_sprite_3_4, 1)
        self.zoomer3.setActiveStatus(True)
        self.zoomerObject3.xVel = self.zoomer3.getCurrentXVelocity()
        self.zoomerObject3.yVel = self.zoomer3.getCurrentYVelocity()

        self.zoomerObject4 = engine.GameObject()
        self.zoomerPhysics4 = engine.PhysicsComponent()
        self.zoomerTransform4 = engine.Transform()
        self.zoomerTransform4.xPos = 550
        self.zoomerTransform4.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 23) - self.zoomerSize
        self.zoomer_sprite_4_1 = engine.Sprite(self.zoomerTransform4, True)
        self.zoomer_sprite_4_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_4_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_4_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_4_2 = engine.Sprite(self.zoomerTransform4, True)
        self.zoomer_sprite_4_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_4_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_4_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_4_3 = engine.Sprite(self.zoomerTransform4, True)
        self.zoomer_sprite_4_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_4_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_4_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_4_4 = engine.Sprite(self.zoomerTransform4, True)
        self.zoomer_sprite_4_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_4_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_4_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject4.addTileMapComponent(self.tilemap3)
        self.zoomerObject4.addPhysicsComponent(self.zoomerPhysics4)
        self.zoomerObject4.addTransformComponent(self.zoomerTransform4)
        self.zoomerObject4.addSpriteComponent(self.zoomer_sprite_4_1)
        self.zoomer4 = Zoomer(self.zoomerObject4, 0, True)
        self.zoomer4.addSpriteToList(self.zoomer_sprite_4_1, 1)
        self.zoomer4.addSpriteToList(self.zoomer_sprite_4_2, 1)
        self.zoomer4.addSpriteToList(self.zoomer_sprite_4_3, 1)
        self.zoomer4.addSpriteToList(self.zoomer_sprite_4_4, 1)
        self.zoomer4.setActiveStatus(True)
        self.zoomerObject4.xVel = self.zoomer4.getCurrentXVelocity()
        self.zoomerObject4.yVel = self.zoomer4.getCurrentYVelocity()

        self.zoomerObject5 = engine.GameObject()
        self.zoomerPhysics5 = engine.PhysicsComponent()
        self.zoomerTransform5 = engine.Transform()
        self.zoomerTransform5.xPos = 350
        self.zoomerTransform5.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 30) - self.zoomerSize
        self.zoomer_sprite_5_1 = engine.Sprite(self.zoomerTransform5, True)
        self.zoomer_sprite_5_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_5_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_5_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_5_2 = engine.Sprite(self.zoomerTransform5, True)
        self.zoomer_sprite_5_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_5_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_5_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_5_3 = engine.Sprite(self.zoomerTransform5, True)
        self.zoomer_sprite_5_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_5_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_5_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_5_4 = engine.Sprite(self.zoomerTransform5, True)
        self.zoomer_sprite_5_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_5_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_5_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject5.addTileMapComponent(self.tilemap3)
        self.zoomerObject5.addPhysicsComponent(self.zoomerPhysics5)
        self.zoomerObject5.addTransformComponent(self.zoomerTransform5)
        self.zoomerObject5.addSpriteComponent(self.zoomer_sprite_5_1)
        self.zoomer5 = Zoomer(self.zoomerObject5, 0, True)
        self.zoomer5.addSpriteToList(self.zoomer_sprite_5_1, 1)
        self.zoomer5.addSpriteToList(self.zoomer_sprite_5_2, 1)
        self.zoomer5.addSpriteToList(self.zoomer_sprite_5_3, 1)
        self.zoomer5.addSpriteToList(self.zoomer_sprite_5_4, 1)
        self.zoomer5.setActiveStatus(True)
        self.zoomerObject5.xVel = self.zoomer5.getCurrentXVelocity()
        self.zoomerObject5.yVel = self.zoomer5.getCurrentYVelocity()

        self.zoomerObject6 = engine.GameObject()
        self.zoomerPhysics6 = engine.PhysicsComponent()
        self.zoomerTransform6 = engine.Transform()
        self.zoomerTransform6.xPos = 450
        self.zoomerTransform6.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 37) - self.zoomerSize
        self.zoomer_sprite_6_1 = engine.Sprite(self.zoomerTransform6, True)
        self.zoomer_sprite_6_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_6_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_6_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_6_2 = engine.Sprite(self.zoomerTransform6, True)
        self.zoomer_sprite_6_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_6_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_6_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_6_3 = engine.Sprite(self.zoomerTransform6, True)
        self.zoomer_sprite_6_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_6_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_6_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_6_4 = engine.Sprite(self.zoomerTransform6, True)
        self.zoomer_sprite_6_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_6_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_6_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject6.addTileMapComponent(self.tilemap3)
        self.zoomerObject6.addPhysicsComponent(self.zoomerPhysics6)
        self.zoomerObject6.addTransformComponent(self.zoomerTransform6)
        self.zoomerObject6.addSpriteComponent(self.zoomer_sprite_6_1)
        self.zoomer6 = Zoomer(self.zoomerObject6, 0, True)
        self.zoomer6.addSpriteToList(self.zoomer_sprite_6_1, 1)
        self.zoomer6.addSpriteToList(self.zoomer_sprite_6_2, 1)
        self.zoomer6.addSpriteToList(self.zoomer_sprite_6_3, 1)
        self.zoomer6.addSpriteToList(self.zoomer_sprite_6_4, 1)
        self.zoomer6.setActiveStatus(True)
        self.zoomerObject6.xVel = self.zoomer6.getCurrentXVelocity()
        self.zoomerObject6.yVel = self.zoomer6.getCurrentYVelocity()

        self.zoomerObject7 = engine.GameObject()
        self.zoomerPhysics7 = engine.PhysicsComponent()
        self.zoomerTransform7 = engine.Transform()
        self.zoomerTransform7.xPos = 550
        self.zoomerTransform7.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 44) - self.zoomerSize
        self.zoomer_sprite_7_1 = engine.Sprite(self.zoomerTransform7, True)
        self.zoomer_sprite_7_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_7_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_7_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_7_2 = engine.Sprite(self.zoomerTransform7, True)
        self.zoomer_sprite_7_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_7_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_7_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_7_3 = engine.Sprite(self.zoomerTransform7, True)
        self.zoomer_sprite_7_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_7_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_7_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_7_4 = engine.Sprite(self.zoomerTransform7, True)
        self.zoomer_sprite_7_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_7_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_7_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject7.addTileMapComponent(self.tilemap3)
        self.zoomerObject7.addPhysicsComponent(self.zoomerPhysics7)
        self.zoomerObject7.addTransformComponent(self.zoomerTransform7)
        self.zoomerObject7.addSpriteComponent(self.zoomer_sprite_7_1)
        self.zoomer7 = Zoomer(self.zoomerObject7, 0, True)
        self.zoomer7.addSpriteToList(self.zoomer_sprite_7_1, 1)
        self.zoomer7.addSpriteToList(self.zoomer_sprite_7_2, 1)
        self.zoomer7.addSpriteToList(self.zoomer_sprite_7_3, 1)
        self.zoomer7.addSpriteToList(self.zoomer_sprite_7_4, 1)
        self.zoomer7.setActiveStatus(True)
        self.zoomerObject7.xVel = self.zoomer7.getCurrentXVelocity()
        self.zoomerObject7.yVel = self.zoomer7.getCurrentYVelocity()

        self.zoomerObject8 = engine.GameObject()
        self.zoomerPhysics8 = engine.PhysicsComponent()
        self.zoomerTransform8 = engine.Transform()
        self.zoomerTransform8.xPos = 350
        self.zoomerTransform8.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 51) - self.zoomerSize
        self.zoomer_sprite_8_1 = engine.Sprite(self.zoomerTransform8, True)
        self.zoomer_sprite_8_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_8_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_8_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_8_2 = engine.Sprite(self.zoomerTransform8, True)
        self.zoomer_sprite_8_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_8_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_8_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_8_3 = engine.Sprite(self.zoomerTransform8, True)
        self.zoomer_sprite_8_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_8_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_8_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_8_4 = engine.Sprite(self.zoomerTransform8, True)
        self.zoomer_sprite_8_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_8_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_8_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject8.addTileMapComponent(self.tilemap3)
        self.zoomerObject8.addPhysicsComponent(self.zoomerPhysics8)
        self.zoomerObject8.addTransformComponent(self.zoomerTransform8)
        self.zoomerObject8.addSpriteComponent(self.zoomer_sprite_8_1)
        self.zoomer8 = Zoomer(self.zoomerObject8, 0, True)
        self.zoomer8.addSpriteToList(self.zoomer_sprite_8_1, 1)
        self.zoomer8.addSpriteToList(self.zoomer_sprite_8_2, 1)
        self.zoomer8.addSpriteToList(self.zoomer_sprite_8_3, 1)
        self.zoomer8.addSpriteToList(self.zoomer_sprite_8_4, 1)
        self.zoomer8.setActiveStatus(True)
        self.zoomerObject8.xVel = self.zoomer8.getCurrentXVelocity()
        self.zoomerObject8.yVel = self.zoomer8.getCurrentYVelocity()

        self.zoomerObject9 = engine.GameObject()
        self.zoomerPhysics9 = engine.PhysicsComponent()
        self.zoomerTransform9 = engine.Transform()
        self.zoomerTransform9.xPos = 450
        self.zoomerTransform9.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 58) - self.zoomerSize
        self.zoomer_sprite_9_1 = engine.Sprite(self.zoomerTransform9, True)
        self.zoomer_sprite_9_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_9_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_9_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_9_2 = engine.Sprite(self.zoomerTransform9, True)
        self.zoomer_sprite_9_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_9_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_9_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_9_3 = engine.Sprite(self.zoomerTransform9, True)
        self.zoomer_sprite_9_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_9_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_9_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_9_4 = engine.Sprite(self.zoomerTransform9, True)
        self.zoomer_sprite_9_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_9_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_9_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject9.addTileMapComponent(self.tilemap3)
        self.zoomerObject9.addPhysicsComponent(self.zoomerPhysics9)
        self.zoomerObject9.addTransformComponent(self.zoomerTransform9)
        self.zoomerObject9.addSpriteComponent(self.zoomer_sprite_9_1)
        self.zoomer9 = Zoomer(self.zoomerObject9, 0, True)
        self.zoomer9.addSpriteToList(self.zoomer_sprite_9_1, 1)
        self.zoomer9.addSpriteToList(self.zoomer_sprite_9_2, 1)
        self.zoomer9.addSpriteToList(self.zoomer_sprite_9_3, 1)
        self.zoomer9.addSpriteToList(self.zoomer_sprite_9_4, 1)
        self.zoomer9.setActiveStatus(True)
        self.zoomerObject9.xVel = self.zoomer9.getCurrentXVelocity()
        self.zoomerObject9.yVel = self.zoomer9.getCurrentYVelocity()

        self.zoomerObject10 = engine.GameObject()
        self.zoomerPhysics10 = engine.PhysicsComponent()
        self.zoomerTransform10 = engine.Transform()
        self.zoomerTransform10.xPos = 550
        self.zoomerTransform10.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 65) - self.zoomerSize
        self.zoomer_sprite_10_1 = engine.Sprite(self.zoomerTransform10, True)
        self.zoomer_sprite_10_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_10_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_10_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_10_2 = engine.Sprite(self.zoomerTransform10, True)
        self.zoomer_sprite_10_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_10_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_10_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_10_3 = engine.Sprite(self.zoomerTransform10, True)
        self.zoomer_sprite_10_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_10_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_10_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_10_4 = engine.Sprite(self.zoomerTransform10, True)
        self.zoomer_sprite_10_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_10_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_10_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject10.addTileMapComponent(self.tilemap3)
        self.zoomerObject10.addPhysicsComponent(self.zoomerPhysics10)
        self.zoomerObject10.addTransformComponent(self.zoomerTransform10)
        self.zoomerObject10.addSpriteComponent(self.zoomer_sprite_10_1)
        self.zoomer10 = Zoomer(self.zoomerObject10, 0, True)
        self.zoomer10.addSpriteToList(self.zoomer_sprite_10_1, 1)
        self.zoomer10.addSpriteToList(self.zoomer_sprite_10_2, 1)
        self.zoomer10.addSpriteToList(self.zoomer_sprite_10_3, 1)
        self.zoomer10.addSpriteToList(self.zoomer_sprite_10_4, 1)
        self.zoomer10.setActiveStatus(True)
        self.zoomerObject10.xVel = self.zoomer10.getCurrentXVelocity()
        self.zoomerObject10.yVel = self.zoomer10.getCurrentYVelocity()

        self.zoomerObject11 = engine.GameObject()
        self.zoomerPhysics11 = engine.PhysicsComponent()
        self.zoomerTransform11 = engine.Transform()
        self.zoomerTransform11.xPos = 350
        self.zoomerTransform11.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 72) - self.zoomerSize
        self.zoomer_sprite_11_1 = engine.Sprite(self.zoomerTransform11, True)
        self.zoomer_sprite_11_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_11_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_11_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_11_2 = engine.Sprite(self.zoomerTransform11, True)
        self.zoomer_sprite_11_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_11_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_11_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_11_3 = engine.Sprite(self.zoomerTransform11, True)
        self.zoomer_sprite_11_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_11_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_11_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_11_4 = engine.Sprite(self.zoomerTransform11, True)
        self.zoomer_sprite_11_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_11_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_11_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject11.addTileMapComponent(self.tilemap3)
        self.zoomerObject11.addPhysicsComponent(self.zoomerPhysics11)
        self.zoomerObject11.addTransformComponent(self.zoomerTransform11)
        self.zoomerObject11.addSpriteComponent(self.zoomer_sprite_11_1)
        self.zoomer11 = Zoomer(self.zoomerObject11, 0, True)
        self.zoomer11.addSpriteToList(self.zoomer_sprite_11_1, 1)
        self.zoomer11.addSpriteToList(self.zoomer_sprite_11_2, 1)
        self.zoomer11.addSpriteToList(self.zoomer_sprite_11_3, 1)
        self.zoomer11.addSpriteToList(self.zoomer_sprite_11_4, 1)
        self.zoomer11.setActiveStatus(True)
        self.zoomerObject11.xVel = self.zoomer11.getCurrentXVelocity()
        self.zoomerObject11.yVel = self.zoomer11.getCurrentYVelocity()

        self.zoomerObject12 = engine.GameObject()
        self.zoomerPhysics12 = engine.PhysicsComponent()
        self.zoomerTransform12 = engine.Transform()
        self.zoomerTransform12.xPos = 450
        self.zoomerTransform12.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 79) - self.zoomerSize
        self.zoomer_sprite_12_1 = engine.Sprite(self.zoomerTransform12, True)
        self.zoomer_sprite_12_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_12_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_12_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_12_2 = engine.Sprite(self.zoomerTransform12, True)
        self.zoomer_sprite_12_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_12_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_12_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_12_3 = engine.Sprite(self.zoomerTransform12, True)
        self.zoomer_sprite_12_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_12_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_12_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_12_4 = engine.Sprite(self.zoomerTransform12, True)
        self.zoomer_sprite_12_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_12_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_12_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject12.addTileMapComponent(self.tilemap3)
        self.zoomerObject12.addPhysicsComponent(self.zoomerPhysics12)
        self.zoomerObject12.addTransformComponent(self.zoomerTransform12)
        self.zoomerObject12.addSpriteComponent(self.zoomer_sprite_12_1)
        self.zoomer12 = Zoomer(self.zoomerObject12, 0, True)
        self.zoomer12.addSpriteToList(self.zoomer_sprite_12_1, 1)
        self.zoomer12.addSpriteToList(self.zoomer_sprite_12_2, 1)
        self.zoomer12.addSpriteToList(self.zoomer_sprite_12_3, 1)
        self.zoomer12.addSpriteToList(self.zoomer_sprite_12_4, 1)
        self.zoomer12.setActiveStatus(True)
        self.zoomerObject12.xVel = self.zoomer12.getCurrentXVelocity()
        self.zoomerObject12.yVel = self.zoomer12.getCurrentYVelocity()

        # zoomers on left platforms
        self.zoomerObject13 = engine.GameObject()
        self.zoomerPhysics13 = engine.PhysicsComponent()
        self.zoomerTransform13 = engine.Transform()
        self.zoomerTransform13.xPos = 100
        self.zoomerTransform13.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 20) - self.zoomerSize
        self.zoomer_sprite_13_1 = engine.Sprite(self.zoomerTransform13, True)
        self.zoomer_sprite_13_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_13_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_13_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_13_2 = engine.Sprite(self.zoomerTransform13, True)
        self.zoomer_sprite_13_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_13_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_13_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_13_3 = engine.Sprite(self.zoomerTransform13, True)
        self.zoomer_sprite_13_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_13_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_13_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_13_4 = engine.Sprite(self.zoomerTransform13, True)
        self.zoomer_sprite_13_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_13_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_13_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject13.addTileMapComponent(self.tilemap3)
        self.zoomerObject13.addPhysicsComponent(self.zoomerPhysics13)
        self.zoomerObject13.addTransformComponent(self.zoomerTransform13)
        self.zoomerObject13.addSpriteComponent(self.zoomer_sprite_13_1)
        self.zoomer13 = Zoomer(self.zoomerObject13, 0, True)
        self.zoomer13.addSpriteToList(self.zoomer_sprite_13_1, 1)
        self.zoomer13.addSpriteToList(self.zoomer_sprite_13_2, 1)
        self.zoomer13.addSpriteToList(self.zoomer_sprite_13_3, 1)
        self.zoomer13.addSpriteToList(self.zoomer_sprite_13_4, 1)
        self.zoomer13.setActiveStatus(True)
        self.zoomerObject13.xVel = self.zoomer13.getCurrentXVelocity()
        self.zoomerObject13.yVel = self.zoomer13.getCurrentYVelocity()

        self.zoomerObject14 = engine.GameObject()
        self.zoomerPhysics14 = engine.PhysicsComponent()
        self.zoomerTransform14 = engine.Transform()
        self.zoomerTransform14.xPos = 200
        self.zoomerTransform14.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 27) - self.zoomerSize
        self.zoomer_sprite_14_1 = engine.Sprite(self.zoomerTransform14, True)
        self.zoomer_sprite_14_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_14_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_14_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_14_2 = engine.Sprite(self.zoomerTransform14, True)
        self.zoomer_sprite_14_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_14_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_14_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_14_3 = engine.Sprite(self.zoomerTransform14, True)
        self.zoomer_sprite_14_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_14_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_14_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_14_4 = engine.Sprite(self.zoomerTransform14, True)
        self.zoomer_sprite_14_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_14_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_14_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject14.addTileMapComponent(self.tilemap3)
        self.zoomerObject14.addPhysicsComponent(self.zoomerPhysics14)
        self.zoomerObject14.addTransformComponent(self.zoomerTransform14)
        self.zoomerObject14.addSpriteComponent(self.zoomer_sprite_14_1)
        self.zoomer14 = Zoomer(self.zoomerObject14, 0, True)
        self.zoomer14.addSpriteToList(self.zoomer_sprite_14_1, 1)
        self.zoomer14.addSpriteToList(self.zoomer_sprite_14_2, 1)
        self.zoomer14.addSpriteToList(self.zoomer_sprite_14_3, 1)
        self.zoomer14.addSpriteToList(self.zoomer_sprite_14_4, 1)
        self.zoomer14.setActiveStatus(True)
        self.zoomerObject14.xVel = self.zoomer14.getCurrentXVelocity()
        self.zoomerObject14.yVel = self.zoomer14.getCurrentYVelocity()

        self.zoomerObject15 = engine.GameObject()
        self.zoomerPhysics15 = engine.PhysicsComponent()
        self.zoomerTransform15 = engine.Transform()
        self.zoomerTransform15.xPos = 300
        self.zoomerTransform15.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 34) - self.zoomerSize
        self.zoomer_sprite_15_1 = engine.Sprite(self.zoomerTransform15, True)
        self.zoomer_sprite_15_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_15_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_15_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_15_2 = engine.Sprite(self.zoomerTransform15, True)
        self.zoomer_sprite_15_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_15_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_15_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_15_3 = engine.Sprite(self.zoomerTransform15, True)
        self.zoomer_sprite_15_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_15_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_15_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_15_4 = engine.Sprite(self.zoomerTransform15, True)
        self.zoomer_sprite_15_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_15_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_15_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject15.addTileMapComponent(self.tilemap3)
        self.zoomerObject15.addPhysicsComponent(self.zoomerPhysics15)
        self.zoomerObject15.addTransformComponent(self.zoomerTransform15)
        self.zoomerObject15.addSpriteComponent(self.zoomer_sprite_15_1)
        self.zoomer15 = Zoomer(self.zoomerObject15, 0, True)
        self.zoomer15.addSpriteToList(self.zoomer_sprite_15_1, 1)
        self.zoomer15.addSpriteToList(self.zoomer_sprite_15_2, 1)
        self.zoomer15.addSpriteToList(self.zoomer_sprite_15_3, 1)
        self.zoomer15.addSpriteToList(self.zoomer_sprite_15_4, 1)
        self.zoomer15.setActiveStatus(True)
        self.zoomerObject15.xVel = self.zoomer15.getCurrentXVelocity()
        self.zoomerObject15.yVel = self.zoomer15.getCurrentYVelocity()

        self.zoomerObject16 = engine.GameObject()
        self.zoomerPhysics16 = engine.PhysicsComponent()
        self.zoomerTransform16 = engine.Transform()
        self.zoomerTransform16.xPos = 100
        self.zoomerTransform16.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 41) - self.zoomerSize
        self.zoomer_sprite_16_1 = engine.Sprite(self.zoomerTransform16, True)
        self.zoomer_sprite_16_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_16_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_16_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_16_2 = engine.Sprite(self.zoomerTransform16, True)
        self.zoomer_sprite_16_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_16_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_16_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_16_3 = engine.Sprite(self.zoomerTransform16, True)
        self.zoomer_sprite_16_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_16_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_16_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_16_4 = engine.Sprite(self.zoomerTransform16, True)
        self.zoomer_sprite_16_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_16_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_16_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject16.addTileMapComponent(self.tilemap3)
        self.zoomerObject16.addPhysicsComponent(self.zoomerPhysics16)
        self.zoomerObject16.addTransformComponent(self.zoomerTransform16)
        self.zoomerObject16.addSpriteComponent(self.zoomer_sprite_16_1)
        self.zoomer16 = Zoomer(self.zoomerObject16, 0, True)
        self.zoomer16.addSpriteToList(self.zoomer_sprite_16_1, 1)
        self.zoomer16.addSpriteToList(self.zoomer_sprite_16_2, 1)
        self.zoomer16.addSpriteToList(self.zoomer_sprite_16_3, 1)
        self.zoomer16.addSpriteToList(self.zoomer_sprite_16_4, 1)
        self.zoomer16.setActiveStatus(True)
        self.zoomerObject16.xVel = self.zoomer16.getCurrentXVelocity()
        self.zoomerObject16.yVel = self.zoomer16.getCurrentYVelocity()

        self.zoomerObject17 = engine.GameObject()
        self.zoomerPhysics17 = engine.PhysicsComponent()
        self.zoomerTransform17 = engine.Transform()
        self.zoomerTransform17.xPos = 200
        self.zoomerTransform17.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 48) - self.zoomerSize
        self.zoomer_sprite_17_1 = engine.Sprite(self.zoomerTransform17, True)
        self.zoomer_sprite_17_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_17_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_17_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_17_2 = engine.Sprite(self.zoomerTransform17, True)
        self.zoomer_sprite_17_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_17_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_17_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_17_3 = engine.Sprite(self.zoomerTransform17, True)
        self.zoomer_sprite_17_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_17_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_17_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_17_4 = engine.Sprite(self.zoomerTransform17, True)
        self.zoomer_sprite_17_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_17_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_17_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject17.addTileMapComponent(self.tilemap3)
        self.zoomerObject17.addPhysicsComponent(self.zoomerPhysics17)
        self.zoomerObject17.addTransformComponent(self.zoomerTransform17)
        self.zoomerObject17.addSpriteComponent(self.zoomer_sprite_17_1)
        self.zoomer17 = Zoomer(self.zoomerObject17, 0, True)
        self.zoomer17.addSpriteToList(self.zoomer_sprite_17_1, 1)
        self.zoomer17.addSpriteToList(self.zoomer_sprite_17_2, 1)
        self.zoomer17.addSpriteToList(self.zoomer_sprite_17_3, 1)
        self.zoomer17.addSpriteToList(self.zoomer_sprite_17_4, 1)
        self.zoomer17.setActiveStatus(True)
        self.zoomerObject17.xVel = self.zoomer17.getCurrentXVelocity()
        self.zoomerObject17.yVel = self.zoomer17.getCurrentYVelocity()

        self.zoomerObject18 = engine.GameObject()
        self.zoomerPhysics18 = engine.PhysicsComponent()
        self.zoomerTransform18 = engine.Transform()
        self.zoomerTransform18.xPos = 300
        self.zoomerTransform18.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 55) - self.zoomerSize
        self.zoomer_sprite_18_1 = engine.Sprite(self.zoomerTransform18, True)
        self.zoomer_sprite_18_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_18_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_18_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_18_2 = engine.Sprite(self.zoomerTransform18, True)
        self.zoomer_sprite_18_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_18_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_18_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_18_3 = engine.Sprite(self.zoomerTransform18, True)
        self.zoomer_sprite_18_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_18_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_18_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_18_4 = engine.Sprite(self.zoomerTransform18, True)
        self.zoomer_sprite_18_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_18_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_18_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject18.addTileMapComponent(self.tilemap3)
        self.zoomerObject18.addPhysicsComponent(self.zoomerPhysics18)
        self.zoomerObject18.addTransformComponent(self.zoomerTransform18)
        self.zoomerObject18.addSpriteComponent(self.zoomer_sprite_18_1)
        self.zoomer18 = Zoomer(self.zoomerObject18, 0, True)
        self.zoomer18.addSpriteToList(self.zoomer_sprite_18_1, 1)
        self.zoomer18.addSpriteToList(self.zoomer_sprite_18_2, 1)
        self.zoomer18.addSpriteToList(self.zoomer_sprite_18_3, 1)
        self.zoomer18.addSpriteToList(self.zoomer_sprite_18_4, 1)
        self.zoomer18.setActiveStatus(True)
        self.zoomerObject18.xVel = self.zoomer18.getCurrentXVelocity()
        self.zoomerObject18.yVel = self.zoomer18.getCurrentYVelocity()

        self.zoomerObject19 = engine.GameObject()
        self.zoomerPhysics19 = engine.PhysicsComponent()
        self.zoomerTransform19 = engine.Transform()
        self.zoomerTransform19.xPos = 100
        self.zoomerTransform19.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 62) - self.zoomerSize
        self.zoomer_sprite_19_1 = engine.Sprite(self.zoomerTransform19, True)
        self.zoomer_sprite_19_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_19_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_19_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_19_2 = engine.Sprite(self.zoomerTransform19, True)
        self.zoomer_sprite_19_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_19_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_19_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_19_3 = engine.Sprite(self.zoomerTransform19, True)
        self.zoomer_sprite_19_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_19_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_19_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_19_4 = engine.Sprite(self.zoomerTransform19, True)
        self.zoomer_sprite_19_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_19_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_19_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject19.addTileMapComponent(self.tilemap3)
        self.zoomerObject19.addPhysicsComponent(self.zoomerPhysics19)
        self.zoomerObject19.addTransformComponent(self.zoomerTransform19)
        self.zoomerObject19.addSpriteComponent(self.zoomer_sprite_19_1)
        self.zoomer19 = Zoomer(self.zoomerObject19, 0, True)
        self.zoomer19.addSpriteToList(self.zoomer_sprite_19_1, 1)
        self.zoomer19.addSpriteToList(self.zoomer_sprite_19_2, 1)
        self.zoomer19.addSpriteToList(self.zoomer_sprite_19_3, 1)
        self.zoomer19.addSpriteToList(self.zoomer_sprite_19_4, 1)
        self.zoomer19.setActiveStatus(True)
        self.zoomerObject19.xVel = self.zoomer19.getCurrentXVelocity()
        self.zoomerObject19.yVel = self.zoomer19.getCurrentYVelocity()

        self.zoomerObject20 = engine.GameObject()
        self.zoomerPhysics20 = engine.PhysicsComponent()
        self.zoomerTransform20 = engine.Transform()
        self.zoomerTransform20.xPos = 200
        self.zoomerTransform20.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 69) - self.zoomerSize
        self.zoomer_sprite_20_1 = engine.Sprite(self.zoomerTransform20, True)
        self.zoomer_sprite_20_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_20_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_20_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_20_2 = engine.Sprite(self.zoomerTransform20, True)
        self.zoomer_sprite_20_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_20_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_20_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_20_3 = engine.Sprite(self.zoomerTransform20, True)
        self.zoomer_sprite_20_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_20_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_20_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_20_4 = engine.Sprite(self.zoomerTransform20, True)
        self.zoomer_sprite_20_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_20_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_20_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject20.addTileMapComponent(self.tilemap3)
        self.zoomerObject20.addPhysicsComponent(self.zoomerPhysics20)
        self.zoomerObject20.addTransformComponent(self.zoomerTransform20)
        self.zoomerObject20.addSpriteComponent(self.zoomer_sprite_20_1)
        self.zoomer20 = Zoomer(self.zoomerObject20, 0, True)
        self.zoomer20.addSpriteToList(self.zoomer_sprite_20_1, 1)
        self.zoomer20.addSpriteToList(self.zoomer_sprite_20_2, 1)
        self.zoomer20.addSpriteToList(self.zoomer_sprite_20_3, 1)
        self.zoomer20.addSpriteToList(self.zoomer_sprite_20_4, 1)
        self.zoomer20.setActiveStatus(True)
        self.zoomerObject20.xVel = self.zoomer20.getCurrentXVelocity()
        self.zoomerObject20.yVel = self.zoomer20.getCurrentYVelocity()

        self.zoomerObject21 = engine.GameObject()
        self.zoomerPhysics21 = engine.PhysicsComponent()
        self.zoomerTransform21 = engine.Transform()
        self.zoomerTransform21.xPos = 300
        self.zoomerTransform21.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 76) - self.zoomerSize
        self.zoomer_sprite_21_1 = engine.Sprite(self.zoomerTransform21, True)
        self.zoomer_sprite_21_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_21_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_21_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_21_2 = engine.Sprite(self.zoomerTransform21, True)
        self.zoomer_sprite_21_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_21_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_21_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_21_3 = engine.Sprite(self.zoomerTransform21, True)
        self.zoomer_sprite_21_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_21_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_21_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_21_4 = engine.Sprite(self.zoomerTransform21, True)
        self.zoomer_sprite_21_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_21_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_21_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject21.addTileMapComponent(self.tilemap3)
        self.zoomerObject21.addPhysicsComponent(self.zoomerPhysics21)
        self.zoomerObject21.addTransformComponent(self.zoomerTransform21)
        self.zoomerObject21.addSpriteComponent(self.zoomer_sprite_21_1)
        self.zoomer21 = Zoomer(self.zoomerObject21, 0, True)
        self.zoomer21.addSpriteToList(self.zoomer_sprite_21_1, 1)
        self.zoomer21.addSpriteToList(self.zoomer_sprite_21_2, 1)
        self.zoomer21.addSpriteToList(self.zoomer_sprite_21_3, 1)
        self.zoomer21.addSpriteToList(self.zoomer_sprite_21_4, 1)
        self.zoomer21.setActiveStatus(True)
        self.zoomerObject21.xVel = self.zoomer21.getCurrentXVelocity()
        self.zoomerObject21.yVel = self.zoomer21.getCurrentYVelocity()

        self.zoomerObject22 = engine.GameObject()
        self.zoomerPhysics22 = engine.PhysicsComponent()
        self.zoomerTransform22 = engine.Transform()
        self.zoomerTransform22.xPos = 100
        self.zoomerTransform22.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 83) - self.zoomerSize
        self.zoomer_sprite_22_1 = engine.Sprite(self.zoomerTransform22, True)
        self.zoomer_sprite_22_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_22_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_22_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_22_2 = engine.Sprite(self.zoomerTransform22, True)
        self.zoomer_sprite_22_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_22_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_22_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_22_3 = engine.Sprite(self.zoomerTransform22, True)
        self.zoomer_sprite_22_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_22_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_22_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_22_4 = engine.Sprite(self.zoomerTransform22, True)
        self.zoomer_sprite_22_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_22_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_22_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject22.addTileMapComponent(self.tilemap3)
        self.zoomerObject22.addPhysicsComponent(self.zoomerPhysics22)
        self.zoomerObject22.addTransformComponent(self.zoomerTransform22)
        self.zoomerObject22.addSpriteComponent(self.zoomer_sprite_22_1)
        self.zoomer22 = Zoomer(self.zoomerObject22, 0, True)
        self.zoomer22.addSpriteToList(self.zoomer_sprite_22_1, 1)
        self.zoomer22.addSpriteToList(self.zoomer_sprite_22_2, 1)
        self.zoomer22.addSpriteToList(self.zoomer_sprite_22_3, 1)
        self.zoomer22.addSpriteToList(self.zoomer_sprite_22_4, 1)
        self.zoomer22.setActiveStatus(True)
        self.zoomerObject22.xVel = self.zoomer22.getCurrentXVelocity()
        self.zoomerObject22.yVel = self.zoomer22.getCurrentYVelocity()

        # zoomers on right platforms
        self.zoomerObject23 = engine.GameObject()
        self.zoomerPhysics23 = engine.PhysicsComponent()
        self.zoomerTransform23 = engine.Transform()
        self.zoomerTransform23.xPos = 650
        self.zoomerTransform23.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 12) - self.zoomerSize
        self.zoomer_sprite_23_1 = engine.Sprite(self.zoomerTransform23, True)
        self.zoomer_sprite_23_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_23_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_23_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_23_2 = engine.Sprite(self.zoomerTransform23, True)
        self.zoomer_sprite_23_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_23_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_23_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_23_3 = engine.Sprite(self.zoomerTransform23, True)
        self.zoomer_sprite_23_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_23_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_23_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_23_4 = engine.Sprite(self.zoomerTransform23, True)
        self.zoomer_sprite_23_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_23_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_23_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject23.addTileMapComponent(self.tilemap3)
        self.zoomerObject23.addPhysicsComponent(self.zoomerPhysics23)
        self.zoomerObject23.addTransformComponent(self.zoomerTransform23)
        self.zoomerObject23.addSpriteComponent(self.zoomer_sprite_23_1)
        self.zoomer23 = Zoomer(self.zoomerObject23, 0, False)
        self.zoomer23.addSpriteToList(self.zoomer_sprite_23_1, 1)
        self.zoomer23.addSpriteToList(self.zoomer_sprite_23_2, 1)
        self.zoomer23.addSpriteToList(self.zoomer_sprite_23_3, 1)
        self.zoomer23.addSpriteToList(self.zoomer_sprite_23_4, 1)
        self.zoomer23.setActiveStatus(True)
        self.zoomerObject23.xVel = self.zoomer23.getCurrentXVelocity()
        self.zoomerObject23.yVel = self.zoomer23.getCurrentYVelocity()

        self.zoomerObject24 = engine.GameObject()
        self.zoomerPhysics24 = engine.PhysicsComponent()
        self.zoomerTransform24 = engine.Transform()
        self.zoomerTransform24.xPos = 750
        self.zoomerTransform24.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 19) - self.zoomerSize
        self.zoomer_sprite_24_1 = engine.Sprite(self.zoomerTransform24, True)
        self.zoomer_sprite_24_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_24_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_24_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_24_2 = engine.Sprite(self.zoomerTransform24, True)
        self.zoomer_sprite_24_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_24_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_24_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_24_3 = engine.Sprite(self.zoomerTransform24, True)
        self.zoomer_sprite_24_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_24_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_24_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_24_4 = engine.Sprite(self.zoomerTransform24, True)
        self.zoomer_sprite_24_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_24_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_24_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject24.addTileMapComponent(self.tilemap3)
        self.zoomerObject24.addPhysicsComponent(self.zoomerPhysics24)
        self.zoomerObject24.addTransformComponent(self.zoomerTransform24)
        self.zoomerObject24.addSpriteComponent(self.zoomer_sprite_24_1)
        self.zoomer24 = Zoomer(self.zoomerObject24, 0, False)
        self.zoomer24.addSpriteToList(self.zoomer_sprite_24_1, 1)
        self.zoomer24.addSpriteToList(self.zoomer_sprite_24_2, 1)
        self.zoomer24.addSpriteToList(self.zoomer_sprite_24_3, 1)
        self.zoomer24.addSpriteToList(self.zoomer_sprite_24_4, 1)
        self.zoomer24.setActiveStatus(True)
        self.zoomerObject24.xVel = self.zoomer24.getCurrentXVelocity()
        self.zoomerObject24.yVel = self.zoomer24.getCurrentYVelocity()

        self.zoomerObject25 = engine.GameObject()
        self.zoomerPhysics25 = engine.PhysicsComponent()
        self.zoomerTransform25 = engine.Transform()
        self.zoomerTransform25.xPos = 850
        self.zoomerTransform25.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 26) - self.zoomerSize
        self.zoomer_sprite_25_1 = engine.Sprite(self.zoomerTransform25, True)
        self.zoomer_sprite_25_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_25_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_25_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_25_2 = engine.Sprite(self.zoomerTransform25, True)
        self.zoomer_sprite_25_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_25_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_25_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_25_3 = engine.Sprite(self.zoomerTransform25, True)
        self.zoomer_sprite_25_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_25_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_25_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_25_4 = engine.Sprite(self.zoomerTransform25, True)
        self.zoomer_sprite_25_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_25_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_25_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject25.addTileMapComponent(self.tilemap3)
        self.zoomerObject25.addPhysicsComponent(self.zoomerPhysics25)
        self.zoomerObject25.addTransformComponent(self.zoomerTransform25)
        self.zoomerObject25.addSpriteComponent(self.zoomer_sprite_25_1)
        self.zoomer25 = Zoomer(self.zoomerObject25, 0, False)
        self.zoomer25.addSpriteToList(self.zoomer_sprite_25_1, 1)
        self.zoomer25.addSpriteToList(self.zoomer_sprite_25_2, 1)
        self.zoomer25.addSpriteToList(self.zoomer_sprite_25_3, 1)
        self.zoomer25.addSpriteToList(self.zoomer_sprite_25_4, 1)
        self.zoomer25.setActiveStatus(True)
        self.zoomerObject25.xVel = self.zoomer25.getCurrentXVelocity()
        self.zoomerObject25.yVel = self.zoomer25.getCurrentYVelocity()

        self.zoomerObject26 = engine.GameObject()
        self.zoomerPhysics26 = engine.PhysicsComponent()
        self.zoomerTransform26 = engine.Transform()
        self.zoomerTransform26.xPos = 650
        self.zoomerTransform26.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 33) - self.zoomerSize
        self.zoomer_sprite_26_1 = engine.Sprite(self.zoomerTransform26, True)
        self.zoomer_sprite_26_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_26_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_26_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_26_2 = engine.Sprite(self.zoomerTransform26, True)
        self.zoomer_sprite_26_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_26_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_26_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_26_3 = engine.Sprite(self.zoomerTransform26, True)
        self.zoomer_sprite_26_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_26_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_26_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_26_4 = engine.Sprite(self.zoomerTransform26, True)
        self.zoomer_sprite_26_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_26_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_26_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject26.addTileMapComponent(self.tilemap3)
        self.zoomerObject26.addPhysicsComponent(self.zoomerPhysics26)
        self.zoomerObject26.addTransformComponent(self.zoomerTransform26)
        self.zoomerObject26.addSpriteComponent(self.zoomer_sprite_26_1)
        self.zoomer26 = Zoomer(self.zoomerObject26, 0, False)
        self.zoomer26.addSpriteToList(self.zoomer_sprite_26_1, 1)
        self.zoomer26.addSpriteToList(self.zoomer_sprite_26_2, 1)
        self.zoomer26.addSpriteToList(self.zoomer_sprite_26_3, 1)
        self.zoomer26.addSpriteToList(self.zoomer_sprite_26_4, 1)
        self.zoomer26.setActiveStatus(True)
        self.zoomerObject26.xVel = self.zoomer26.getCurrentXVelocity()
        self.zoomerObject26.yVel = self.zoomer26.getCurrentYVelocity()

        self.zoomerObject27 = engine.GameObject()
        self.zoomerPhysics27 = engine.PhysicsComponent()
        self.zoomerTransform27 = engine.Transform()
        self.zoomerTransform27.xPos = 750
        self.zoomerTransform27.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 40) - self.zoomerSize
        self.zoomer_sprite_27_1 = engine.Sprite(self.zoomerTransform27, True)
        self.zoomer_sprite_27_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_27_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_27_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_27_2 = engine.Sprite(self.zoomerTransform27, True)
        self.zoomer_sprite_27_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_27_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_27_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_27_3 = engine.Sprite(self.zoomerTransform27, True)
        self.zoomer_sprite_27_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_27_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_27_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_27_4 = engine.Sprite(self.zoomerTransform27, True)
        self.zoomer_sprite_27_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_27_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_27_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject27.addPhysicsComponent(self.zoomerPhysics27)
        self.zoomerObject27.addTransformComponent(self.zoomerTransform27)
        self.zoomerObject27.addSpriteComponent(self.zoomer_sprite_27_1)
        self.zoomerObject27.addTileMapComponent(self.tilemap3)
        self.zoomer27 = Zoomer(self.zoomerObject27, 0, False)
        self.zoomer27.addSpriteToList(self.zoomer_sprite_27_1, 1)
        self.zoomer27.addSpriteToList(self.zoomer_sprite_27_2, 1)
        self.zoomer27.addSpriteToList(self.zoomer_sprite_27_3, 1)
        self.zoomer27.addSpriteToList(self.zoomer_sprite_27_4, 1)
        self.zoomer27.setActiveStatus(True)
        self.zoomerObject27.xVel = self.zoomer27.getCurrentXVelocity()
        self.zoomerObject27.yVel = self.zoomer27.getCurrentYVelocity()

        self.zoomerObject28 = engine.GameObject()
        self.zoomerPhysics28 = engine.PhysicsComponent()
        self.zoomerTransform28 = engine.Transform()
        self.zoomerTransform28.xPos = 850
        self.zoomerTransform28.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 47) - self.zoomerSize
        self.zoomer_sprite_28_1 = engine.Sprite(self.zoomerTransform28, True)
        self.zoomer_sprite_28_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_28_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_28_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_28_2 = engine.Sprite(self.zoomerTransform28, True)
        self.zoomer_sprite_28_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_28_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_28_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_28_3 = engine.Sprite(self.zoomerTransform28, True)
        self.zoomer_sprite_28_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_28_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_28_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_28_4 = engine.Sprite(self.zoomerTransform28, True)
        self.zoomer_sprite_28_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_28_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_28_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject28.addPhysicsComponent(self.zoomerPhysics28)
        self.zoomerObject28.addTransformComponent(self.zoomerTransform28)
        self.zoomerObject28.addSpriteComponent(self.zoomer_sprite_28_1)
        self.zoomerObject28.addTileMapComponent(self.tilemap3)
        self.zoomer28 = Zoomer(self.zoomerObject28, 0, False)
        self.zoomer28.addSpriteToList(self.zoomer_sprite_28_1, 1)
        self.zoomer28.addSpriteToList(self.zoomer_sprite_28_2, 1)
        self.zoomer28.addSpriteToList(self.zoomer_sprite_28_3, 1)
        self.zoomer28.addSpriteToList(self.zoomer_sprite_28_4, 1)
        self.zoomer28.setActiveStatus(True)
        self.zoomerObject28.xVel = self.zoomer28.getCurrentXVelocity()
        self.zoomerObject28.yVel = self.zoomer28.getCurrentYVelocity()

        self.zoomerObject29 = engine.GameObject()
        self.zoomerPhysics29 = engine.PhysicsComponent()
        self.zoomerTransform29 = engine.Transform()
        self.zoomerTransform29.xPos = 650
        self.zoomerTransform29.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 54) - self.zoomerSize
        self.zoomer_sprite_29_1 = engine.Sprite(self.zoomerTransform29, True)
        self.zoomer_sprite_29_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_29_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_29_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_29_2 = engine.Sprite(self.zoomerTransform29, True)
        self.zoomer_sprite_29_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_29_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_29_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_29_3 = engine.Sprite(self.zoomerTransform29, True)
        self.zoomer_sprite_29_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_29_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_29_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_29_4 = engine.Sprite(self.zoomerTransform29, True)
        self.zoomer_sprite_29_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_29_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_29_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject29.addPhysicsComponent(self.zoomerPhysics29)
        self.zoomerObject29.addTransformComponent(self.zoomerTransform29)
        self.zoomerObject29.addSpriteComponent(self.zoomer_sprite_29_1)
        self.zoomerObject29.addTileMapComponent(self.tilemap3)
        self.zoomer29 = Zoomer(self.zoomerObject29, 0, False)
        self.zoomer29.addSpriteToList(self.zoomer_sprite_29_1, 1)
        self.zoomer29.addSpriteToList(self.zoomer_sprite_29_2, 1)
        self.zoomer29.addSpriteToList(self.zoomer_sprite_29_3, 1)
        self.zoomer29.addSpriteToList(self.zoomer_sprite_29_4, 1)
        self.zoomer29.setActiveStatus(True)
        self.zoomerObject29.xVel = self.zoomer29.getCurrentXVelocity()
        self.zoomerObject29.yVel = self.zoomer29.getCurrentYVelocity()

        self.zoomerObject30 = engine.GameObject()
        self.zoomerPhysics30 = engine.PhysicsComponent()
        self.zoomerTransform30 = engine.Transform()
        self.zoomerTransform30.xPos = 750
        self.zoomerTransform30.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 61) - self.zoomerSize
        self.zoomer_sprite_30_1 = engine.Sprite(self.zoomerTransform30, True)
        self.zoomer_sprite_30_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_30_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_30_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_30_2 = engine.Sprite(self.zoomerTransform30, True)
        self.zoomer_sprite_30_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_30_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_30_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_30_3 = engine.Sprite(self.zoomerTransform30, True)
        self.zoomer_sprite_30_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_30_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_30_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_30_4 = engine.Sprite(self.zoomerTransform30, True)
        self.zoomer_sprite_30_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_30_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_30_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject30.addPhysicsComponent(self.zoomerPhysics30)
        self.zoomerObject30.addTransformComponent(self.zoomerTransform30)
        self.zoomerObject30.addSpriteComponent(self.zoomer_sprite_30_1)
        self.zoomerObject30.addTileMapComponent(self.tilemap3)
        self.zoomer30 = Zoomer(self.zoomerObject30, 0, False)
        self.zoomer30.addSpriteToList(self.zoomer_sprite_30_1, 1)
        self.zoomer30.addSpriteToList(self.zoomer_sprite_30_2, 1)
        self.zoomer30.addSpriteToList(self.zoomer_sprite_30_3, 1)
        self.zoomer30.addSpriteToList(self.zoomer_sprite_30_4, 1)
        self.zoomer30.setActiveStatus(True)
        self.zoomerObject30.xVel = self.zoomer30.getCurrentXVelocity()
        self.zoomerObject30.yVel = self.zoomer30.getCurrentYVelocity()

        self.zoomerObject31 = engine.GameObject()
        self.zoomerPhysics31 = engine.PhysicsComponent()
        self.zoomerTransform31 = engine.Transform()
        self.zoomerTransform31.xPos = 850
        self.zoomerTransform31.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 68) - self.zoomerSize
        self.zoomer_sprite_31_1 = engine.Sprite(self.zoomerTransform31, True)
        self.zoomer_sprite_31_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_31_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_31_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_31_2 = engine.Sprite(self.zoomerTransform31, True)
        self.zoomer_sprite_31_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_31_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_31_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_31_3 = engine.Sprite(self.zoomerTransform31, True)
        self.zoomer_sprite_31_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_31_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_31_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_31_4 = engine.Sprite(self.zoomerTransform31, True)
        self.zoomer_sprite_31_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_31_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_31_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject31.addPhysicsComponent(self.zoomerPhysics31)
        self.zoomerObject31.addTransformComponent(self.zoomerTransform31)
        self.zoomerObject31.addSpriteComponent(self.zoomer_sprite_31_1)
        self.zoomerObject31.addTileMapComponent(self.tilemap3)
        self.zoomer31 = Zoomer(self.zoomerObject31, 0, False)
        self.zoomer31.addSpriteToList(self.zoomer_sprite_31_1, 1)
        self.zoomer31.addSpriteToList(self.zoomer_sprite_31_2, 1)
        self.zoomer31.addSpriteToList(self.zoomer_sprite_31_3, 1)
        self.zoomer31.addSpriteToList(self.zoomer_sprite_31_4, 1)
        self.zoomer31.setActiveStatus(True)
        self.zoomerObject31.xVel = self.zoomer31.getCurrentXVelocity()
        self.zoomerObject31.yVel = self.zoomer31.getCurrentYVelocity()

        self.zoomerObject32 = engine.GameObject()
        self.zoomerPhysics32 = engine.PhysicsComponent()
        self.zoomerTransform32 = engine.Transform()
        self.zoomerTransform32.xPos = 650
        self.zoomerTransform32.yPos = self.tilemap3.getRows() * self.tileSize - (self.tileSize * 75) - self.zoomerSize
        self.zoomer_sprite_32_1 = engine.Sprite(self.zoomerTransform32, True)
        self.zoomer_sprite_32_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_32_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_32_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_32_2 = engine.Sprite(self.zoomerTransform32, True)
        self.zoomer_sprite_32_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_32_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_32_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_32_3 = engine.Sprite(self.zoomerTransform32, True)
        self.zoomer_sprite_32_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_32_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_32_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_32_4 = engine.Sprite(self.zoomerTransform32, True)
        self.zoomer_sprite_32_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_32_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_32_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject32.addPhysicsComponent(self.zoomerPhysics32)
        self.zoomerObject32.addTransformComponent(self.zoomerTransform32)
        self.zoomerObject32.addSpriteComponent(self.zoomer_sprite_32_1)
        self.zoomerObject32.addTileMapComponent(self.tilemap3)
        self.zoomer32 = Zoomer(self.zoomerObject32, 0, False)
        self.zoomer32.addSpriteToList(self.zoomer_sprite_32_1, 1)
        self.zoomer32.addSpriteToList(self.zoomer_sprite_32_2, 1)
        self.zoomer32.addSpriteToList(self.zoomer_sprite_32_3, 1)
        self.zoomer32.addSpriteToList(self.zoomer_sprite_32_4, 1)
        self.zoomer32.setActiveStatus(True)
        self.zoomerObject32.xVel = self.zoomer32.getCurrentXVelocity()
        self.zoomerObject32.yVel = self.zoomer32.getCurrentYVelocity()

        # zoomer for tilemap1
        self.zoomerObject33 = engine.GameObject()
        self.zoomerPhysics33 = engine.PhysicsComponent()
        self.zoomerTransform33 = engine.Transform()
        self.zoomerTransform33.xPos = self.tilemap1.getCols() * self.tileSize - (self.tileSize * 13)
        self.zoomerTransform33.yPos = (self.tileSize * 7) - self.zoomerSize
        self.zoomer_sprite_33_1 = engine.Sprite(self.zoomerTransform33, True)
        self.zoomer_sprite_33_1.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_33_1.setSpriteSheetDimensions(18, 14, 8, 7, 2, 2, 0)
        self.zoomer_sprite_33_1.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_33_2 = engine.Sprite(self.zoomerTransform33, True)
        self.zoomer_sprite_33_2.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_33_2.setSpriteSheetDimensions(16, 18, 44, 4, 2, 2, 1)
        self.zoomer_sprite_33_2.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_33_3 = engine.Sprite(self.zoomerTransform33, True)
        self.zoomer_sprite_33_3.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 40, 36
        self.zoomer_sprite_33_3.setSpriteSheetDimensions(18, 14, 76, 7, 2, 2, 0)
        self.zoomer_sprite_33_3.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomer_sprite_33_4 = engine.Sprite(self.zoomerTransform33, True)
        self.zoomer_sprite_33_4.setRectangleDimensions(self.zoomerSize, self.zoomerSize) # 36, 40
        self.zoomer_sprite_33_4.setSpriteSheetDimensions(16, 18, 112, 4, 2, 2, 1)
        self.zoomer_sprite_33_4.loadImage('Assets/spritesheets/enemies.png', self.sdl.getSDLRenderer())
        self.zoomerObject33.addPhysicsComponent(self.zoomerPhysics33)
        self.zoomerObject33.addTransformComponent(self.zoomerTransform33)
        self.zoomerObject33.addSpriteComponent(self.zoomer_sprite_33_1)
        self.zoomerObject33.addTileMapComponent(self.tilemap1)
        self.zoomer33 = Zoomer(self.zoomerObject33, 0, False)
        self.zoomer33.addSpriteToList(self.zoomer_sprite_33_1, 1)
        self.zoomer33.addSpriteToList(self.zoomer_sprite_33_2, 1)
        self.zoomer33.addSpriteToList(self.zoomer_sprite_33_3, 1)
        self.zoomer33.addSpriteToList(self.zoomer_sprite_33_4, 1)
        self.zoomer33.setActiveStatus(True)
        self.zoomerObject33.xVel = self.zoomer33.getCurrentXVelocity()
        self.zoomerObject33.yVel = self.zoomer33.getCurrentYVelocity()

        self.zoomerArray = []
        self.zoomerArray.append(self.zoomer1)
        self.zoomerArray.append(self.zoomer2)
        self.zoomerArray.append(self.zoomer3)
        self.zoomerArray.append(self.zoomer4)
        self.zoomerArray.append(self.zoomer5)
        self.zoomerArray.append(self.zoomer6)
        self.zoomerArray.append(self.zoomer7)
        self.zoomerArray.append(self.zoomer8)
        self.zoomerArray.append(self.zoomer9)
        self.zoomerArray.append(self.zoomer10)
        self.zoomerArray.append(self.zoomer11)
        self.zoomerArray.append(self.zoomer12)
        self.zoomerArray.append(self.zoomer13)
        self.zoomerArray.append(self.zoomer14)
        self.zoomerArray.append(self.zoomer15)
        self.zoomerArray.append(self.zoomer16)
        self.zoomerArray.append(self.zoomer17)
        self.zoomerArray.append(self.zoomer18)
        self.zoomerArray.append(self.zoomer19)
        self.zoomerArray.append(self.zoomer20)
        self.zoomerArray.append(self.zoomer21)
        self.zoomerArray.append(self.zoomer22)
        self.zoomerArray.append(self.zoomer23)
        self.zoomerArray.append(self.zoomer24)
        self.zoomerArray.append(self.zoomer25)
        self.zoomerArray.append(self.zoomer26)
        self.zoomerArray.append(self.zoomer27)
        self.zoomerArray.append(self.zoomer28)
        self.zoomerArray.append(self.zoomer29)
        self.zoomerArray.append(self.zoomer30)
        self.zoomerArray.append(self.zoomer31)
        self.zoomerArray.append(self.zoomer32)

        self.enemiesDict[str(self.tilemap3)] = {"zoomerArray": self.zoomerArray}
        self.enemiesDict[str(self.tilemap1)] = {"zoomerArray": [self.zoomer33]}

    def createPowerUpObjects(self):
        self.screwAttackObject = engine.GameObject()
        self.screwAttackPhysics = engine.PhysicsComponent()
        self.screwAttackTransform = engine.Transform()
        self.screwAttackTransform.xPos = self.lvlWidth4 - (self.tileSize * 12) - 7
        self.screwAttackTransform.yPos = self.tileSize * 9 - 14
        self.screwAttackSprite = engine.Sprite(self.screwAttackTransform, True)
        self.screwAttackSprite.setRectangleDimensions(50, 50)
        self.screwAttackSprite.setSpriteSheetDimensions(24, 16, 304, 128, 2, 2, 9)
        self.screwAttackSprite.loadImage('Assets/spritesheets/revamped_powerups.png', self.sdl.getSDLRenderer())
        self.screwAttackObject.addPhysicsComponent(self.screwAttackPhysics)
        self.screwAttackObject.addTransformComponent(self.screwAttackTransform)
        self.screwAttackObject.addSpriteComponent(self.screwAttackSprite)
        self.screwAttackObject.addTileMapComponent(self.tilemap4)

        self.powerUpDict = {}
        self.powerUpDict[str(self.tilemap4)] = self.screwAttackObject

        self.powerUpActiveDict = {}
        self.powerUpActiveDict[str(self.tilemap4)] = True

        self.powerUpFrameCountDict = {}
        self.powerUpFrameCountDict[str(self.tilemap4)] = 2

    def createExplodableTiles(self):
        self.explodableTilesDict = {}
        tileArr4 = []
        for i in range(11):
            xPos = self.tileSize * (39 + i)
            yPos = self.tileSize * 16
            tile = ExplodableTile(xPos, yPos, self.tileSize, self.tilemap4, self.sdl)
            tileArr4.append(tile)
        self.explodableTilesDict[str(self.tilemap4)] = tileArr4
    
    def changePlayerSprite(self, sprite):
        # adjusts yPos if necessary and changes sprite
        if sprite.getHeight() > self.player.mSprite.getHeight():
            self.player.mTransform.yPos -= (sprite.getHeight() - self.player.mSprite.getHeight())
        self.player.addSpriteComponent(sprite)
        self.currentMaxFrame = self.maxFrameDict[str(sprite)]

    # Handles player left and right movement from input
    def handlePlayerMove(self, inputs):
        jumpAgain = False
        if inputs[engine.J_PRESSED] and self.jumpTimer <= 0:
            jumpAgain = True
        if (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]) and not (inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]):
            if self.playerState.getState() == "standing":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isFirstStandingFrame:
                    self.playerTransform.yPos -= self.diffBetweenStandingAndDucking
                    self.isFirstStandingFrame = False
                    # change to running left
                    if self.isShooting():
                        self.changePlayerSprite(self.shooting_run_left)
                    else:
                        self.changePlayerSprite(self.run_left_sprite)
                        self.waitOneFrameForShot = True
                elif jumpAgain:
                    if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                        self.changePlayerSprite(self.aim_up_falling_left)
                    else:
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_falling_left)
                        else:
                            self.changePlayerSprite(self.falling_left)
                else:
                    if inputs[engine.UP_PRESSED]or inputs[engine.W_PRESSED]:
                        self.changePlayerSprite(self.aim_up_run_left)
                    else:
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_run_left)
                        else:
                            self.changePlayerSprite(self.run_left_sprite)
                            self.waitOneFrameForShot = True
            elif self.playerState.getState() == "ducking":
                self.waitOneFrameForShot = True
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.duck_left)
            elif self.playerState.getState() == "rolling":
                self.waitOneFrameForShot = True
                if self.isFirstRollingFrame:
                    self.playerTransform.yPos += self.diffBetweenDuckingAndRolling
                    self.isFirstRollingFrame = False
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.roll_left)
            elif self.playerState.getState() == "abouttostand":
                self.waitOneFrameForShot = True
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.duck_left)
            elif self.playerState.getState() == "jumping" or self.playerState.getState() == "aimupjumping":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
            elif self.playerState.getState() == "falling":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                    # change to aim_up_falling_left
                    self.playerState.setState("aimupfalling")
                    self.changePlayerSprite(self.aim_up_falling_left)
                else:
                    # change to falling left
                    if self.isShooting():
                        self.changePlayerSprite(self.shooting_falling_left)
                    else:
                        self.changePlayerSprite(self.falling_left)
                        self.waitOneFrameForShot = True
            elif self.playerState.getState() == "aimupfalling":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                    # change to aim up falling left
                    self.changePlayerSprite(self.aim_up_falling_left)
                else:
                    # change to falling left
                    self.playerState.setState("falling")
                    if self.isShooting():
                        self.changePlayerSprite(self.shooting_falling_left)
                    else:
                        self.changePlayerSprite(self.falling_left)
                        self.waitOneFrameForShot = True

        elif (inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]) and not (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]):
            if self.playerState.getState() == "standing":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isFirstStandingFrame:
                    self.isFirstStandingFrame = False
                    # change to running right
                    if self.isShooting():
                        self.changePlayerSprite(self.shooting_run_right)
                    else:
                        self.changePlayerSprite(self.run_right_sprite)
                        self.waitOneFrameForShot = True
                elif jumpAgain:
                    if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                        self.changePlayerSprite(self.aim_up_falling_right)
                    else:
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_falling_right)
                        else:
                            self.changePlayerSprite(self.falling_right)
                else:
                    if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                        self.changePlayerSprite(self.aim_up_run_right)
                    else:
                        # change to running right
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_run_right)
                        else:
                            self.changePlayerSprite(self.run_right_sprite)
                            self.waitOneFrameForShot = True
            elif self.playerState.getState() == "ducking":
                self.waitOneFrameForShot = True
                # self.playerTransform.yPos += self.diffBetweenStandingAndDucking
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.duck_right)
            elif self.playerState.getState() == "rolling":
                self.waitOneFrameForShot = True
                if self.isFirstRollingFrame:
                    self.playerTransform.yPos += self.diffBetweenDuckingAndRolling
                    self.isFirstRollingFrame = False
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.roll_right)
            elif self.playerState.getState() == "abouttostand":
                self.waitOneFrameForShot = True
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.duck_right)
            elif self.playerState.getState() == "jumping" or self.playerState.getState() == "aimupjumping":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
            elif self.playerState.getState() == "falling":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                    # change to aim_up_falling_right
                    self.playerState.setState("aimupfalling")
                    self.changePlayerSprite(self.aim_up_falling_right)
                else:
                    # change to falling right
                    if self.isShooting():
                        self.changePlayerSprite(self.shooting_falling_right)
                    else:
                        self.changePlayerSprite(self.falling_right)
                        self.waitOneFrameForShot = True
            elif self.playerState.getState() == "aimupfalling":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                    self.changePlayerSprite(self.aim_up_falling_right)
                else:
                    # change to falling right
                    self.playerState.setState("falling")
                    if self.isShooting():
                        self.changePlayerSprite(self.shooting_falling_right)
                    else:
                        self.changePlayerSprite(self.falling_right)
                        self.waitOneFrameForShot = True

        else:
            # player does not move along x-axis
            if self.playerState.getState() == "standing":
                self.player.xVel = 0
                if self.curXDirection > 0:
                    if inputs[engine.UP_PRESSED]or inputs[engine.W_PRESSED]:
                        # switch to aiming up
                        if jumpAgain:
                            self.changePlayerSprite(self.aim_up_falling_right)
                        elif self.isFirstStandingFrame:
                            self.isFirstStandingFrame = False
                            self.changePlayerSprite(self.aim_up_idle_right)
                        else:
                            self.changePlayerSprite(self.aim_up_idle_right)
                    else:
                        # switch to idle_right
                        if jumpAgain:
                            self.changePlayerSprite(self.falling_right)
                        elif self.isFirstStandingFrame:
                            self.isFirstStandingFrame = False
                            self.changePlayerSprite(self.idle_right)
                        else:
                            self.changePlayerSprite(self.idle_right)

                else:
                    if inputs[engine.UP_PRESSED]or inputs[engine.W_PRESSED]:
                        # switch to aiming up
                        if jumpAgain:
                            self.changePlayerSprite(self.aim_up_falling_left)
                        elif self.isFirstStandingFrame:
                            self.isFirstStandingFrame = False
                            self.changePlayerSprite(self.aim_up_idle_left)
                        else:
                            self.changePlayerSprite(self.aim_up_idle_left)
                    else:
                        # switch to idle_left
                        if jumpAgain:
                            self.changePlayerSprite(self.falling_left)
                        elif self.isFirstStandingFrame:
                            self.isFirstStandingFrame = False
                            self.changePlayerSprite(self.idle_left)
                        else:
                            self.changePlayerSprite(self.idle_left)
            elif self.playerState.getState() == "ducking":
                self.waitOneFrameForShot = True
                self.player.xVel = 0
                if self.curXDirection > 0:
                    self.changePlayerSprite(self.duck_right)
                else:
                    self.changePlayerSprite(self.duck_left)
            elif self.playerState.getState() == "rolling":
                self.waitOneFrameForShot = True
                if self.isFirstRollingFrame:
                    self.playerTransform.yPos += self.diffBetweenDuckingAndRolling
                    self.isFirstRollingFrame = False
                self.player.xVel = 0
                if self.curXDirection > 0:
                    self.changePlayerSprite(self.roll_right)
                else:
                    self.changePlayerSprite(self.roll_left)
            elif self.playerState.getState() == "abouttostand":
                self.waitOneFrameForShot = True
                self.player.xVel = 0
                if self.curXDirection > 0:
                    self.changePlayerSprite(self.duck_right)
                else:
                    self.changePlayerSprite(self.duck_left)
            elif self.playerState.getState() == "jumping" or self.playerState.getState() == "aimupjumping":
                self.player.xVel = 0
            elif self.playerState.getState() == "falling":
                self.player.xVel = 0
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                    if self.curXDirection > 0:
                        self.changePlayerSprite(self.aim_up_falling_right)
                    else:
                        self.changePlayerSprite(self.aim_up_falling_left)
                else:
                    if self.curXDirection > 0:
                        # switch to fall right
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_falling_right)
                        else:
                            self.changePlayerSprite(self.falling_right)
                            self.waitOneFrameForShot = True
                    else:
                        # switch to fall left
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_falling_left)
                        else:
                            self.changePlayerSprite(self.falling_left)
                            self.waitOneFrameForShot = True
            elif self.playerState.getState() == "aimupfalling":
                self.player.xVel = 0
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                    if self.curXDirection > 0:
                        self.changePlayerSprite(self.aim_up_falling_right)
                    else:
                        self.changePlayerSprite(self.aim_up_falling_left)
                else:
                    if self.curXDirection > 0:
                        # switch to fall right
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_falling_right)
                        else:
                            self.changePlayerSprite(self.falling_right)
                            self.waitOneFrameForShot = True
                    else:
                        # switch to fall left
                        if self.isShooting():
                            self.changePlayerSprite(self.shooting_falling_left)
                        else:
                            self.changePlayerSprite(self.falling_left)
                            self.waitOneFrameForShot = True

    def animateRoomChangeToTheRight(self, curTilemap, nextTilemap):
        # Set level sizes
        leftLvlWidth = curTilemap.getCols() * self.tileSize
        rightLvlWidth = nextTilemap.getCols() * self.tileSize
        leftLvlHeight = curTilemap.getRows() * self.tileSize
        rightLvlHeight = nextTilemap.getRows() * self.tileSize
        # Set up 2 cameras
        if self.sideOrVertDict[str(curTilemap)] == "horizontal":
            self.leftCamera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, leftLvlWidth, 
                                                    leftLvlHeight, self.player.mSprite)
        elif self.sideOrVertDict[str(curTilemap)] == "vertical":
            self.leftCamera = engine.SpriteVerticalScrollerCamera(self.windowWidth, self.windowHeight, leftLvlWidth,
                                                                  leftLvlHeight, self.player.mSprite)
        if self.sideOrVertDict[str(nextTilemap)] == "horizontal":
            self.rightCamera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, rightLvlWidth, 
                                                    rightLvlHeight, self.player.mSprite)
        elif self.sideOrVertDict[str(nextTilemap)] == "vertical":
            self.rightCamera = engine.SpriteVerticalScrollerCamera(self.windowWidth, self.windowHeight, rightLvlWidth,
                                                                   rightLvlHeight, self.player.mSprite)
            # self.player.addTileMapComponent(nextTilemap)
            self.player.mJumpComponent.changeInitialY(rightLvlHeight - leftLvlHeight)
            self.player.mTransform.yPos = rightLvlHeight - (leftLvlHeight - self.player.mTransform.yPos)
            
        
        if self.sideOrVertDict[str(curTilemap)] == "horizontal":
            self.leftCamera.y = self.camera.y
            self.rightCamera.y = self.camera.y
        elif self.sideOrVertDict[str(curTilemap)] == "vertical":
            self.leftCamera.y = self.camera.y
            self.rightCamera.y = self.camera.y
        if self.sideOrVertDict[str(nextTilemap)] == "horizontal":
            self.leftCamera.y = self.camera.y
            self.rightCamera.y = self.camera.y
        elif self.sideOrVertDict[str(nextTilemap)] == "vertical":
            self.leftCamera.y = self.camera.y
            # from the bottom
            self.rightCamera.y = rightLvlHeight - self.windowHeight

        self.leftCamera.x = self.camera.x
        self.rightCamera.x = -self.windowWidth

        xVelocity = 8

        # close doors
        self.closeCorrectDoor(curTilemap, nextTilemap)
        
        while self.rightCamera.x < 0:
            self.frameStartTime = self.sdl.getTimeMS()
            self.UpdateAnimation(curTilemap, nextTilemap)
            self.RenderAnimation(curTilemap, nextTilemap, self.leftCamera, self.rightCamera)
            self.limitFPS()
            self.leftCamera.x += xVelocity
            self.rightCamera.x += xVelocity

        # adjust cameras to 0 position
        cameraXDiff = self.rightCamera.x
        if cameraXDiff >= 0:
            self.rightCamera.x -= cameraXDiff
            self.leftCamera.x -= cameraXDiff
        
        # reset all enemies in curTilemap (previous)
        self.resetEnemies(curTilemap)
        
        # open all doors
        self.openCorrectDoor(curTilemap, nextTilemap)
        count = 0
        while count <= 5:
            self.frameStartTime = self.sdl.getTimeMS()
            self.UpdateAnimation(curTilemap, nextTilemap)
            self.RenderAnimation(curTilemap, nextTilemap, self.leftCamera, self.rightCamera)
            self.limitFPS()
            count += 1
        
        # change tilemap
        self.tilemap = nextTilemap
        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        # Player Tilemap Component
        self.player.addTileMapComponent(self.tilemap)
        # Change self.camera to rightCamera
        self.camera = self.rightCamera
        # place player sprite
        self.player.mTransform.xPos = self.tileSize
    
    def animateRoomChangeToTheLeft(self, curTilemap, nextTilemap):
        # Set level sizes
        rightLvlWidth = curTilemap.getCols() * self.tileSize
        leftLvlWidth = nextTilemap.getCols() * self.tileSize
        rightLvlHeight = curTilemap.getRows() * self.tileSize
        leftLvlHeight = nextTilemap.getRows() * self.tileSize
        # Set up 2 cameras
        if self.sideOrVertDict[str(curTilemap)] == "horizontal":
            self.rightCamera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, rightLvlWidth, 
                                                    rightLvlHeight, self.player.mSprite)
        elif self.sideOrVertDict[str(curTilemap)] == "vertical":
            self.rightCamera = engine.SpriteVerticalScrollerCamera(self.windowWidth, self.windowHeight, rightLvlWidth,
                                                                  rightLvlHeight, self.player.mSprite)
        if self.sideOrVertDict[str(nextTilemap)] == "horizontal":
            self.leftCamera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, leftLvlWidth, 
                                                    leftLvlHeight, self.player.mSprite)
        elif self.sideOrVertDict[str(nextTilemap)] == "vertical":
            self.leftCamera = engine.SpriteVerticalScrollerCamera(self.windowWidth, self.windowHeight, leftLvlWidth,
                                                                   leftLvlHeight, self.player.mSprite)
        
        if self.sideOrVertDict[str(curTilemap)] == "horizontal":
            self.rightCamera.y = self.camera.y
            self.leftCamera.y = leftLvlHeight - self.windowHeight
        elif self.sideOrVertDict[str(curTilemap)] == "vertical":
            self.rightCamera.y = self.camera.y
            self.leftCamera.y = leftLvlHeight - self.windowHeight
        if self.sideOrVertDict[str(nextTilemap)] == "horizontal":
            self.rightCamera.y = self.camera.y
            self.leftCamera.y = leftLvlHeight - self.windowHeight
            self.player.mJumpComponent.changeInitialY(leftLvlHeight - rightLvlHeight)
            self.player.mTransform.yPos = leftLvlHeight - (rightLvlHeight - self.player.mTransform.yPos)
        elif self.sideOrVertDict[str(nextTilemap)] == "vertical":
            self.rightCamera.y = self.camera.y
            self.leftCamera.y = self.camera.y

        self.rightCamera.x = self.camera.x
        self.leftCamera.x = leftLvlWidth
        
        xVelocity = 8

        # close doors
        self.closeCorrectDoor(curTilemap, nextTilemap)
        
        while self.leftCamera.x > leftLvlWidth - self.windowWidth:
            self.frameStartTime = self.sdl.getTimeMS()
            self.UpdateAnimation(nextTilemap, curTilemap)
            self.RenderAnimation(nextTilemap, curTilemap, self.leftCamera, self.rightCamera)
            self.limitFPS()
            self.leftCamera.x -= xVelocity
            self.rightCamera.x -= xVelocity

        # adjust cameras to 0 position
        cameraXDiff = self.rightCamera.x
        if cameraXDiff >= 0:
            self.rightCamera.x += cameraXDiff
            self.leftCamera.x += cameraXDiff
        # reset all enemies in curTilemap (previous)
        self.resetEnemies(curTilemap)
        
        # open all doors
        self.openCorrectDoor(curTilemap, nextTilemap)
        count = 0
        while count <= 5:
            self.frameStartTime = self.sdl.getTimeMS()
            self.UpdateAnimation(nextTilemap, curTilemap)
            self.RenderAnimation(nextTilemap, curTilemap, self.leftCamera, self.rightCamera)
            self.limitFPS()
            count += 1
        
        # change tilemap
        self.tilemap = nextTilemap
        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        # Player Tilemap Component
        self.player.addTileMapComponent(self.tilemap)
        # Change self.camera to rightCamera
        self.camera = self.leftCamera
        # place player sprite
        self.player.mTransform.xPos = leftLvlWidth - self.tileSize - self.player.mSprite.getWidth()

    def closeCorrectDoor(self, curTilemap, nextTilemap):
        bubbleDoor = self.whichDoorToCloseDict[str(curTilemap) + str(nextTilemap)]
        bubbleDoor.closeDoor()
        self.doorInflatingSound.PlaySound()

    def openCorrectDoor(self, curTilemap, nextTilemap):
        bubbleDoor = self.whichDoorToOpenDict[str(curTilemap) + str(nextTilemap)]
        bubbleDoor.openDoor()
        # end bubble door counter
        bubbleDoor.pauseTimer = bubbleDoor.maxPauseTimer + 1
        self.doorPoppingSound.PlaySound()

    def resetEnemies(self, tilemap):
        # count = 1
        if str(tilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(tilemap)]:
                for bug in self.enemiesDict[str(tilemap)]["bugArray"]:
                    # count += 1
                    bug.setActiveStatus(True)
            if "zoomerArray" in self.enemiesDict[str(tilemap)]:
                for zoomer in self.enemiesDict[str(tilemap)]["zoomerArray"]:
                    zoomer.setActiveStatus(True)

    def UpdateAnimation(self, leftTilemap, rightTilemap):
        if str(leftTilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(leftTilemap)]:
                for bug in self.enemiesDict[str(leftTilemap)]["bugArray"]:
                    self.handleBugUpdate(bug, leftTilemap, True)
            if "zoomerArray" in self.enemiesDict[str(leftTilemap)]:
                for zoomer in self.enemiesDict[str(leftTilemap)]["zoomerArray"]:
                    self.handleZoomerUpdate(zoomer, leftTilemap, True)
        if str(rightTilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(rightTilemap)]:
                for bug in self.enemiesDict[str(rightTilemap)]["bugArray"]:
                    self.handleBugUpdate(bug, rightTilemap, True)
            if "zoomerArray" in self.enemiesDict[str(rightTilemap)]:
                for zoomer in self.enemiesDict[str(rightTilemap)]["zoomerArray"]:
                    self.handleZoomerUpdate(zoomer, rightTilemap, True)
        if str(leftTilemap) in self.doorObjectsDict.keys():
            for doorObject in self.doorObjectsDict[str(leftTilemap)]:
                doorObject.mSprite.update(0, 0, 0)
        if str(rightTilemap) in self.doorObjectsDict.keys():
            for doorObject in self.doorObjectsDict[str(rightTilemap)]:
                doorObject.mSprite.update(0, 0, 0)
        self.bubbleDoorsUpdate(leftTilemap)
        self.bubbleDoorsUpdate(rightTilemap)

    # modify Render method for animation needs
    def RenderAnimation(self, leftTilemap, rightTilemap, leftCamera, rightCamera):
        #self.sdl.clear(60, 60, 60, 255) # TODO: Set background to black
        self.sdl.clear(0, 0, 0, 0) # This is code for black background
        leftTilemap.Render(self.sdl.getSDLRenderer(), leftCamera.x, leftCamera.y)
        rightTilemap.Render(self.sdl.getSDLRenderer(), rightCamera.x, rightCamera.y)
        # self.player.mSprite.render(self.sdl.getSDLRenderer(), leftCamera.x, leftCamera.y)
        self.renderEnemiesInAnimation(leftTilemap, rightTilemap, leftCamera, rightCamera)
        self.renderDoorObjectsInAnimation(leftTilemap, rightTilemap, leftCamera, rightCamera)
        self.renderBubbleDoorsInAnimation(leftTilemap, rightTilemap, leftCamera, rightCamera)
        self.sdl.flip()

    def renderEnemiesInAnimation(self, leftTilemap, rightTilemap, leftCamera, rightCamera):
        if str(leftTilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(leftTilemap)]:
                for bug in self.enemiesDict[str(leftTilemap)]["bugArray"]:
                    if bug.isActive():
                        bug.getBugObject().mSprite.render(self.sdl.getSDLRenderer(), leftCamera.x, leftCamera.y)
            if "zoomerArray" in self.enemiesDict[str(leftTilemap)]:
                for zoomer in self.enemiesDict[str(leftTilemap)]["zoomerArray"]:
                    if zoomer.isActive():
                        zoomer.getZoomerObject().mSprite.render(self.sdl.getSDLRenderer(), leftCamera.x, leftCamera.y)
        if str(rightTilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(rightTilemap)]:
                for bug in self.enemiesDict[str(rightTilemap)]["bugArray"]:
                    if bug.isActive():
                        bug.getBugObject().mSprite.render(self.sdl.getSDLRenderer(), rightCamera.x, rightCamera.y)
            if "zoomerArray" in self.enemiesDict[str(rightTilemap)]:
                for zoomer in self.enemiesDict[str(rightTilemap)]["zoomerArray"]:
                    if zoomer.isActive():
                        zoomer.getZoomerObject().mSprite.render(self.sdl.getSDLRenderer(), rightCamera.x, rightCamera.y)

    def renderDoorObjectsInAnimation(self, leftTilemap, rightTilemap, leftCamera, rightCamera):
        if str(leftTilemap) in self.doorObjectsDict.keys():
            for doorObject in self.doorObjectsDict[str(leftTilemap)]:
                doorObject.mSprite.render(self.sdl.getSDLRenderer(), leftCamera.x, leftCamera.y)
        if str(rightTilemap) in self.doorObjectsDict.keys():
            for doorObject in self.doorObjectsDict[str(rightTilemap)]:
                doorObject.mSprite.render(self.sdl.getSDLRenderer(), rightCamera.x, rightCamera.y)
        
    def renderBubbleDoorsInAnimation(self, leftTilemap, rightTilemap, leftCamera, rightCamera):
        if str(leftTilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(leftTilemap)]:
                bubbleDoor.getSpriteComponent().render(self.sdl.getSDLRenderer(), leftCamera.x, leftCamera.y)
        if str(rightTilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(rightTilemap)]:
                bubbleDoor.getSpriteComponent().render(self.sdl.getSDLRenderer(), rightCamera.x, rightCamera.y)
    
    def isShooting(self):
        if self.shootingCounter <= self.shootingCounterMax:
            return True
        return False

    def handlePlayerShooting(self, inputs):
        state = self.playerState.getState()
        if (inputs[engine.H_PRESSED] or inputs[engine.K_PRESSED] and not (state == "rolling" or state == "ducking" or state == "abouttostand")):
            self.shootingCounter = 0
            if self.waitOneFrameForShot:
                self.waitOneFrameForShot = False
            elif self.shotPauseTimer > self.shotPauseMax:
                self.createBullet()
                self.shotPauseTimer = 0
                self.bulletCreatedSound.PlaySound()
        self.shotPauseTimer += 1
    
    def createBullet(self):
        bullet = engine.GameObject()
        transform = engine.Transform()
        physics = engine.PhysicsComponent()
        # create bullet_sprite
        bullet_sprite = engine.Sprite(transform, True)
        bullet_sprite.setRectangleDimensions(10, 10)
        bullet_sprite.setSpriteSheetDimensions(8, 8, 21, 289, 1, 1, 0)
        bullet_sprite.loadImage("Assets/spritesheets/MetroidWeaponsSpriteSheet.bmp", self.sdl.getSDLRenderer())
        bullet.addSpriteComponent(bullet_sprite)
        bullet.addTransformComponent(transform)
        bullet.addPhysicsComponent(physics)
        bullet = self.setBulletStartingPointAndSetVelocity(bullet)
        # put bullet in dict
        if len(self.bulletDict) == 0:
            self.bulletIndex = 0
        self.bulletDict[self.bulletIndex] = [bullet, 0]
        self.spriteDict[self.bulletIndex] = bullet_sprite
        self.transformDict[self.bulletIndex] = transform
        self.physicsDict[self.bulletIndex] = physics
        self.bulletIndex += 1
    
    def setBulletStartingPointAndSetVelocity(self, bullet):
        sprite = self.player.mSprite
        match sprite:
            case self.aim_up_falling_right:
                bullet.xVel = 0
                bullet.yVel = -self.bulletSpeed
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.5)
                bullet.mTransform.yPos = self.player.mTransform.yPos
            case self.aim_up_falling_left:
                bullet.xVel = 0
                bullet.yVel = -self.bulletSpeed
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.25)
                bullet.mTransform.yPos = self.player.mTransform.yPos
            case self.aim_up_idle_right:
                bullet.xVel = 0
                bullet.yVel = -self.bulletSpeed
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.45)
                bullet.mTransform.yPos = self.player.mTransform.yPos
            case self.aim_up_idle_left:
                bullet.xVel = 0
                bullet.yVel = -self.bulletSpeed
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.20)
                bullet.mTransform.yPos = self.player.mTransform.yPos
            case self.aim_up_run_right:
                bullet.xVel = 0
                bullet.yVel = -self.bulletSpeed
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.5)
                bullet.mTransform.yPos = self.player.mTransform.yPos
            case self.aim_up_run_left:
                bullet.xVel = 0
                bullet.yVel = -self.bulletSpeed
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.15)
                bullet.mTransform.yPos = self.player.mTransform.yPos
            case self.shooting_falling_right:
                bullet.xVel = self.bulletSpeed
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.75)
                bullet.mTransform.yPos = self.player.mTransform.yPos + int(sprite.getHeight() * 0.30)
            case self.shooting_falling_left:
                bullet.xVel = -self.bulletSpeed
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos
                bullet.mTransform.yPos = self.player.mTransform.yPos + int(sprite.getHeight() * 0.30)
            case self.shooting_run_right:
                bullet.xVel = self.bulletSpeed
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.75)
                bullet.mTransform.yPos = self.player.mTransform.yPos + int(sprite.getHeight() * 0.25)
            case self.shooting_run_left:
                bullet.xVel = -self.bulletSpeed
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos
                bullet.mTransform.yPos = self.player.mTransform.yPos + int(sprite.getHeight() * 0.25)
            case self.idle_right:
                bullet.xVel = self.bulletSpeed
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.75)
                bullet.mTransform.yPos = self.player.mTransform.yPos + int(sprite.getHeight() * 0.25)
            case self.idle_left:
                bullet.xVel = -self.bulletSpeed
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos
                bullet.mTransform.yPos = self.player.mTransform.yPos + int(sprite.getHeight() * 0.25)
            case _:
                bullet.xVel = 0
                bullet.yVel = 0
                bullet.mTransform.xPos = self.player.mTransform.xPos + int(sprite.getWidth() * 0.5)
                bullet.mTransform.yPos = self.player.mTransform.yPos
        return bullet
        

    def changeToFalling(self, inputs):
        if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
            self.playerState.setState("aimupfalling")
            if self.curXDirection > 0:
                self.player.addSpriteComponent(self.aim_up_falling_right)
                self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_right)]
            else:
                self.player.addSpriteComponent(self.aim_up_falling_left)
                self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_left)]
        else:
            self.playerState.setState("falling")
            if self.curXDirection > 0:
                if self.isShooting():
                    self.player.addSpriteComponent(self.shooting_falling_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.shooting_falling_right)]
                else:
                    self.player.addSpriteComponent(self.falling_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.falling_right)]
                    self.waitOneFrameForShot = True
            else:
                if self.isShooting():
                    self.player.addSpriteComponent(self.shooting_falling_left)
                    self.currrentMaxFrame = self.maxFrameDict[str(self.shooting_falling_left)]
                else:
                    self.player.addSpriteComponent(self.falling_left)
                    self.currentMaxFrame = self.maxFrameDict[str(self.falling_left)]
                    self.waitOneFrameForShot = True

    # Handles player jump logic
    def handlePlayerJump(self, inputs):
        self.decrementJumpTimer()
        currentState = self.playerState.getState()
        if currentState == "jumping" or currentState == "aimupjumping":
            wait = False
            if self.waitOneCycleToInitiateJump:
                wait = True
                self.waitOneCycleToInitiateJump = False

            if not self.playerJump.stillJumping() and not wait:
                # change to falling
                self.changeToFalling(inputs)
            elif inputs[engine.J_PRESSED] and self.jumpTimer <= 0:
                # continue jump
                self.playerJump.Update(self.player)
                if self.uprightJump:
                    if self.curXDirection > 0:
                        if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                            self.changePlayerSprite(self.aim_up_falling_right)
                        else:
                            if self.isShooting():
                                # fix multiple jumps
                                self.player.mTransform.xPos -= abs(self.player.mSprite.getWidth() - self.shooting_falling_right.getWidth())
                                self.changePlayerSprite(self.shooting_falling_right)
                            else:
                                self.changePlayerSprite(self.falling_right)
                                self.waitOneFrameForShot = True
                    else:
                        # go left
                        if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                            self.changePlayerSprite(self.aim_up_falling_left)
                        else:
                            if self.isShooting():
                                self.changePlayerSprite(self.shooting_falling_left)
                            else:
                                self.changePlayerSprite(self.falling_left)
                                self.waitOneFrameForShot = True
                else:
                    if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                        # change to uprightJump
                        self.uprightJump = True
                        if self.curXDirection > 0:
                            self.changePlayerSprite(self.aim_up_falling_right)
                        else:
                            self.changePlayerSprite(self.aim_up_falling_left)
                    elif self.isShooting():
                        self.uprightJump = True
                        if self.curXDirection > 0:
                            self.changePlayerSprite(self.shooting_falling_right)
                        else:
                            self.changePlayerSprite(self.shooting_falling_left)
                            self.waitOneFrameForShot = True

            else:
                # stop jump
                self.playerJump.EndJump()
                self.uprightJump = False
                self.playerState.setState("falling")
                self.changeToFalling(inputs)
        else:
            if inputs[engine.J_PRESSED] and currentState == "standing":
                if self.jumpTimer <= 0:
                    self.player.InitiateJump()
                    self.playerJumpSound.PlaySound()
                    self.waitOneCycleForJumpUpdate = True
                    self.waitOneCycleToInitiateJump = True
                    # if UP_PRESSED: should go to else statement(uprightJump)
                    if (inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]) and not (inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]):
                        self.uprightJump = False
                        self.playerState.setState("jumping")
                        self.shootingCounter = self.shootingCounterMax + 1
                        self.waitOneFrameForShot = True
                        if self.hasScrewAttack:
                            self.changePlayerSprite(self.screw_attack_right)
                        else:
                            self.changePlayerSprite(self.somersault_right)
                        self.currentFrame = 0
                    elif (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]) and not (inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]):
                        self.uprightJump = False
                        self.playerState.setState("jumping")
                        self.shootingCounter = self.shootingCounterMax + 1
                        self.waitOneFrameForShot = True
                        if self.hasScrewAttack:
                            self.changePlayerSprite(self.screw_attack_left)
                        else:
                            self.changePlayerSprite(self.somersault_left)
                        self.currentFrame = 0
                    else:
                        self.uprightJump = True
                        if self.curXDirection > 0:
                            if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                                self.playerState.setState("aimupjumping")
                                currentWidth = self.player.mSprite.getWidth()
                                self.changePlayerSprite(self.aim_up_falling_right)
                                collision = self.tilemap.isTouchingRightWall(self.player)
                                if collision.isColliding:
                                    self.playerTransform.xPos -= (self.aim_up_falling_right.getWidth() - currentWidth)
                            else:
                                self.playerState.setState("jumping")
                                currentWidth = self.player.mSprite.getWidth()
                                if self.isShooting():
                                    self.changePlayerSprite(self.shooting_falling_right)
                                    collision = self.tilemap.isTouchingRightWall(self.player)
                                    if collision.isColliding:
                                        self.playerTransform.xPos -= (self.shooting_falling_right.getWidth() - currentWidth)
                                else:
                                    self.changePlayerSprite(self.falling_right)
                                    self.waitOneFrameForShot = True
                                    collision = self.tilemap.isTouchingRightWall(self.player)
                                    if collision.isColliding:
                                        self.playerTransform.xPos -= (self.falling_right.getWidth() - currentWidth)

                        else:
                            if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
                                self.playerState.setState("aimupjumping")
                                self.changePlayerSprite(self.aim_up_falling_left)
                            else:
                                self.playerState.setState("jumping")
                                if self.isShooting():
                                    self.changePlayerSprite(self.shooting_falling_left)
                                else:
                                    self.changePlayerSprite(self.falling_left)
                                    self.waitOneFrameForShot = True

    def decrementJumpTimer(self):
        if self.jumpTimer > 0:
            self.jumpTimer -= 1

    # Handles duck and roll and standing back up: sprites are assigned in handlePlayerMove()
    def handleDuckAndRoll(self, inputs, collision):
        if self.playerState.getState() == "standing":
            if collision.isColliding and (inputs[engine.DOWN_PRESSED] or inputs[engine.S_PRESSED]) and not inputs[engine.J_PRESSED]:
                # begin duck
                self.playerState.setState("ducking")
        elif self.playerState.getState() == "ducking":
            self.playerState.setState("rolling")
            self.isFirstRollingFrame = True
        elif self.playerState.getState() == "rolling":
            if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED] or inputs[engine.J_PRESSED]:
                # check if rolling under an obstacle
                if self.tilemap.tileAtXY(self.playerTransform.xPos, self.playerTransform.yPos - self.player.mSprite.getHeight()) == -1 and \
                    self.tilemap.tileAtXY(self.playerTransform.xPos + self.player.mSprite.getWidth(), self.playerTransform.yPos - self.player.mSprite.getHeight()) == -1:
                    self.playerState.setState("abouttostand")
                    self.jumpTimer = self.jumpTimerMax
        elif self.playerState.getState() == "abouttostand":
            self.playerState.setState("standing")
            self.isFirstStandingFrame = True
        
    def handlePlayerBombing(self, inputs):
        if len(self.bombArr) > 0:
            self.countDownBetweenBombs -= 1
        # must be rolling, fire pressed, countDownBetweenBombs <= 0, numBombs <= 3
        if self.playerState.getState() == "rolling":
            if inputs[engine.H_PRESSED] or inputs[engine.K_PRESSED]:
                if len(self.bombArr) < 3:
                    if self.countDownBetweenBombs <= 0:
                        bomb = Bomb(self.tilemap, self.sdl)
                        xPos = int(self.player.mTransform.xPos + self.player.mSprite.getWidth()/2 - bomb.getBombWidth()/2)
                        yPos = int(self.player.mTransform.yPos + self.player.mSprite.getHeight() - bomb.getBombHeight())
                        bomb.setBombPosition(xPos, yPos)
                        self.bombArr.append(bomb)
                        self.countDownBetweenBombs = self.numFramesBetweenBombs
                        self.bombCreatedSound.PlaySound()

    # Handles player touching wall
    def handlePlayerWallCollision(self):
            if self.player.mTransform.xPos + self.player.mSprite.getWidth() > self.lvlWidth:
                self.animateRoomChangeToTheRight(self.tilemap, self.tilemapAdjacencyDict[str(self.tilemap)]["right1"])
            elif self.player.mTransform.xPos < 0:
                self.animateRoomChangeToTheLeft(self.tilemap, self.tilemapAdjacencyDict[str(self.tilemap)]["left1"])
            else:
                collision = self.tilemap.isTouchingRightWall(self.player)
                if collision.isColliding:
                    # hit right wall: set xPos to correct x according to row, col
                    self.player.mTransform.xPos = self.tileSize * collision.firstTileColumn - self.player.mSprite.getWidth() - 1 # minus one is necessary to stay off right wall
                collision = self.tilemap.isTouchingLeftWall(self.player)
                if collision.isColliding:
                    # hit left wall
                    self.player.mTransform.xPos = self.tileSize * (collision.firstTileColumn + 1)
        
            
    def handlePlayerFloorCollision(self, inputs):
        collision = engine.Collision()
        collision.isColliding = False
        currentState = self.playerState.getState()
        if self.waitOneCycleForJumpUpdate:
            self.waitOneCycleForJumpUpdate = False
            # This yPos change is necessary so that we don't get a left and right wall collision
            collision = self.tilemap.isOnGround(self.player)
            if collision.isColliding:
                self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.player.mSprite.getHeight() - 1
        elif self.player.yVel > 0:
            collision = self.tilemap.isOnGround(self.player)
            if collision.isColliding:
                # collision with ground
                if currentState == "falling" or currentState == "aimupfalling":
                    self.changeToStanding(collision, inputs)
                elif currentState == "jumping" or currentState == "aimupjumping":
                    # stop jump
                    self.playerJump.EndJump()
                    self.uprightJump = False
                    self.changeToStanding(collision, inputs)
                else:
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.player.mSprite.getHeight() - 1
            else:
                if currentState == "standing":
                    self.changeToFalling(inputs)
        return collision
    
    def changeToStanding(self, collision, inputs):
        self.playerState.setState("standing")
        # if up is pressed, keep sprite as aim-up-jumping but still change playerState to "standing"
        jumpAgain = False
        aimUp = False
        if inputs[engine.J_PRESSED] and self.jumpTimer <= 0:
            jumpAgain = True
        if inputs[engine.UP_PRESSED] or inputs[engine.W_PRESSED]:
            aimUp = True
        if inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
            if self.isShooting():
                if jumpAgain:
                    if aimUp:
                        self.player.addSpriteComponent(self.aim_up_falling_right)
                        self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_right)]
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.aim_up_falling_right.getHeight() - 1
                    else:
                        self.player.addSpriteComponent(self.shooting_falling_right)
                        self.currentMaxFrame = self.maxFrameDict[str(self.shooting_falling_right)]
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.shooting_falling_right.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.shooting_run_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.shooting_run_right)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.shooting_run_right.getHeight() - 1
            else:
                if jumpAgain:
                    if aimUp:
                        self.player.addSpriteComponent(self.aim_up_falling_right)
                        self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_right)]
                        self.waitOneFrameForShot = True
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.aim_up_falling_right.getHeight() - 1
                    else:
                        self.player.addSpriteComponent(self.falling_right)
                        self.currentMaxFrame = self.maxFrameDict[str(self.falling_right)]
                        self.waitOneFrameForShot = True
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.falling_right.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.run_right_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]
                    self.waitOneFrameForShot = True
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.run_right_sprite.getHeight() - 1
        elif inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]:
            if self.isShooting():
                if jumpAgain:
                    if aimUp:
                        self.player.addSpriteComponent(self.aim_up_falling_left)
                        self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_left)]
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.aim_up_falling_left.getHeight() - 1
                    else:
                        self.player.addSpriteComponent(self.shooting_falling_left)
                        self.currentMaxFrame = self.maxFrameDict[str(self.shooting_falling_left)]
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.shooting_falling_left.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.shooting_run_left)
                    self.currentMaxFrame = self.maxFrameDict[str(self.shooting_run_left)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.shooting_run_left.getHeight() - 1
            else:
                if jumpAgain:
                    if aimUp:
                        self.player.addSpriteComponent(self.aim_up_falling_left)
                        self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_left)]
                        self.waitOneFrameForShot = True
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.aim_up_falling_left.getHeight() - 1
                    else:
                        self.player.addSpriteComponent(self.falling_left)
                        self.currentMaxFrame = self.maxFrameDict[str(self.falling_left)]
                        self.waitOneFrameForShot = True
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.falling_left.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.run_left_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_left_sprite)]
                    self.waitOneFrameForShot = True
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.run_left_sprite.getHeight() - 1
        else:
            if self.curXDirection > 0:
                if jumpAgain:
                    if aimUp:
                        self.player.addSpriteComponent(self.aim_up_falling_right)
                        self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_right)]
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.aim_up_falling_right.getHeight() - 1
                    else:
                        if self.isShooting():
                            self.player.addSpriteComponent(self.shooting_falling_right)
                            self.currentMaxFrame = self.maxFrameDict[str(self.shooting_falling_right)]
                            self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.shooting_falling_right.getHeight() - 1
                        else:
                            self.player.addSpriteComponent(self.falling_right)
                            self.currentMaxFrame = self.maxFrameDict[str(self.falling_right)]
                            self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.falling_right.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.idle_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_right)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.idle_right.getHeight() - 1
            else:
                if jumpAgain:
                    if aimUp:
                        self.player.addSpriteComponent(self.aim_up_falling_left)
                        self.currentMaxFrame = self.maxFrameDict[str(self.aim_up_falling_left)]
                        self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.aim_up_falling_left.getHeight() - 1
                    else:
                        if self.isShooting():
                            self.player.addSpriteComponent(self.shooting_falling_left)
                            self.currentMaxFrame = self.maxFrameDict[str(self.shooting_falling_left)]
                            self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.shooting_falling_left.getHeight() - 1
                        else:
                            self.player.addSpriteComponent(self.falling_left)
                            self.currentMaxFrame = self.maxFrameDict[str(self.falling_left)]
                            self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.falling_left.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.idle_left)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_left)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.idle_left.getHeight() - 1


    def handlePlayerCeilingCollision(self, inputs):
        collision = engine.Collision()
        collision.isColliding = False
        if self.player.yVel <= 0:
            collision = self.tilemap.isOnCeiling(self.player)
            if collision.isColliding:
                # collision with ceiling
                self.playerTransform.yPos = self.tileSize * (collision.firstTileRow + 1)
                self.playerJump.EndJump()
                self.uprightJump = False
                self.changeToFalling(inputs)

    def handleDoorCollisionX(self):
        if str(self.tilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(self.tilemap)]:
                isColliding = bubbleDoor.checkIfColliding(self.player)
                if isColliding == True:
                    self.player.mTransform.xPos += bubbleDoor.getXDiff(self.player)
    
    def handleDoorCollisionY(self, inputs):
        if str(self.tilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(self.tilemap)]:
                isColliding = bubbleDoor.checkIfColliding(self.player)
                if isColliding == True:
                    yDiff = bubbleDoor.getYDiff(self.player)
                    self.player.mTransform.yPos += yDiff
                    if yDiff < 0:
                        # end jump, change to standing
                        if self.playerState.getState() == "jumping" or self.playerState.getState() == "falling":
                            self.player.mJumpComponent.EndJump()
                            self.uprightJump = False
                            self.playerState.setState("standing")
                            if inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
                                curHeight = self.player.mSprite.getHeight()
                                if self.isShooting():
                                    self.player.addSpriteComponent(self.shooting_run_right)
                                    self.player.mTransform.yPos -= (self.shooting_run_right.getHeight() - curHeight)
                                else:
                                    self.player.addSpriteComponent(self.run_right_sprite)
                                    self.player.mTransform.yPos -= (self.run_right_sprite.getHeight() - curHeight)
                            elif inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]:
                                curHeight = self.player.mSprite.getHeight()
                                if self.isShooting():
                                    self.player.addSpriteComponent(self.shooting_run_left)
                                    self.player.mTransform.yPos -= (self.shooting_run_left.getHeight() - curHeight)
                                else:
                                    self.player.addSpriteComponent(self.run_left_sprite)
                                    self.player.mTransform.yPos -= (self.run_left_sprite.getHeight() - curHeight)
                            else:
                                if self.curXDirection > 0:
                                    curHeight = self.player.mSprite.getHeight()
                                    self.player.addSpriteComponent(self.idle_right)
                                    self.player.mTransform.yPos -= (self.idle_right.getHeight() - curHeight)
                                else:
                                    curHeight = self.player.mSprite.getHeight()
                                    self.player.addSpriteComponent(self.idle_left)
                                    self.player.mTransform.yPos -= (self.idle_left.getHeight() - curHeight)
                    return
    
    def handleEnemyCollision(self, inputs):
        if self.playerCannotBeHit == True:
            self.playerCannotBeHitTimer += 1
            if self.playerCannotBeHitTimer > self.playerCannotBeHitMax:
                self.playerCannotBeHitTimer = 0
                self.playerCannotBeHit = False
            if self.playerIsHit == True:
                self.hitTimer += 1
            if self.hitTimer > self.maxHitTimer:
                self.hitTimer = 0
                self.playerIsHit = False
                self.backupLeft = False
                self.backupRight = False
            if self.backupLeft:
                if (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]) and not (inputs[engine.RIGHT_PRESSED or inputs[engine.D_PRESSED]]):
                    self.player.mTransform.xPos -= self.backupXDiff
                elif (inputs[engine.RIGHT_PRESSED or inputs[engine.D_PRESSED]]) and not (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]):
                    self.player.mTransform.xPos -= self.playerRunSpeed + self.backupXDiff
                else:
                    self.player.mTransform.xPos -= self.backupXDiff
            elif self.backupRight:
                if (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]) and not (inputs[engine.RIGHT_PRESSED or inputs[engine.D_PRESSED]]):
                    self.player.mTransform.xPos += self.playerRunSpeed + self.backupXDiff
                elif (inputs[engine.RIGHT_PRESSED or inputs[engine.D_PRESSED]]) and not (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]):
                    self.player.mTransform.xPos += self.backupXDiff
                else:
                    self.player.mTransform.xPos += self.backupXDiff
        else:
            # for all other states, handle x change the same way
            if str(self.tilemap) in self.enemiesDict:
                if "bugArray" in self.enemiesDict[str(self.tilemap)]:
                    for bug in self.enemiesDict[str(self.tilemap)]["bugArray"]:
                        if bug.isActive():
                            isColliding = bug.checkIfColliding(self.player)
                            if isColliding:
                                if self.player.mSprite == self.screw_attack_left or self.player.mSprite == self.screw_attack_right:
                                    bug.decreaseHitPoints(100)
                                else:
                                    self.player.mJumpComponent.EndJump()
                                    self.uprightJump = False
                                    self.playerIsHit = True
                                    self.playerCannotBeHit = True
                                    self.playerHitSound.PlaySound()
                                    if bug.getCurrentXDirection() > 0:
                                        self.backupRight = True
                                    else:
                                        self.backupLeft = True
                if "zoomerArray" in self.enemiesDict[str(self.tilemap)]:
                    for zoomer in self.enemiesDict[str(self.tilemap)]["zoomerArray"]:
                        if zoomer.isActive():
                            isColliding = zoomer.checkIfColliding(self.player)
                            if isColliding:
                                if self.player.mSprite == self.screw_attack_left or self.player.mSprite == self.screw_attack_right:
                                    zoomer.decreaseHitPoints(100)
                                else:
                                    self.player.mJumpComponent.EndJump()
                                    self.uprightJump = False
                                    self.playerIsHit = True
                                    self.playerCannotBeHit = True
                                    self.playerHitSound.PlaySound()
                                    if self.curXDirection > 0:
                                        self.backupLeft = True
                                    else:
                                        self.backupRight = True

    def handlePowerUpCollision(self):
        def checkIfColliding(powerUpObj, playerObj):
            x1 = powerUpObj.mTransform.xPos
            y1 = powerUpObj.mTransform.yPos
            width1 = powerUpObj.mSprite.getWidth()
            height1 = powerUpObj.mSprite.getHeight()
            x2 = playerObj.mTransform.xPos
            y2 = playerObj.mTransform.yPos
            width2 = playerObj.mSprite.getWidth()
            height2 = playerObj.mSprite.getHeight()
            if (x1 < x2 + width2 and x1 + width1 > x2 and
                    y1 < y2 + height2 and y1 + height1 > y2):
                return True
            return False
        if str(self.tilemap) in self.powerUpDict:
            if self.powerUpActiveDict[str(self.tilemap)]:
                if checkIfColliding(self.powerUpDict[str(self.tilemap)], self.player):
                    self.hasScrewAttack = True
                    self.powerUpActiveDict[str(self.tilemap)] = False
                    self.powerUpSound.PlaySound()

    def handlePlayerExplodingTileCollisionX(self):
        if str(self.tilemap) in self.explodableTilesDict:
            for tile in self.explodableTilesDict[str(self.tilemap)]:
                if tile.isActive():
                    if tile.checkIfColliding(self.player):
                        tileObject = tile.getTileObject()
                        if self.curXDirection > 0:
                            self.player.mTransform.xPos = tileObject.mTransform.xPos - self.player.mSprite.getWidth() - 1
                        else:
                            self.player.mTransform.xPos = tileObject.mTransform.xPos + tileObject.mSprite.getWidth() + 1


                    
    # Handles all player associated updates
    def playerUpdate(self, inputs):
        # Player left and right movement
        self.handlePlayerMove(inputs)
        # Physics update on player xPos
        self.physics.UpdateX(self.player)
        self.handleEnemyCollision(inputs)
        self.handlePowerUpCollision()
        self.handlePlayerWallCollision()
        self.handleDoorCollisionX()
        self.handlePlayerExplodingTileCollisionX()
        self.handlePlayerJump(inputs)

        # Physics update on player yPos
        self.physics.UpdateY(self.player)
        collisionFloor = self.handlePlayerFloorCollision(inputs)
        self.handleDoorCollisionY(inputs)
        self.handlePlayerCeilingCollision(inputs)
        self.handleDuckAndRoll(inputs, collisionFloor)
        self.handlePlayerBombing(inputs)
        self.handlePlayerShooting(inputs)
        
        # update frame
        if self.currentFrame > self.currentMaxFrame:
            self.currentFrame = 0
        
        if self.frameUpdateDelay > self.maxFrameUpdateDelay:
            self.frameUpdateDelay = 0
            if self.currentFrame > self.currentMaxFrame:
                self.currentFrame = 0
            else:
                self.currentFrame += 1
        else:
            self.frameUpdateDelay += 1
        self.player.mSprite.update(0, 0, self.currentFrame)
        # increment shootingCounter
        if self.shootingCounter <= self.shootingCounterMax:
            self.shootingCounter += 1
        else:
            self.waitOneFrameForShot = True

    def bulletsUpdate(self):
        keysArr = []
        for key in self.bulletDict.keys():
            bullet = self.bulletDict[key][0]
            bullet.mPhysicsComponent.UpdateX(bullet)
            collision1 = engine.Collision()
            collision1.isColliding = False
            if bullet.xVel > 0:
                collision1 = self.tilemap.isTouchingRightWall(bullet)
            elif bullet.xVel < 0:
                collision1 = self.tilemap.isTouchingLeftWall(bullet)
            bullet.mPhysicsComponent.UpdateY(bullet)
            collision2 = engine.Collision()
            collision2.isColliding = False
            if bullet.yVel < 0:
                collision2 = self.tilemap.isOnCeiling(bullet)
            self.bulletDict[key][1] += 1
            bullet.mSprite.update(0, 0, 0)
            if collision1.isColliding or collision2.isColliding or self.bulletDict[key][1] > self.shotLifeMax:
                keysArr.append(key)
        for key in keysArr:
            del self.bulletDict[key]
            del self.spriteDict[key]
            del self.transformDict[key]
            del self.physicsDict[key]

    def bombsUpdate(self):
        numBombsToDestroy = 0
        for bomb in self.bombArr:
            bomb.incrementCurrentFrameCount()
            bomb.decrementCountDown()
            bomb.getBombObject().mSprite.update(0, 0, int(bomb.getCurrentFrameCount()))
            if bomb.isTimeToDestroy():
                numBombsToDestroy += 1
        for i in range(numBombsToDestroy):
            self.bombArr.pop(0)
        if len(self.bombArr) == 0:
            self.countDownBetweenBombs = 0


    def doorObjectsUpdate(self, tilemap):
        if str(tilemap) in self.doorObjectsDict.keys():
            for doorObject in self.doorObjectsDict[str(tilemap)]:
                doorObject.mSprite.update(0, 0, 0)
    
    def bubbleDoorsUpdate(self, tilemap):
        if str(tilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(tilemap)]:
                bubbleDoor.getSpriteComponent().update(0, 0, int(bubbleDoor.getFrameCount()))
                # update frame count for bubbleDoor
                bubbleDoor.advanceTimer()

    def enemiesUpdate(self, tilemap):
        if str(tilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(tilemap)]:
                for bug in self.enemiesDict[str(tilemap)]["bugArray"]:
                    self.handleBugUpdate(bug, tilemap, False)
            if "zoomerArray" in self.enemiesDict[str(tilemap)]:
                for zoomer in self.enemiesDict[str(tilemap)]["zoomerArray"]:
                    self.handleZoomerUpdate(zoomer, tilemap, False)

    def getPowerUpFrameCount(self, tilemap):
        res = 0
        if str(tilemap) in self.powerUpFrameCountDict:
            self.powerUpFrameCountDict[str(tilemap)] += 1
            if self.powerUpFrameCountDict[str(tilemap)] > 1:
                self.powerUpFrameCountDict[str(tilemap)] = 0
            res = self.powerUpFrameCountDict[str(tilemap)]
        return res

    def powerUpUpdate(self, tilemap):
        if str(tilemap) in self.powerUpDict and str(tilemap) in self.powerUpActiveDict:
            if self.powerUpActiveDict[str(tilemap)]:
                self.powerUpDict[str(tilemap)].mSprite.update(0, 0, self.getPowerUpFrameCount(tilemap))

    
    def handleBugUpdate(self, bug, tilemap, isAnimating):
        if bug.isActive():
            bugObject = bug.getBugObject()
            # check if off screen
            if (self.player.mTransform.xPos >= bug.originalXPos + self.windowWidth or self.player.mTransform.xPos <= bug.originalXPos - self.windowWidth)\
                and (self.player.mTransform.xPos >= bugObject.mTransform.xPos + self.windowWidth\
                or self.player.mTransform.xPos <= bugObject.mTransform.xPos - self.windowWidth) and not isAnimating:
                bug.setActiveStatus(True)
                return
            # update sprite
            bugObject.mSprite.update(0, 0, int(bug.getCurrentFrameCount()))
            bugObject.mJumpComponent.Update(bugObject)
            if bugObject.mJumpComponent.stillJumping():
                # continue jump
                bugObject.mTransform.xPos += (bug.getCurrentXDirection() * int(bugObject.mJumpComponent.xVelocity))
                self.checkBugForWallCollision(bug, tilemap)
                bugObject.mPhysicsComponent.UpdateY(bugObject)
                self.checkBugForFloorAndCeilingCollision(bug, tilemap)
                oneThirdHeight = bug.jumpHeight // 3
                if bugObject.mTransform.yPos < bug.originalYPos + oneThirdHeight:
                    bug.setCurrentSprite(0)
                    bug.incrementCurrentFrameCount(self.bugFrameIncrement, bug.getMaxFrameCount(0))
                elif bugObject.mTransform.yPos < bug.originalYPos + 2 * oneThirdHeight:
                    bug.setCurrentSprite(1)
                    bug.incrementCurrentFrameCount(self.bugFrameIncrement, bug.getMaxFrameCount(1))
                else:
                    bug.setCurrentSprite(2)
                    bug.incrementCurrentFrameCount(self.bugFrameIncrement, bug.getMaxFrameCount(2))
            else:
                bug.incrementCurrentFrameCount(self.bugFrameIncrement, bug.getMaxFrameCount(0))
                if bugObject.mTransform.yPos > bug.getOriginalYPos():
                    bugObject.mTransform.xPos += (bug.getCurrentXDirection() * int(bugObject.mJumpComponent.xVelocity))
                self.checkBugForWallCollision(bug, tilemap)
                bugObject.mPhysicsComponent.UpdateY(bugObject)
                ceilingCollision = tilemap.isOnCeiling(bugObject)
                if ceilingCollision.isColliding:
                    self.handleBugCeilingCollision(bug, bugObject, ceilingCollision)
                    # initiate jump
                    if bugObject.mTransform.xPos - bug.getCloseness() <= self.player.mTransform.xPos <= bugObject.mTransform.xPos:
                        bug.setCurrentXDirection(-1)
                        bug.waitOneCycleForJumpUpdate = True
                        bugObject.InitiateJump()
                    elif bugObject.mTransform.xPos <= self.player.mTransform.xPos <= bugObject.mTransform.xPos + bug.getCloseness():
                        bug.setCurrentXDirection(1)
                        bug.waitOneCycleForJumpUpdate = True
                        bugObject.InitiateJump()
                else:
                    # fall upward
                    bugObject.yVel = -4
                    bugObject.mPhysicsComponent.UpdateY(bugObject)
                    ceilingCollision = tilemap.isOnCeiling(bugObject)
                    if ceilingCollision.isColliding:
                        bugObject.mTransform.yPos = self.tileSize * (ceilingCollision.firstTileRow + 1)
            # self.checkBugForWallAndFloorCollision(bug, tilemap)
        else:
            # bug is inActive: reactivate if far enough away from player
            if self.player.mTransform.xPos >= bug.originalXPos + self.windowWidth or self.player.mTransform.xPos <= bug.originalXPos - self.windowWidth:
                bug.setActiveStatus(True)

    def checkBugForWallCollision(self, bug, tilemap):
        lvlWidth = tilemap.getCols() * self.tileSize
        bugObject = bug.getBugObject()
        rightWallCollision = tilemap.isTouchingRightWall(bugObject)
        if rightWallCollision.isColliding:
            bugObject.mTransform.xPos = self.tileSize * rightWallCollision.firstTileColumn - bugObject.mSprite.getWidth() - 1
        leftWallCollision = tilemap.isTouchingLeftWall(bugObject)
        if leftWallCollision.isColliding:
            bugObject.mTransform.xPos = self.tileSize * (leftWallCollision.firstTileColumn + 1)
        # check if going through door
        if bugObject.mTransform.xPos < 0:
            bugObject.mTransform.xPos = 0
            bug.curXDirection *= -1
        elif bugObject.mTransform.xPos + bugObject.mSprite.getWidth() >= lvlWidth:
            bugObject.mTransform.xPos = lvlWidth - bugObject.mSprite.getWidth()
            bug.curXDirection *= -1

    def checkBugForFloorAndCeilingCollision(self, bug, tilemap):
        bugObject = bug.getBugObject()
        floorCollision = tilemap.isOnGround(bugObject)
        if floorCollision.isColliding:
            bugObject.mTransform.yPos = self.tileSize * (floorCollision.firstTileRow) - bugObject.mSprite.getHeight() - 1
            bugObject.mJumpComponent.EndJump()
        else:
            ceilingCollision = tilemap.isOnGround(bugObject)
            if ceilingCollision.isColliding:
                bugObject.mTransform.yPos = self.tileSize * (ceilingCollision.firstTileRow + 1) + 1

    def handleBugCeilingCollision(self, bugClass, bugObject, collision):
        bugObject.mTransform.yPos = self.tileSize * (collision.firstTileRow + 1)
        if bugClass.waitOneCycleForJumpUpdate == True:
            bugClass.waitOneCycleForJumpUpdate = False
        else:
            bugObject.mJumpComponent.EndJump()

    def handleZoomerUpdate(self, zoomer, tilemap, isAnimating):
        if zoomer.isActive():
            zoomerObject = zoomer.getZoomerObject()
            # update sprite
            curOrientation = zoomer.getCurrentOrientation()
            zoomer.incrementCurrentFrameCount(self.zoomerFrameIncrement, zoomer.getMaxFrameCount(curOrientation))
            zoomerObject.mSprite.update(0, 0, int(zoomer.getCurrentFrameCount()))
            if zoomerObject.mTransform.xPos <= 0:
                zoomer.reverseClockwiseDirection()
                zoomerObject.mTransform.xPos = 1
                zoomerObject.xVel = zoomer.getCurrentXVelocity()
            elif zoomerObject.mTransform.xPos + zoomerObject.mSprite.getWidth() >= (tilemap.getCols() + 1) * self.tileSize:
                zoomer.reverseClockwiseDirection()
                zoomerObject.mTransform.xPos = (tilemap.getCols() + 1) * self.tileSize - zoomerObject.mSprite.getWidth() - 1
                zoomerObject.xVel = zoomer.getCurrentXVelocity()
            self.updateZoomer(zoomer, tilemap, curOrientation, zoomer.isGoingClockwise())
        else:
            # check if zoomer is offscreen: re-activate
            if (zoomer.getOriginalYPos() > self.player.mTransform.yPos + self.windowHeight or
                zoomer.getOriginalYPos() < self.player.mTransform.yPos - self.windowHeight or
                zoomer.getOriginalXPos() > self.player.mTransform.xPos + self.windowWidth or
                zoomer.getOriginalXPos() < self.player.mTransform.xPos - self.windowWidth) and isAnimating == False:
                zoomer.setActiveStatus(True)

    def updateZoomer(self, zoomer, tilemap, curOrientation, isClockwise):
        zoomerObject = zoomer.getZoomerObject()
        match curOrientation:
            case 0:
                tempY = zoomerObject.mTransform.yPos
                zoomerObject.mPhysicsComponent.UpdateY(zoomerObject)
                floorCollision = tilemap.isOnGround(zoomerObject)
                if floorCollision.isColliding:
                    zoomerObject.mTransform.yPos = self.tileSize * (floorCollision.firstTileRow) - zoomerObject.mSprite.getHeight() - 1
                else:
                    zoomerObject.mTransform.yPos = tempY
                zoomerObject.mPhysicsComponent.UpdateX(zoomerObject)
                if isClockwise:
                    rightCollision = tilemap.isTouchingRightWall(zoomerObject)
                    if rightCollision.isColliding:
                        zoomer.setCurrentSprite(3)
                        zoomer.decrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.xPos = self.tileSize * rightCollision.firstTileColumn - zoomerObject.mSprite.getWidth() - 1
                    else:
                        if floorCollision.isColliding:
                            if tilemap.tileAt(floorCollision.firstTileRow, floorCollision.firstTileColumn + 1) == -1:
                                if zoomerObject.mTransform.xPos + zoomerObject.mSprite.getWidth() + 2 > (floorCollision.firstTileColumn + 1) * self.tileSize + zoomerObject.mSprite.getHeight():
                                    zoomer.setCurrentSprite(1)
                                    zoomer.incrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.xPos = self.tileSize * (floorCollision.firstTileColumn + 1) + 1
                else:
                    leftCollision = tilemap.isTouchingLeftWall(zoomerObject)
                    if leftCollision.isColliding:
                        zoomer.setCurrentSprite(1)
                        zoomer.incrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.xPos = self.tileSize * (leftCollision.firstTileColumn + 1)
                    else:
                        if floorCollision.isColliding:
                            if tilemap.tileAt(floorCollision.firstTileRow, floorCollision.firstTileColumn - 1) == -1:
                                if zoomerObject.mTransform.xPos < floorCollision.firstTileColumn * self.tileSize - zoomerObject.mSprite.getHeight() + 1:
                                    zoomer.setCurrentSprite(3)
                                    zoomer.decrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.xPos = self.tileSize * floorCollision.firstTileColumn - zoomerObject.mSprite.getWidth() - 1
            case 1:
                tempX = zoomerObject.mTransform.xPos
                zoomerObject.mPhysicsComponent.UpdateX(zoomerObject)
                leftWallCollision = tilemap.isTouchingLeftWall(zoomerObject)
                if leftWallCollision.isColliding:
                    zoomerObject.mTransform.xPos = self.tileSize * (leftWallCollision.firstTileColumn + 1) + 1
                else:
                    zoomerObject.mTransform.xPos = tempX
                zoomerObject.mPhysicsComponent.UpdateY(zoomerObject)
                if isClockwise:
                    floorCollision = tilemap.isOnGround(zoomerObject)
                    if floorCollision.isColliding:
                        zoomer.setCurrentSprite(0)
                        zoomer.decrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.yPos = floorCollision.firstTileRow * self.tileSize - zoomerObject.mSprite.getHeight() - 1
                    else:
                        if leftWallCollision.isColliding:
                            if tilemap.tileAt(leftWallCollision.firstTileRow + 1, leftWallCollision.firstTileColumn) == -1:
                                if zoomerObject.mTransform.yPos + zoomerObject.mSprite.getHeight() > (leftWallCollision.firstTileRow + 1) * self.tileSize + zoomerObject.mSprite.getWidth() - 9:
                                    tempY = zoomerObject.mTransform.yPos
                                    zoomer.setCurrentSprite(2)
                                    zoomer.incrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.yPos = self.tileSize * (leftWallCollision.firstTileRow + 1) + 1
                else:
                    ceilingCollision = tilemap.isOnCeiling(zoomerObject)
                    if ceilingCollision.isColliding:
                        zoomer.setCurrentSprite(2)
                        zoomer.incrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.yPos = self.tileSize * (ceilingCollision.firstTileRow + 1)
                    else:
                        if leftWallCollision.isColliding:
                            if tilemap.tileAt(leftWallCollision.firstTileRow - 1, leftWallCollision.firstTileColumn) == -1:
                                if zoomerObject.mTransform.yPos < (leftWallCollision.firstTileRow) * self.tileSize - zoomerObject.mSprite.getWidth() + 9:
                                    zoomer.setCurrentSprite(0)
                                    zoomer.decrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.yPos = self.tileSize * leftWallCollision.firstTileRow - zoomerObject.mSprite.getHeight() - 1
            case 2:
                tempY = zoomerObject.mTransform.yPos
                zoomerObject.mPhysicsComponent.UpdateY(zoomerObject)
                ceilingCollision = tilemap.isOnCeiling(zoomerObject)
                if ceilingCollision.isColliding:
                    zoomerObject.mTransform.yPos = self.tileSize * (ceilingCollision.firstTileRow + 1)
                else:
                    zoomerObject.mTransform.yPos = tempY
                zoomerObject.mPhysicsComponent.UpdateX(zoomerObject)
                if isClockwise:
                    leftCollision = tilemap.isTouchingLeftWall(zoomerObject)
                    if leftCollision.isColliding:
                        zoomer.setCurrentSprite(1)
                        zoomer.decrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.xPos = self.tileSize * (leftCollision.firstTileColumn + 1) + 1
                    else:
                        if ceilingCollision.isColliding:
                            if tilemap.tileAt(ceilingCollision.firstTileRow, ceilingCollision.firstTileColumn - 1) == -1:
                                if zoomerObject.mTransform.xPos < (ceilingCollision.firstTileColumn) * self.tileSize - zoomerObject.mSprite.getHeight() + 9:
                                    zoomer.setCurrentSprite(3)
                                    zoomer.incrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.xPos = self.tileSize * (ceilingCollision.firstTileColumn) - zoomerObject.mSprite.getWidth() - 1
                else:
                    rightCollision = tilemap.isTouchingRightWall(zoomerObject)
                    if rightCollision.isColliding:
                        zoomer.setCurrentSprite(3)
                        zoomer.incrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.xPos = self.tileSize * (rightCollision.firstTileColumn) - zoomerObject.mSprite.getWidth() - 1
                    else:
                        if ceilingCollision.isColliding:
                            if tilemap.tileAt(ceilingCollision.firstTileRow, ceilingCollision.firstTileColumn + 1) == -1:
                                if zoomerObject.mTransform.xPos + zoomerObject.mSprite.getWidth() > ceilingCollision.firstTileColumn * self.tileSize + zoomerObject.mSprite.getHeight() - 9:
                                    zoomer.setCurrentSprite(1)
                                    zoomer.decrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.xPos = self.tileSize * (ceilingCollision.firstTileColumn + 1) + 1
            case 3:
                tempX = zoomerObject.mTransform.xPos
                zoomerObject.mPhysicsComponent.UpdateX(zoomerObject)
                rightWallCollision = tilemap.isTouchingRightWall(zoomerObject)
                if rightWallCollision.isColliding:
                    zoomerObject.mTransform.xPos = self.tileSize * (rightWallCollision.firstTileColumn) - zoomerObject.mSprite.getWidth() - 1
                else:
                    zoomerObject.mTransform.xPos = tempX
                zoomerObject.mPhysicsComponent.UpdateY(zoomerObject)
                if isClockwise:
                    ceilingCollision = tilemap.isOnCeiling(zoomerObject)
                    if ceilingCollision.isColliding:
                        zoomer.setCurrentSprite(2)
                        zoomer.decrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.yPos = (ceilingCollision.firstTileRow + 1) * self.tileSize + 1
                    else:
                        if rightWallCollision.isColliding:
                            if tilemap.tileAt(rightWallCollision.firstTileRow - 1, rightWallCollision.firstTileColumn) == -1:
                                if zoomerObject.mTransform.yPos < (rightWallCollision.firstTileRow) * self.tileSize - zoomerObject.mSprite.getWidth() + 9:
                                    zoomer.setCurrentSprite(0)
                                    zoomer.incrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.yPos = self.tileSize * (rightWallCollision.firstTileRow) - zoomerObject.mSprite.getHeight()
                else:
                    floorCollision = tilemap.isOnGround(zoomerObject)
                    if floorCollision.isColliding:
                        zoomer.setCurrentSprite(0)
                        zoomer.incrementOrientation()
                        zoomerObject.yVel = zoomer.getCurrentYVelocity()
                        zoomerObject.xVel = zoomer.getCurrentXVelocity()
                        zoomerObject.mTransform.yPos = self.tileSize * (floorCollision.firstTileRow) - zoomerObject.mSprite.getHeight() - 1
                    else:
                        if rightWallCollision.isColliding:
                            if tilemap.tileAt(rightWallCollision.firstTileRow + 1, rightWallCollision.firstTileColumn) == -1:
                                if zoomerObject.mTransform.yPos + zoomerObject.mSprite.getHeight() > (rightWallCollision.firstTileRow + 1) * self.tileSize + zoomerObject.mSprite.getWidth() - 20:
                                    zoomer.setCurrentSprite(2)
                                    zoomer.decrementOrientation()
                                    zoomerObject.yVel = zoomer.getCurrentYVelocity()
                                    zoomerObject.xVel = zoomer.getCurrentXVelocity()
                                    zoomerObject.mTransform.yPos = self.tileSize * (rightWallCollision.firstTileRow + 1) + 1

    def bulletDoorCollisionUpdate(self):
        destroyKey = None
        if str(self.tilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(self.tilemap)]:
                for key in self.bulletDict.keys():
                    bullet = self.bulletDict[key][0]
                    isColliding = bubbleDoor.checkIfColliding(bullet)
                    if isColliding:
                        destroyKey = key
                        # begin opening door
                        bubbleDoor.openDoor()
                        self.doorPoppingSound.PlaySound()
                        break
        if destroyKey != None:
            del self.bulletDict[key]
            del self.spriteDict[key]
            del self.transformDict[key]
            del self.physicsDict[key]

    def handleDoorClosingUpdate(self):
        playSound = False
        if str(self.tilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(self.tilemap)]:
                if bubbleDoor.isClosed() == False and not (bubbleDoor.isClosing() or bubbleDoor.isOpening()):
                    if bubbleDoor.isFacingLeft():
                        if (self.player.mTransform.xPos + self.player.mSprite.getWidth() <= bubbleDoor.getXPos() or
                            self.player.mTransform.yPos + self.player.mSprite.getHeight() <= bubbleDoor.getYPos()) and bubbleDoor.isPauseTimerUp():
                            bubbleDoor.closeDoor()
                            playSound = True
                    else:
                        if (self.player.mTransform.xPos >= bubbleDoor.getXPos() + bubbleDoor.getWidth() or
                            self.player.mTransform.yPos + self.player.mSprite.getHeight() <= bubbleDoor.getYPos()) and bubbleDoor.isPauseTimerUp():
                            bubbleDoor.closeDoor()
                            playSound = True
        if playSound:
            self.doorInflatingSound.PlaySound()

    def bulletEnemiesCollisionUpdate(self):
        destroyArr = []
        for key in self.bulletDict.keys():
            bullet = self.bulletDict[key][0]
            if str(self.tilemap) in self.enemiesDict:
                if "bugArray" in self.enemiesDict[str(self.tilemap)]:
                    for bug in self.enemiesDict[str(self.tilemap)]["bugArray"]:
                        if bug.isActive():
                            isColliding = bug.checkIfColliding(bullet)
                            if isColliding:
                                if key not in destroyArr:
                                    destroyArr.append(key)
                                    bug.decreaseHitPoints(1)
                if "zoomerArray" in self.enemiesDict[str(self.tilemap)]:
                    for zoomer in self.enemiesDict[str(self.tilemap)]["zoomerArray"]:
                        if zoomer.isActive():
                            isColliding = zoomer.checkIfColliding(bullet)
                            if isColliding:
                                if key not in destroyArr:
                                    destroyArr.append(key)
                                    zoomer.decreaseHitPoints(1)
        for key in destroyArr:
            del self.bulletDict[key]
            del self.spriteDict[key]
            del self.transformDict[key]
            del self.physicsDict[key]

    def bombEnemiesCollisionUpdate(self):
        for bomb in self.bombArr:
            bombObject = bomb.getBombObject()
            if str(self.tilemap) in self.enemiesDict:
                if "bugArray" in self.enemiesDict[str(self.tilemap)]:
                    for bug in self.enemiesDict[str(self.tilemap)]["bugArray"]:
                        if bug.isActive():
                            if bomb.isExploding():
                                if str(bug) not in bomb.getEnemyArr():
                                    isColliding = bug.checkIfColliding(bombObject)
                                    if isColliding:
                                        bug.decreaseHitPoints(2)
                                        bomb.addEnemyToHitArray(str(bug))
                if "zoomerArray" in self.enemiesDict[str(self.tilemap)]:
                    for zoomer in self.enemiesDict[str(self.tilemap)]["zoomerArray"]:
                        if zoomer.isActive():
                            if bomb.isExploding():
                                if str(zoomer) not in bomb.getEnemyArr():
                                    isColliding = zoomer.checkIfColliding(bombObject)
                                    if isColliding:
                                        zoomer.decreaseHitPoints(2)
                                        bomb.addEnemyToHitArray(str(zoomer))

    def bombExplodableTilesUpdate(self):
        if str(self.tilemap) in self.explodableTilesDict:
            for tile in self.explodableTilesDict[str(self.tilemap)]:
                if tile.isActive():
                    for bomb in self.bombArr:
                        if bomb.isExploding():
                            bombObject = bomb.getBombObject()
                            if tile.checkIfColliding(bombObject):
                                tile.explodeTile()
                else:
                    tile.decrementCountDown(self.player)
                                
    
    # Update
    def Update(self, inputs):
        # Quit check
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
        self.bubbleDoorsUpdate(self.tilemap)
        self.enemiesUpdate(self.tilemap)
        self.powerUpUpdate(self.tilemap)
        self.playerUpdate(inputs)
        self.bulletsUpdate()
        self.bombsUpdate()
        self.handleDoorClosingUpdate()
        self.bulletDoorCollisionUpdate()
        self.bulletEnemiesCollisionUpdate()
        self.bombEnemiesCollisionUpdate()
        self.bombExplodableTilesUpdate()
        self.doorObjectsUpdate(self.tilemap)
        # update camera
        self.camera.Update()
    
    def renderDoorObjects(self, tilemap):
        if str(tilemap) in self.doorObjectsDict.keys():
            for doorObject in self.doorObjectsDict[str(tilemap)]:
                doorObject.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
    
    def renderBubbleDoors(self, tilemap):
        if str(tilemap) in self.bubbleDoorDict:
            for bubbleDoor in self.bubbleDoorDict[str(tilemap)]:
                if bubbleDoor.isClosed() or bubbleDoor.isOpening() or bubbleDoor.isClosing():
                    bubbleDoor.getSpriteComponent().render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)

    def renderEnemies(self, tilemap):
        if str(tilemap) in self.enemiesDict:
            if "bugArray" in self.enemiesDict[str(tilemap)]:
                for bug in self.enemiesDict[str(tilemap)]["bugArray"]:
                    if bug.isActive():
                        bug.getBugObject().mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
            if "zoomerArray" in self.enemiesDict[str(tilemap)]:
                for zoomer in self.enemiesDict[str(tilemap)]["zoomerArray"]:
                    if zoomer.isActive():
                        zoomer.getZoomerObject().mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)

    def renderBombs(self):
        for bomb in self.bombArr:
            bomb.getBombObject().mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)

    def renderPowerUp(self, tilemap):
        if str(tilemap) in self.powerUpDict and str(tilemap) in self.powerUpActiveDict:
            if self.powerUpActiveDict[str(tilemap)]:
                powerUpObject = self.powerUpDict.get(str(tilemap))
                powerUpObject.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)

    def renderExplodableTiles(self, tilemap):
        if str(tilemap) in self.explodableTilesDict:
            for tile in self.explodableTilesDict[str(tilemap)]:
                tileObject = tile.getTileObject()
                if tile.isActive():
                    tileObject.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)

    # Render
    def Render(self):
        #self.sdl.clear(60, 60, 60, 255) # TODO: Set background to black
        self.sdl.clear(0, 0, 0, 0) # This is code for black background
        self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.renderBubbleDoors(self.tilemap)
        self.renderEnemies(self.tilemap)
        self.player.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        for key in self.bulletDict.keys():
            self.bulletDict[key][0].mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.renderDoorObjects(self.tilemap)
        self.renderBombs()
        self.renderPowerUp(self.tilemap)
        self.renderExplodableTiles(self.tilemap)
        self.sdl.flip()

    # Starts or re-starts the game
    def StartGame(self):
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerFallingSpeed

    # Delay game loop to reach target fps
    def limitFPS(self):
        frameTicks = self.sdl.getTimeMS() - self.frameStartTime
        if frameTicks < self.maxTicksPerFrame:
            self.sdl.delay(self.maxTicksPerFrame - frameTicks)
        # self.frame_count += 1
        # timeElapsed = self.sdl.getTimeMS() - self.startTime
        # fps = self.frame_count / (timeElapsed / 1000)

    # Main Loop
    def RunLoop(self):
        inputs = self.sdl.getInput()
        self.music.PlayMusic()
        while not inputs[engine.QUIT_EVENT]:
            self.frameStartTime = self.sdl.getTimeMS()
            self.Update(inputs := self.sdl.getInput())
            self.Render()
            self.limitFPS()
# Main
def main():
    game = Game(972, 720)
    game.StartGame()
    game.RunLoop()

# Run Main
if __name__ == "__main__":
    main()