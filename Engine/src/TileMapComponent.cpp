#include <iostream>
#include <iomanip>
#include <string>

#include <SDL2/SDL_image.h>

#include "Rectangle.hpp"
#include "TileMapComponent.hpp"
#include "LevelReader.hpp"

/** @brief Overloaded Constructor with param levelPath
 * 
 * Overloaded Constructor that takes in levelPath string as parameter. Sets all member variables using LevelReader.
*/
TileMapComponent::TileMapComponent(const std::string& levelPath, int offSetX, int offSetY) {
    mOffSetX = offSetX;
    mOffSetY = offSetY;
    LevelReader levelReader(levelPath);
    mRows = levelReader.getRows();
    mCols = levelReader.getCols();
    mSize = levelReader.getTileSize();
    mTilesetRows = levelReader.getTilesetRows();
    mTilesetCols = levelReader.getTilesetCols();
    mTiles = levelReader.getTiles();
    // PrintTiles();
}

/** @brief Overloaded Constructor with rows, cols, and size as parameters
 * 
 * Overloaded Constructor that takes in rows, cols, size as parameters. Sets member variables and creates a temporary level for testing.
*/
TileMapComponent::TileMapComponent(int rows, int cols, int size) {
    mRows = rows;
    mCols = cols;
    mSize = size;
    mTiles.reserve(rows*cols);
    for (int i = 0; i < rows*cols; i++) {
        mTiles.push_back(0);
    }

    // Temporary level for testing
    mTiles[1] = 1;
    mTiles[3] = 1;
    // mTiles[14] = 1;
    // mTiles[23] = 1;
    // mTiles[36] = 1;
    // mTiles[34] = 1;
    // setTile(5, 5, 1);
    // setTile(4, 6, 1);
    // setTile(5, 7, 1);
    // setTile(6, 8, 1);
    for (int row = 0; row < mRows; row++) {
        for (int col = 0; col < mCols; col++) {
            if (row == 0 || col == 0 || row == mRows - 1 || col == mCols - 1) {
                setTile(row, col, 1);
            }
        }
    }

    setTile(18, 3, 1);
    setTile(17, 3, 1);
    setTile(16, 3, 1);

    setTile(18, 5, 1);
    setTile(17, 5, 1);
    setTile(16, 5, 1);

    setTile(14, 6, 1);
    setTile(14, 7, 1);
    setTile(14, 8, 1);

    setTile(17, 7, 1);

    setTile(12, 9, 1);
    setTile(12, 10, 1);
    // PrintTiles();
}

/** @brief Deconstructor
 * 
 * Deconstructor: destroys tilesetTexture and calls IMG_Quit()
*/
TileMapComponent::~TileMapComponent() {
    SDL_DestroyTexture(tilesetTexture);
    IMG_Quit();
}

/** @brief extends the tilemap given a level
 * 
 * extends the current tilemap given a level's file path, must be same height.
*/
void TileMapComponent::ExtendTilemap(const std::string& levelPath) {
    LevelReader levelReader(levelPath);
    if (mSize != levelReader.getTileSize() || mTilesetRows != levelReader.getTilesetRows() ) { 
        //|| mTilesetCols != levelReader.getTilesetCols()
        // std::cout << "ExtendTilemap mismatched tileset" << std::endl;
        return;
    }
    int addedRows = levelReader.getRows();
    int addedCols = levelReader.getCols();
    std::vector<int> newTiles = levelReader.getTiles();
    int oldRows = mRows;
    int oldCols = mCols;
    //mRows = oldRows + addedRows;
    mCols = oldCols + addedCols;
    mTiles.resize(mRows * mCols);

    for (int row = 0; row < addedRows; row++) {
        for (int col = 0; col < addedCols; col++) {
            mTiles.insert(mTiles.begin() + getTileIdx(row, col+oldCols), newTiles[col+row*addedCols]);
        }
    }
}

/** @brief Method loads tileset from tileset path
 * 
 * Method loads tileset from param tilesetPath. Must be called by user after TileMapComponent is initialized.
 * Otherwise, it will cause a segmentation fault.
*/
void TileMapComponent::loadTileset(std::string tilesetPath, std::uintptr_t rendererAddress) {
        SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
        int flags = IMG_INIT_PNG; // Only loading pngs for now
        int status = IMG_Init(flags);
        if ((status & flags) != flags) {
            std::cout << "Error initializing SDL_Image: " << IMG_GetError() << std::endl;
            exit(1);
        }
        SDL_Surface* tilesetSurface = IMG_Load(tilesetPath.c_str());
        if (!tilesetSurface) {
            std::cout << "Error loading surface: " << IMG_GetError() << std::endl;
            exit(1);
        }
        tilesetTexture = SDL_CreateTextureFromSurface(renderer, tilesetSurface);
        if (!tilesetTexture) {
            std::cout << "Error creating texture: " << SDL_GetError() << std::endl;
            exit(1);
        }
        SDL_FreeSurface(tilesetSurface);
}

/** @brief Renders all tiles according to camera offset
 * 
 * Renders all tiles according to camera offset. Blank tiles are now left blank.
*/
void TileMapComponent::Render(std::uintptr_t rendererAddress, int camOffsetX, int camOffsetY) {
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    int tileIdx = 0;
    for (int y = 0; y < mRows * mSize; y += mSize) {
        for (int x = 0; x < mCols * mSize; x += mSize) {
            int tileType = mTiles[tileIdx];
            if (tileType >= 0) {
                int rowIdx = tileType / mTilesetCols;
                int colIdx = tileType % mTilesetCols;
                SDL_Rect srcRect = {colIdx * mSize + mOffSetX, rowIdx * mSize + mOffSetY, mSize, mSize};
                SDL_Rect destRect = {x - camOffsetX, y - camOffsetY, mSize, mSize};
                SDL_RenderCopy(renderer, tilesetTexture, &srcRect, &destRect);
            }
            // else {
            //     SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
            //     SDL_Rect rect = {x - camOffsetX, y - camOffsetY, mSize, mSize};
            //     SDL_RenderDrawRect(renderer, &rect); // Show tile grid for debug
            // }
            tileIdx++;
        }
    }
}

/** @brief Checks for collisions around GameObject. Returns collision object.
 * 
 * Gets tiles on object's left, right, top, and bottom edges.
 * Iterate from left to right and top to bottom of tiles covered
 * to check for collisions. Returns a Collision object.
*/
Collision TileMapComponent::checkCollision(GameObject* o) {
    Collision collision;
    collision.isColliding = false;
    if (o->mSprite != nullptr) {
        Sprite* r = o->mSprite;
        int leftTile = r->getX() / mSize;
        int rightTile = (r->getX() + r->getWidth() - 1) / mSize;
        int topTile = r->getY() / mSize;
        int bottomTile = (r->getY() + r->getHeight() - 1) / mSize;
        
        std::vector<int> allTypes;
        for (int col = leftTile; col <= rightTile; col++) {
            for (int row = topTile; row <= bottomTile; row++) {
                int tileIdx = tileAt(row, col);
                if (tileIdx >= 0) { // TODO: test >-
                    if (!collision.isColliding) {
                        collision.isColliding = true;
                        collision.firstTileRow = row;
                        collision.firstTileColumn = col;
                        collision.firstTileID = tileIdx;
                    }
                    allTypes.push_back(tileIdx);
                }
            }
        }
        collision.allTileTypes = allTypes;
        
    }
    else if (o->mRectangle != nullptr) {
        RectangleComponent* r = o->mRectangle;
        int leftTile = r->getX() / mSize;
        int rightTile = (r->getX() + r->getWidth() - 1) / mSize;
        int topTile = r->getY() / mSize;
        int bottomTile = (r->getY() + r->getHeight() - 1) / mSize;
        
        std::vector<int> allTypes;
        for (int col = leftTile; col <= rightTile; col++) {
            for (int row = topTile; row <= bottomTile; row++) {
                int tileIdx = tileAt(row, col);
                if (tileIdx >= 0) {
                    if (!collision.isColliding) {
                        collision.isColliding = true;
                        collision.firstTileRow = row;
                        collision.firstTileColumn = col;
                        collision.firstTileID = tileIdx;
                    }
                    allTypes.push_back(tileIdx);
                }
            }
        }
        collision.allTileTypes = allTypes;
        
    }
    
    return collision;
}


/** @brief Checks if sprite or rectangle is touching the top of a tile.
 * 
 * Checks if GameObject's mSprite or mRectangle is touching the top of a tile (floor). Takes in GameObject pointer
 * as parameter.
*/
Collision TileMapComponent::isOnGround(GameObject* o) {
    Collision collision;
    collision.isColliding = false;
    if (o->mSprite != nullptr) {
        Sprite* r = o->mSprite;
        int leftTile = (r->getX()) / mSize;
        int rightTile = (r->getX() + r->getWidth()) / mSize;
        int belowTile = (r->getY() + r->getHeight() + 1) / mSize; // row below object
        // std::cout << "leftTile= " << leftTile << ", rightTile= " << rightTile << ", belowTile= " << belowTile << std::endl;
        std::vector<int> allTypes;
        
        for (int col = leftTile; col <= rightTile; col++) {
            
            int tileIdx = tileAt(belowTile, col);
            if (tileIdx >= 0) {
                if (!collision.isColliding) {
                    collision.isColliding = true;
                    collision.firstTileRow = belowTile;
                    collision.firstTileColumn = col;
                    collision.firstTileID = tileIdx;
                }
                allTypes.push_back(tileIdx);
            }
            
        }
        collision.allTileTypes = allTypes;
    }
    // else if (o->mRectangle != nullptr) {
    //     RectangleComponent* r = o->mRectangle;
    //     int leftTile = r->getX() / mSize;
    //     int rightTile = (r->getX() + r->getWidth() - 1) / mSize;
    //     int belowTile = (r->getY() + r->getHeight()) / mSize; // row below object
    //     Collision collision;
    //     for (int col = leftTile; col <= rightTile; col++) {
    //         if (tileAt(belowTile, col) >= 0) {
    //             return true;
    //         }
    //     }
    //     return false;
    // }    
    return collision;
    
}

/** @brief Checks if sprite or rectangle is touching the bottom of a tile.
 * 
 * Checks if GameObject's mSprite or mRectangle is touching the bottom of a tile (ceiling). Takes in GameObject pointer
 * as parameter.
*/
Collision TileMapComponent::isOnCeiling(GameObject* o) {
    Collision collision;
    collision.isColliding = false;
    if (o->mSprite != nullptr) {
        Sprite* r = o->mSprite;
        int leftTile = (r->getX()) / mSize;
        int rightTile = (r->getX() + r->getWidth()) / mSize;
        int aboveTile = (r->getY()) / mSize; // row above object
        std::vector<int> allTypes;

        for (int col = leftTile; col <= rightTile; col++) {
            int tileIdx = tileAt(aboveTile, col);
            if (tileIdx >= 0) {
                if (!collision.isColliding) {
                    collision.isColliding = true;
                    collision.firstTileRow = aboveTile;
                    collision.firstTileColumn = col;
                    collision.firstTileID = tileIdx;
                }
                allTypes.push_back(tileIdx);
            }
        }
        collision.allTileTypes = allTypes;
    }
    // else if (o->mRectangle != nullptr) {
    //     RectangleComponent* r = o->mRectangle;
    //     int leftTile = r->getX() / mSize;
    //     int rightTile = (r->getX() + r->getWidth() - 1) / mSize;
    //     int aboveTile = (r->getY() - 1) / mSize; // row above object
    //     Collision collision;
    //     for (int col = leftTile; col <= rightTile; col++) {
    //         if (tileAt(aboveTile, col) >= 0) {
    //             return true;
    //         }
    //     }
    //     return false;
    // }
    return collision;
    
}


/** @brief Checks if sprite or rectangle is touching tile to the right.
 * 
 * Checks if GameObject's mSprite or mRectangle is touching a tile to the right (right wall). Takes in GameObject
 * as parameter.
*/
Collision TileMapComponent::isTouchingRightWall(GameObject* o) {
    Collision collision;
    collision.isColliding = false;
    if (o->mSprite != nullptr) {
        Sprite* r = o->mSprite;
        int topTile = r->getY() / mSize;
        int bottomTile = (r->getY() + r->getHeight() - 1) / mSize;
        int rightTile = (r->getX() + r->getWidth() + 5) / mSize; // col to right of object
        //std::cout << "topTile= " << topTile << ", bottomTile= " << bottomTile << ", rightTile= " << rightTile << std::endl;
        std::vector<int> allTypes;

        for (int row = topTile; row <= bottomTile; row++) {
            if (rightTile < getCols()) {
                int tileIdx = tileAt(row, rightTile);
                if (tileIdx >= 0) { // TODO: test >-
                    if (!collision.isColliding) {
                        collision.isColliding = true;
                        collision.firstTileRow = row;
                        collision.firstTileColumn = rightTile;
                        collision.firstTileID = tileIdx;
                    }
                    allTypes.push_back(tileIdx);
                }
            }
            
        }
        collision.allTileTypes = allTypes;
    }
    // else if (o->mRectangle != nullptr) {
    //     RectangleComponent* r = o->mRectangle;
    //     int topTile = r->getY() / mSize;
    //     int bottomTile = (r->getY() + r->getHeight() - 1) / mSize;
    //     int rightTile = (r->getX() + r->getWidth()) / mSize; // col to right of object

    //     for (int row = topTile; row <= bottomTile; row++) {
    //         if (rightTile < getCols() && tileAt(row, rightTile) >= 0) {
    //             return true;
    //         }
            
    //     }
    //     return false;
    // }
    return collision;
    
}
/** @brief Checks if sprite or rectangle is touching tile to the left.
 * 
 * Checks if GameObject's mSprite or mRectangle is touching a tile to the left (left wall). Takes in GameObject
 * as parameter.
*/
Collision TileMapComponent::isTouchingLeftWall(GameObject* o) {
    Collision collision;
    collision.isColliding = false;
    if (o->mSprite != nullptr) {
        Sprite* r = o->mSprite;
        int topTile = r->getY() / mSize;
        //std::cout << "sprite->getY(): " << r->getY() << std::endl;
        // int bottomTile = (r->getY() + r->getHeight() - mSize) / mSize;
        int bottomTile = (r->getY() + r->getHeight() - 1) / mSize;
        int leftTile = (r->getX() - 6) / mSize; // col to left of object
        //std::cout << "topTile= " << topTile << ", bottomTile= " << bottomTile << ", leftTile= " << leftTile << std::endl;

        std::vector<int> allTypes;

        // std::cout << "isTouchingLeftWall()" << std::endl;
        for (int row = topTile; row <= bottomTile; row++) {
            if (leftTile >= 0) {
                int tileIdx = tileAt(row, leftTile);
                if (tileIdx >= 0) { // TODO: test >-
                    if (!collision.isColliding) {
                        collision.isColliding = true;
                        collision.firstTileRow = row;
                        collision.firstTileColumn = leftTile;
                        collision.firstTileID = tileIdx;
                    }
                    allTypes.push_back(tileIdx);
                }
            }
        }
        collision.allTileTypes = allTypes;
    }
    // else if (o->mRectangle != nullptr) {
    //     RectangleComponent* r = o->mRectangle;
    //     int topTile = r->getY() / mSize;
    //     int bottomTile = (r->getY() + r->getHeight() - 1) / mSize;
    //     int leftTile = r->getX() / mSize - 1; // col to left of object

    //     // std::cout << "isTouchingLeftWall()" << std::endl;
    //     for (int row = topTile; row <= bottomTile; row++) {
    //         if (leftTile >= 0 && tileAt(row, leftTile) >= 0) {
    //             return true;
    //         }
    //     }
    //     return false;
    // }
    return collision;
    
}

/** @brief Checks if a collision is touching a tile with the given type.
 * 
 * Checks if a collision is touching a tile with the given type.
*/
bool TileMapComponent::isTouchingType(Collision collision, int id) {
    return std::count(collision.allTileTypes.begin(), collision.allTileTypes.end(), id);
}

/** @brief Getter method: returns mRows
 * 
*/
int TileMapComponent::getRows() {
    return mRows;
}

/** @brief Getter method: returns mCols
 * 
*/
int TileMapComponent::getCols() {
    return mCols;
}

/** @brief Getter method: returns mSize
 * 
*/
int TileMapComponent::getSize() {
    return mSize;
}

/** @brief Determines if tile is on grid.
 * 
 * Determines if tile is on grid by checking if row and col are valid.
*/
bool TileMapComponent::isValidTile(int row, int col) {
    return (row >= 0 || row < mRows) && (col >= 0 || col < mCols);
}

/** @brief Returns number (name) of tile at position (row, col).
 * 
 * Returns number (name) of tile at position according to row and col position.
*/
int TileMapComponent::tileAt(int row, int col) {
    int tileIdx = getTileIdx(row, col);
    if (tileIdx >= 0) {
        return mTiles[tileIdx];
    }
    return -1;
}

// onGround
// get bot left and right corner, check if tiles 1 down and between are ground
/** @brief Returns numer (name) of tile at (x, y) position.
 * 
 * Returns number (name) of tile at position according to x and y position.
*/
int TileMapComponent::tileAtXY(int x, int y) {
    int col = x / mSize;
    int row = y / mSize;
    return tileAt(row, col);
}

/** @brief Internal method. Returns index of tile by (row, col) position.
 * 
 * Internal method. Returns index of tile in mTiles by inputs row and col.
*/
int TileMapComponent::getTileIdx(int row, int col) {
    if (isValidTile(row, col)) {
        return row * mCols + col;
    }
    return -1;
}

/** @brief Setter: sets name/type of tile at (row, col) position.
 * 
 * Setter method that sets name (int) of tile at position according to row and col.
*/
void TileMapComponent::setTile(int row, int col, int type) {
    int tileIdx = getTileIdx(row, col);
    if (tileIdx >= 0) {
        mTiles[tileIdx] = type;
    }
}

/** @brief Prints all tiles in grid. For debugging.
 *
*/
void TileMapComponent::PrintTiles() {
    std::cout << "Printing Tiles" << std::endl;
    for (int row = 0; row < mRows; row++) {
        for (int col = 0; col < mCols; col++) {
            std::cout << tileAt(row, col) << "   ";
        }
        std::cout << "|||" << std::endl;
    }
}