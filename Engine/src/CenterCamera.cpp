#include "CenterCamera.hpp"
#include <algorithm>

CenterCamera::CenterCamera(int camWidth, int camHeight, int lvlWidth, int lvlHeight, RectangleComponent* r):
    cameraWidth(camWidth),
    cameraHeight(camHeight),
    levelWidth(lvlWidth),
    levelHeight(lvlHeight),
    target(r) {
        x = std::clamp(r->getCenterX() - cameraWidth/2, 0, levelWidth - cameraWidth);
        y = std::clamp(r->getCenterY() - cameraHeight/2, 0, levelHeight - cameraHeight);
    }

CenterCamera::~CenterCamera() {}

void CenterCamera::Update() {
    x = target->getCenterX() - cameraWidth/2;
    y = target->getCenterY() - cameraHeight/2;
    x = std::clamp(x, 0, levelWidth - cameraWidth);
    y = std::clamp(y, 0, levelHeight - cameraWidth);
}