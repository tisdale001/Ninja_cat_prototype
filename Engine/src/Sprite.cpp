#include "Sprite.hpp"
#include "SurfaceResourceManager.hpp"
#include "TextureResourceManager.hpp"

/** @brief Constructor
 * 
 * Constructor that takes in Transform pointer and readLeftToRight (bool) as params. 
 * ReadLeftToRight param allows the sprite sheet to be read left-to-right or right-to-left to make it easy to create the necessary sprites and reverse sprites
 * needed for side-scroller game creation.
*/
Sprite::Sprite(Transform* _transform, bool readLeftToRight){
    mTransform = _transform;
    mReadLeftToRight = readLeftToRight;
}

/** @brief Deconstructor
 * 
*/
Sprite::~Sprite(){
}

// Set the sprite position
/** @brief Setter: sets mPositionX and mPositionY
 * 
*/
void Sprite::setPosition(int x, int y){
    mPositionX = x;
    mPositionY = y;
}

/** @brief Finds sprite image that corresponds to frame number.
 * 
 * Finds sprite image that corresponds to frame number. Updates the image selected according to mNumPixelsToTrimFromWidth, which trims extra empty
 * pixels from the width, and mReadLeftToRight, which determines if the sprite sheet is read from left-to-right or right-to-left.
*/
void Sprite::update (int x, int y, int frame){
    // The part of the image that we want to render
    mCurrentFrame = frame;
    if(mCurrentFrame>mLastFrame){
        mCurrentFrame=0;
    }

    if (mReadLeftToRight) {
        mSrc.y = floor(mCurrentFrame / mNumSpritesInRow) * mSrc.h + mStartY;
        mSrc.x = (mCurrentFrame % mNumSpritesInRow) * (mSrc.w + mNumPixelsToTrimFromWidth) + mStartX;
    }
    else {
        mSrc.y = floor(mCurrentFrame / mNumSpritesInRow) * mSrc.h + mStartY;

        int xPos = mTextureWidth;
        if (mStartX != 0){
            xPos = mStartX;
        }

        mSrc.x = xPos - ((mCurrentFrame % mNumSpritesInRow + 1) * (mSrc.w + mNumPixelsToTrimFromWidth) 
            - mNumPixelsToTrimFromWidth);
    }
    
}

/** @brief Renders the desination rectangle (sprite image) adjusted for camera offset
 * 
 * Renders the mDest rectangle (sprite image) adjusted for camOffsetX and camOffsetY.
*/
void Sprite::render(std::uintptr_t rendererAddress, int camOffsetX, int camOffsetY){
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    mDest.x = mTransform->xPos - camOffsetX;
    mDest.y = mTransform->yPos - camOffsetY;
    SDL_RenderCopy(renderer, mTexture, &mSrc, &mDest);
    // std::cout << "Pos: " << mPosition.x << "  Des: " << mDest.x << std::endl;
}

/** @brief Loads and creates sprite sheet from filePath
 * 
 * Loads and creates sprite sheet, mSpriteSheet, according to param filePath.
*/
void Sprite::loadImage(std::string filePath, std::uintptr_t rendererAddress){
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    SurfaceResourceManager::instance().LoadResource(filePath);
    SDL_Surface* mSpriteSheet = SurfaceResourceManager::instance().GetResource(filePath);
    if(nullptr == mSpriteSheet){
           SDL_Log("Failed to allocate surface");
    }else{
        // SDL_Log("Allocated a bunch of memory to create identical game character");
        // Create a texture from our surface
        // Textures run faster and take advantage 
        // of hardware acceleration
        mFilePath = filePath;
        TextureResourceManager::instance().LoadResource(mSpriteSheet, renderer);
        mTexture = TextureResourceManager::instance().GetResource(mSpriteSheet); //SDL_CreateTextureFromSurface(renderer, mSpriteSheet);
	//mTexture = SDL_CreateTextureFromSurface(renderer, mSpriteSheet);
	SDL_Point size;
        SDL_QueryTexture(mTexture, NULL, NULL, &size.x, &size.y);
        mTextureWidth = size.x;
        mTextureHeight = size.y;
        
    }
}

/**
 * @brief Sprite loader for previewing sprite animation
 */ 
void Sprite::loadImageForPreview(std::string filePath, std::uintptr_t rendererAddress){
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    SurfaceResourceManager::instance().LoadResource(filePath);
    SDL_Surface* mSpriteSheet = SurfaceResourceManager::instance().GetResource(filePath);
    if(nullptr == mSpriteSheet){
           SDL_Log("Failed to allocate surface");
    }else{
        // SDL_Log("Allocated a bunch of memory to create identical game character");
        // Create a texture from our surface
        // Textures run faster and take advantage
        // of hardware acceleration
        mFilePath = filePath;
        TextureResourceManager::instance().LoadResource(mSpriteSheet, renderer);
        //mTexture = TextureResourceManager::instance().GetResource(mSpriteSheet); //SDL_CreateTextureFromSurface(renderer, mSpriteSheet);
        mTexture = SDL_CreateTextureFromSurface(renderer, mSpriteSheet);
        SDL_Point size;
        SDL_QueryTexture(mTexture, NULL, NULL, &size.x, &size.y);
        mTextureWidth = size.x;
        mTextureHeight = size.y;

    }
}

/** @brief Setter: sets member variables
 * 
 * Setter method that sets member variable values. Param mSrc width is adjusted by numPixelsToTrimFromWidth.
*/
void Sprite::setSpriteSheetDimensions(int frameWidth, int frameHeight, int startX, int startY, int numSpritesInRow, unsigned int totalSprites, unsigned int numPixelsToTrimFromWidth) {

    mLastFrame = totalSprites - 1;
    mNumPixelsToTrimFromWidth = numPixelsToTrimFromWidth;
    mSrc.w = frameWidth - numPixelsToTrimFromWidth;
    mSrc.h = frameHeight;
    mNumSpritesInRow = numSpritesInRow;
    mStartX = startX;
    mStartY = startY;
}

/** @brief Setter: sets width and height of destination rectangle
 * 
 * Setter method that sets mDest width and height as x and y, respectively
*/
void Sprite::setRectangleDimensions(int x, int y) {

    mDest.w = x;
    mDest.h = y;
}

/** @brief Returns 0
 * 
*/
int Sprite::send() {
    return 0;
}

/** @brief Adds val to mPosition
 * 
*/
void Sprite::receive(int val) {

    mPositionX += val;
}

/** @brief Unused method
 * 
*/
void Sprite::identify () {
    std::cout << "Sprite" << std::endl;
}

/** @brief Getter: returns mDest width
 * 
*/
int Sprite::getWidth() {

    return mDest.w;
}

/** @brief Getter: returns mDest height
 * 
*/
int Sprite::getHeight() {

    return mDest.h;
}

/** @brief Getter: returns xPos from mTransform
 * 
*/
int Sprite::getX() {
    
    return mTransform->xPos;
}

/** @brief Getter: returns yPos from mTransform
 * 
*/
int Sprite::getY() {

    return mTransform->yPos;
}

/** @brief Getter: returns x coordinate of center of rectangle, using xPos value from mTransform
 * 
*/
int Sprite::getCenterX() {

    return mTransform->xPos + mDest.w / 2;
}

/** @brief Getter: returns y coordinate of center of rectangle, using yPos value from mTransform
 * 
*/
int Sprite::getCenterY() {

    return mTransform->yPos + mDest.h / 2;
}

/** @brief Removes resources from manager
 * 
*/
void Sprite::removeSpriteFromManager() {

    if (mSpriteSheet && mTexture) {
        TextureResourceManager::instance().RemoveResource(mSpriteSheet);
    } 
    if (mSpriteSheet) {
        SurfaceResourceManager::instance().RemoveResource(mFilePath);
    }
}

/** @brief Calls shutDown for items in manager
 * 
*/
void Sprite::shutDownManager() {

    TextureResourceManager::instance().shutDown();
    SurfaceResourceManager::instance().shutDown();
}
