#include "SpriteVerticalScrollerCamera.hpp"
#include <algorithm>

/** @brief Constructor
 * 
 * Constructor that takes in dimensions and, for now, a RectangleComponent as the main character
 * 
*/
SpriteVerticalScrollerCamera::SpriteVerticalScrollerCamera(int camWidth, int camHeight, int lvlWidth, int lvlHeight, Sprite* sp):
    cameraWidth(camWidth),
    cameraHeight(camHeight),
    levelWidth(lvlWidth),
    levelHeight(lvlHeight),
    target(sp) {
        y = std::clamp(sp->getCenterY() - cameraHeight/2, 0, levelHeight - cameraHeight);
        x = 0; // Set to left of level by default
    }
/** @brief Deconstructor
 * 
*/
SpriteVerticalScrollerCamera::~SpriteVerticalScrollerCamera() {}

/** @brief Update function that offsets camera x position
 * 
 * Update function offsets camera y value according to target (main character). Uses std::clamp() to not pan off the level on top or bottom.
 * This creates the vertical scroller functionality of the camera.
*/
void SpriteVerticalScrollerCamera::Update() {
    y = target->getCenterY() - cameraHeight/2;
    y = std::clamp(y, 0, levelHeight - cameraHeight);
}