#ifndef SPRITE_H
#define SPRITE_H

#include <string>
#include <iostream>
#include <ostream>

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

#include "Transform.hpp"

/**
 * A small class to demonstrate loading sprites.
 * Sprite sheets are often used for loading characters,
 * environments, icons, or other images in a game.
 */
class Sprite {
public:

    Sprite(Transform *_transform, bool readLeftToRight = true);

    ~Sprite();

    /**
	 * Sets the position of the sprite.
	 *
	 * @params:
	 * x - x coordinate of sprite
	 * y - y coordinate of sprite
	 */
    void setPosition(int x, int y);

    /**
	 * Sets the position of the sprite.
	 *
	 * @params:
	 * x - x coordinate of sprite
	 * y - y coordinate of sprite
	 */
    void update(int x, int y, int frame);

    /**
	 * Renders the sprite to the screen.
	 *
	 * @params:
	 * renderer - SDL_Renderer
	 */
    void render(std::uintptr_t rendererAddress, int camOffsetX, int camOffsetY);

    /**
     * Load a sprite
     */
    void loadImage(std::string filePath, std::uintptr_t rendererAddress);

    /**
     * Alternative way of loading a sprite mainly for preview purposes.
     *
     */ 
    void loadImageForPreview(std::string filePath, std::uintptr_t rendererAddress);

	/**
	 * Sets the dimensions of the rectangle the sprite is drawn on.
	 *
	 * @params:
	 * width - the horizontal length of the sprite
	 * height - the vertical lenght of the sprite
	 */
    void setRectangleDimensions(int x, int y);

	/**
	 * Sets the dimesnions of the sprite surface. In other words, 
	 * each frame of the animation should be dimensions frameWidth x frameHeight.
	 * Also records the number of rows and columns in the sprite sheet.
	 */
    void setSpriteSheetDimensions(int frameWidth, int frameHeight, int startX, int startY, int numSpritesInRow, unsigned int totalSprites, unsigned int numPixelsToTrimFromWidth);

	/**
	 * Send function for communicating with other components.
	 */
    int send();

	/**
	 * Receive component for getting information from other components.
	 */
    void receive(int val);

    void identify();

	int getWidth();

	int getHeight();

	int getX();

	int getY();

	int getCenterX();
	
	int getCenterY();

	Transform* mTransform = nullptr;

	void removeSpriteFromManager();

	void shutDownManager();

private:
	int mStartX = 0;
	int mStartY = 0;
    int mPositionX, mPositionY;
	unsigned int    mCurrentFrame, mLastFrame, mNumPixelsToTrimFromWidth;

    // An SDL Surface contains pixel data to draw an image
	SDL_Surface*    mSpriteSheet =  nullptr;
	SDL_Texture*    mTexture     =  nullptr;

	std::string mFilePath;

	SDL_Rect        mSrc, mDest;

    unsigned int mNumSpritesInRow;

	bool mReadLeftToRight;
	int mTextureWidth = 0;
	int mTextureHeight = 0;

	
};


#endif
