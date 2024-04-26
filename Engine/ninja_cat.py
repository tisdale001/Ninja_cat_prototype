from lib import engine
import math

###############################################################################################################################################################


class PlayerState:
    def __init__(self):
        self.state = "falling"
    def setState(self, s):
        self.state = s
    def getState(self):
        return self.state


# Represents a Ninja Cat Game
class Game:
    # Initialize Game
    def __init__(self, windowWidth, windowHeight):
        # SDL Setup
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth # self.tileSize * 27 = 864
        self.windowHeight = windowHeight # self.tileSize * 20 = 640
        # Tilemap Setup
        self.tilemap1 = engine.TileMapComponent("Assets/Levels/Tileset5/ninja_cat_practice_1.lvl", 0, 0)
        self.tilemap1.loadTileset("Assets/tilesets/Tileset5.png", self.sdl.getSDLRenderer())
        # tilemap side or vertical dict
        self.sideOrVertDict = {}
        self.sideOrVertDict[str(self.tilemap1)] = "horizontal"
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
        self.playerJump = engine.JumpComponent(-140, 290, 6, -2)
        self.player.addJumpComponent(self.playerJump)
        # Setup PlayerState
        self.playerState = PlayerState()

        self.maxFrameDict = {}
        
        self.createPlayerSprites()

        self.lvlHeight1 = self.tilemap1.getRows() * self.tileSize
        self.lvlWidth1 = self.tilemap1.getCols() * self.tileSize

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
        self.music.SetMusic("Assets/Sounds/86 - Escape.mp3")
        self.playerJumpSound = engine.Sound()
        self.playerJumpSound.SetSound("Assets/Sounds/Metroid_sounds/Sound Effect (6).wav")
        

        # Player Settings
        self.playerRunSpeed = 8
        self.playerPunchSpeed = 4
        self.playerFallingSpeed = 10
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
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
        self.playerJumpingFrameIncrement = 0.25

        self.isPunching = False

        # Game Variables
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerFallingSpeed
        
        # Frame capping variables
        targetFPS = 50 # TODO: set back to 50
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
        self.run_right_sprite.setRectangleDimensions(120, 68) # was 120, 68
        self.run_right_sprite.setSpriteSheetDimensions(900, 520, 340, 260 * 2 + 520 * 3, 6, 6, 20)
        self.run_right_sprite.loadImage("Assets/spritesheets/Black Cat Game Sprite Right.png", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.run_right_sprite)
        self.maxFrameDict[str(self.run_right_sprite)] = 5

        self.run_left_sprite = engine.Sprite(self.playerTransform, False)
        self.run_left_sprite.setRectangleDimensions(120, 68)
        self.run_left_sprite.setSpriteSheetDimensions(900, 520, 900 * 7 - 550, 260 * 2 + 520 * 3, 6, 6, 0)
        self.run_left_sprite.loadImage("Assets/spritesheets/Black Cat Game Sprite Left.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_sprite)] = 5

        self.idle_right = engine.Sprite(self.playerTransform, True)
        self.idle_right.setRectangleDimensions(120, 68)
        self.idle_right.setSpriteSheetDimensions(900, 520, 400 + 900 * 1, 260, 1, 1, 68)
        self.idle_right.loadImage("Assets/spritesheets/Black Cat Game Sprite Right.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right)] = 0

        self.idle_left = engine.Sprite(self.playerTransform, False)
        self.idle_left.setRectangleDimensions(120, 68)
        self.idle_left.setSpriteSheetDimensions(900, 520, 900 * 6 - 620, 260, 1, 1, 68)
        self.idle_left.loadImage("Assets/spritesheets/Black Cat Game Sprite Left.png", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left)] = 0

        self.jump_right = engine.Sprite(self.playerTransform, True)
        self.jump_right.setRectangleDimensions(110, 100) # used to be 110, 100
        self.jump_right.setSpriteSheetDimensions(796, 220, 34 + 796, 870, 4, 4, 502)
        self.jump_right.loadImage('Assets/spritesheets/black-cat-jumping-right-transparent.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.jump_right)] = 3

        self.jump_left = engine.Sprite(self.playerTransform, False)
        self.jump_left.setRectangleDimensions(110, 100)
        self.jump_left.setSpriteSheetDimensions(796, 220, -44 + 796 * 4, 870, 4, 4, 502)
        self.jump_left.loadImage('Assets/spritesheets/black-cat-jumping-left-transparent.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.jump_left)] = 3

        self.falling_right = engine.Sprite(self.playerTransform, True)
        self.falling_right.setRectangleDimensions(110, 100)
        self.falling_right.setSpriteSheetDimensions(796, 220, 26 + 796 * 4, 870, 1, 1, 502)
        self.falling_right.loadImage('Assets/spritesheets/black-cat-jumping-right-transparent.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.falling_right)] = 0

        self.falling_left = engine.Sprite(self.playerTransform, False)
        self.falling_left.setRectangleDimensions(110, 100)
        self.falling_left.setSpriteSheetDimensions(796, 220, -30 + 796, 870, 1, 1, 502)
        self.falling_left.loadImage('Assets/spritesheets/black-cat-jumping-left-transparent.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.falling_left)] = 0

        self.punch_right = engine.Sprite(self.playerTransform, True)
        self.punch_right.setRectangleDimensions(80, 110)
        self.punch_right.setSpriteSheetDimensions(1300, 998, 162, 200, 3, 3, 660)
        self.punch_right.loadImage('Assets/spritesheets/black-cat-game-sprite/black_cat_upright/black_cat_upright_transparent.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.punch_right)] = 2

        self.punch_left = engine.Sprite(self.playerTransform, False)
        self.punch_left.setRectangleDimensions(80, 110)
        self.punch_left.setSpriteSheetDimensions(1280, 998, -258 + 1300 * 3, 200, 3, 3, 662)
        self.punch_left.loadImage('Assets/spritesheets/black-cat-game-sprite/black_cat_upright/black_cat_upright_left_transparent.png', self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.punch_left)] = 2

    
    def changePlayerSprite(self, sprite):
        # adjusts yPos if necessary and changes sprite
        if sprite.getHeight() > self.player.mSprite.getHeight():
            self.player.mTransform.yPos -= (sprite.getHeight() - self.player.mSprite.getHeight())
        self.player.addSpriteComponent(sprite)
        self.currentMaxFrame = self.maxFrameDict[str(sprite)]

    # Handles player left and right movement from input
    def handlePlayerMove(self, inputs):
        jumpAgain = False
        if inputs[engine.J_PRESSED] or inputs[engine.Z_PRESSED] and self.jumpTimer <= 0:
            jumpAgain = True
        if (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]) and not (inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]):
            if self.playerState.getState() == "standing" and self.isPunching:
                self.curXDirection = -1
                self.player.xVel = - self.playerPunchSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isFirstStandingFrame:
                    self.playerTransform.yPos -= self.diffBetweenStandingAndDucking
                    self.isFirstStandingFrame = False
                    # change to running left
                    self.changePlayerSprite(self.punch_left)
                    self.waitOneFrameForShot = True
                elif jumpAgain:
                    
                    self.changePlayerSprite(self.falling_left)
                else:
                    self.changePlayerSprite(self.punch_left)
                    self.waitOneFrameForShot = True
            elif self.playerState.getState() == "standing":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isFirstStandingFrame:
                    self.playerTransform.yPos -= self.diffBetweenStandingAndDucking
                    self.isFirstStandingFrame = False
                    # change to running left
                    self.changePlayerSprite(self.run_left_sprite)
                    self.waitOneFrameForShot = True
                elif jumpAgain:
                    
                    self.changePlayerSprite(self.falling_left)
                else:
                    self.changePlayerSprite(self.run_left_sprite)
                    self.waitOneFrameForShot = True
            elif self.playerState.getState() == "jumping":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.changePlayerSprite(self.jump_left)
            elif self.playerState.getState() == "falling":
                self.curXDirection = -1
                self.player.xVel = - self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                self.changePlayerSprite(self.falling_left)
                self.waitOneFrameForShot = True

        elif (inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]) and not (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]):
            if self.playerState.getState() == "standing" and self.isPunching:
                self.curXDirection = 1
                self.player.xVel = self.playerPunchSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isFirstStandingFrame:
                    self.isFirstStandingFrame = False
                    self.changePlayerSprite(self.punch_right)
                    self.waitOneFrameForShot = True
                elif jumpAgain:
                    self.changePlayerSprite(self.falling_right)
                else:
                    self.changePlayerSprite(self.punch_right)
                    self.waitOneFrameForShot = True
            elif self.playerState.getState() == "standing":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isFirstStandingFrame:
                    self.isFirstStandingFrame = False
                    self.changePlayerSprite(self.run_right_sprite)
                    self.waitOneFrameForShot = True
                elif jumpAgain:
                    self.changePlayerSprite(self.falling_right)
                else:
                    self.changePlayerSprite(self.run_right_sprite)
                    self.waitOneFrameForShot = True
            elif self.playerState.getState() == "jumping":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.changePlayerSprite(self.jump_right)
            elif self.playerState.getState() == "falling":
                self.curXDirection = 1
                self.player.xVel = self.playerRunSpeed
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
                if self.isShooting():
                    self.changePlayerSprite(self.shooting_falling_right)
                else:
                    self.changePlayerSprite(self.falling_right)
                    self.waitOneFrameForShot = True

        else:
            # player does not move along x-axis
            if self.playerState.getState() == "standing" and self.isPunching:
                self.player.xVel = 0
                if self.curXDirection > 0:
                    if jumpAgain:
                        self.changePlayerSprite(self.falling_right)
                    elif self.isFirstStandingFrame:
                        self.isFirstStandingFrame = False
                        self.changePlayerSprite(self.punch_right)
                    else:
                        self.changePlayerSprite(self.punch_right)

                else:
                    if jumpAgain:
                        self.changePlayerSprite(self.falling_left)
                    elif self.isFirstStandingFrame:
                        self.isFirstStandingFrame = False
                        self.changePlayerSprite(self.punch_left)
                    else:
                        self.changePlayerSprite(self.punch_left)
            elif self.playerState.getState() == "standing":
                self.player.xVel = 0
                if self.curXDirection > 0:
                    if jumpAgain:
                        self.changePlayerSprite(self.falling_right)
                    elif self.isFirstStandingFrame:
                        self.isFirstStandingFrame = False
                        self.changePlayerSprite(self.idle_right)
                    else:
                        self.changePlayerSprite(self.idle_right)

                else:
                    if jumpAgain:
                        self.changePlayerSprite(self.falling_left)
                    elif self.isFirstStandingFrame:
                        self.isFirstStandingFrame = False
                        self.changePlayerSprite(self.idle_left)
                    else:
                        self.changePlayerSprite(self.idle_left)
            elif self.playerState.getState() == "jumping":
                self.player.xVel = 0
                if self.curXDirection > 0:
                    self.changePlayerSprite(self.jump_right)
                else:
                    self.changePlayerSprite(self.jump_left)
            elif self.playerState.getState() == "falling":
                self.player.xVel = 0
                self.player.yVel = self.playerFallingSpeed * self.curYDirection
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
    
    def isShooting(self):
        if self.shootingCounter <= self.shootingCounterMax:
            return True
        return False
        

    def changeToFalling(self, inputs):
        self.playerState.setState("falling")
        if self.curXDirection > 0:
            self.player.addSpriteComponent(self.falling_right)
            self.currentMaxFrame = self.maxFrameDict[str(self.falling_right)]
            self.waitOneFrameForShot = True
        else:
            self.player.addSpriteComponent(self.falling_left)
            self.currentMaxFrame = self.maxFrameDict[str(self.falling_left)]
            self.waitOneFrameForShot = True

    # Handles player jump logic
    def handlePlayerJump(self, inputs):
        self.decrementJumpTimer()
        currentState = self.playerState.getState()
        if currentState == "jumping":
            wait = False
            if self.waitOneCycleToInitiateJump:
                wait = True
                self.waitOneCycleToInitiateJump = False

            if not self.playerJump.stillJumping() and not wait:
                # change to falling
                self.changeToFalling(inputs)
            elif inputs[engine.J_PRESSED] or inputs[engine.Z_PRESSED] and self.jumpTimer <= 0:
                # continue jump
                self.playerJump.Update(self.player)
                if self.uprightJump:
                    if self.curXDirection > 0:
                        self.changePlayerSprite(self.jump_right)
                        self.waitOneFrameForShot = True
                    else:
                        self.changePlayerSprite(self.jump_left)
                        self.waitOneFrameForShot = True

            else:
                # stop jump
                self.playerJump.EndJump()
                self.uprightJump = False
                self.playerState.setState("falling")
                self.changeToFalling(inputs)
        else:
            if inputs[engine.J_PRESSED] or inputs[engine.Z_PRESSED] and currentState == "standing":
                if self.jumpTimer <= 0:
                    self.player.InitiateJump()
                    self.currentFrame = 0
                    self.playerJumpSound.PlaySound()
                    self.waitOneCycleForJumpUpdate = True
                    self.waitOneCycleToInitiateJump = True
                    # if UP_PRESSED: should go to else statement(uprightJump)
                    if (inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]):
                        self.uprightJump = False
                        self.playerState.setState("jumping")
                        self.shootingCounter = self.shootingCounterMax + 1
                        self.waitOneFrameForShot = True
                        self.changePlayerSprite(self.jump_right)
                    elif (inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]):
                        self.uprightJump = False
                        self.playerState.setState("jumping")
                        self.shootingCounter = self.shootingCounterMax + 1
                        self.waitOneFrameForShot = True
                        self.changePlayerSprite(self.jump_left)
                    else:
                        self.uprightJump = True
                        if self.curXDirection > 0:
                            self.playerState.setState("jumping")
                            currentWidth = self.player.mSprite.getWidth()
                            self.changePlayerSprite(self.jump_right)
                            self.waitOneFrameForShot = True
                            collision = self.tilemap.isTouchingRightWall(self.player)
                            if collision.isColliding:
                                self.playerTransform.xPos -= (self.falling_right.getWidth() - currentWidth)

                        else:
                            self.playerState.setState("jumping")
                            self.changePlayerSprite(self.jump_left)
                            self.waitOneFrameForShot = True

    def decrementJumpTimer(self):
        if self.jumpTimer > 0:
            self.jumpTimer -= 1

    # Handles player touching wall
    def handlePlayerWallCollision(self):
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
                if currentState == "falling":
                    self.changeToStanding(collision, inputs)
                elif currentState == "jumping":
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
        jumpAgain = False
        # aimUp = False
        if inputs[engine.J_PRESSED] or inputs[engine.Z_PRESSED] and self.jumpTimer <= 0:
            jumpAgain = True
        if inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
            if jumpAgain:
                self.player.addSpriteComponent(self.jump_right)
                self.currentMaxFrame = self.maxFrameDict[str(self.jump_right)]
                self.waitOneFrameForShot = True
                self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.jump_right.getHeight() - 1
            else:
                self.player.addSpriteComponent(self.run_right_sprite)
                self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]
                self.waitOneFrameForShot = True
                self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.run_right_sprite.getHeight() - 1
        elif inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]:
            if jumpAgain:
                self.player.addSpriteComponent(self.jump_left)
                self.currentMaxFrame = self.maxFrameDict[str(self.jump_left)]
                self.waitOneFrameForShot = True
                self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.jump_left.getHeight() - 1
            else:
                self.player.addSpriteComponent(self.run_left_sprite)
                self.currentMaxFrame = self.maxFrameDict[str(self.run_left_sprite)]
                self.waitOneFrameForShot = True
                self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.run_left_sprite.getHeight() - 1
        else:
            if self.curXDirection > 0:
                if jumpAgain:
                    self.player.addSpriteComponent(self.jump_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.jump_right)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.jump_right.getHeight() - 1
                else:
                    self.player.addSpriteComponent(self.idle_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_right)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.idle_right.getHeight() - 1
            else:
                if jumpAgain:
                    self.player.addSpriteComponent(self.jump_left)
                    self.currentMaxFrame = self.maxFrameDict[str(self.jump_left)]
                    self.player.mTransform.yPos = self.tileSize * (collision.firstTileRow) - self.jump_left.getHeight() - 1
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

    def handlePlayerPunching(self, inputs):
        if (inputs[engine.H_PRESSED] or inputs[engine.K_PRESSED] or inputs[engine.X_PRESSED]):
            self.isPunching = True
        else:
            self.isPunching = False


                    
    # Handles all player associated updates
    def playerUpdate(self, inputs):
        # Player left and right movement
        self.handlePlayerMove(inputs)
        # Physics update on player xPos
        self.physics.UpdateX(self.player)
        self.handlePlayerWallCollision()
        self.handlePlayerJump(inputs)

        # Physics update on player yPos
        self.physics.UpdateY(self.player)
        collisionFloor = self.handlePlayerFloorCollision(inputs)
        self.handlePlayerCeilingCollision(inputs)
        self.handlePlayerPunching(inputs)
        
        # update frame
        if self.currentFrame > self.currentMaxFrame:
            self.currentFrame = 0
        
        if self.frameUpdateDelay > self.maxFrameUpdateDelay:
            self.frameUpdateDelay = 0
            if self.currentFrame > self.currentMaxFrame:
                self.currentFrame = 0
            elif self.playerState.getState() == "jumping":
                self.currentFrame += self.playerJumpingFrameIncrement
            else:
                self.currentFrame += 1
        else:
            self.frameUpdateDelay += 1
        self.player.mSprite.update(0, 0, int(self.currentFrame))
                                
    
    # Update
    def Update(self, inputs):
        # Quit check
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
        self.playerUpdate(inputs)
        # update camera
        self.camera.Update()

    # Render
    def Render(self):
        # self.sdl.clear(60, 60, 60, 255) # This is code for gray background
        # self.sdl.clear(0, 0, 0, 0) # This is code for black background
        self.sdl.clear(255, 255, 255, 255) # This is code for white background
        self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.player.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
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
    game = Game(864, 640)
    game.StartGame()
    game.RunLoop()

# Run Main
if __name__ == "__main__":
    main()