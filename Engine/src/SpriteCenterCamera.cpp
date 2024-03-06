#include "SpriteCenterCamera.hpp"
#include <algorithm>

/** @brief Constructor
 * 
*/
SpriteCenterCamera::SpriteCenterCamera(int camWidth, int camHeight, int lvlWidth, int lvlHeight, Sprite* sp):
    cameraWidth(camWidth),
    cameraHeight(camHeight),
    levelWidth(lvlWidth),
    levelHeight(lvlHeight),
    target(sp) {
        x = std::clamp(sp->getCenterX() - cameraWidth/2, 0, levelWidth - cameraWidth);
        y = std::clamp(sp->getCenterY() - cameraHeight/2, 0, levelHeight - cameraHeight);
    }

/** @brief Deconstructor
 * 
*/
SpriteCenterCamera::~SpriteCenterCamera() {}

/** @brief Updates camera position, centering on target while staying within level bounds
 * 
*/
void SpriteCenterCamera::Update() {
    x = target->getCenterX() - cameraWidth/2;
    y = target->getCenterY() - cameraHeight/2;
    x = std::clamp(x, 0, levelWidth - cameraWidth);
    y = std::clamp(y, 0, levelHeight - cameraWidth);
}