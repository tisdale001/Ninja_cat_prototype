#include <iostream>

#include "Rectangle.hpp"

/** @brief Constructor: Transform component as parameter
 * 
 * Constructor that takes in a pointer to pre-existing Transform component
*/
RectangleComponent::RectangleComponent(Transform* _transform) {
    transform = _transform;
}

/** @brief Deconstructor
 * 
*/
RectangleComponent::~RectangleComponent() {}

/** @brief Empty method. Not needed.*/
void RectangleComponent::Update() {}

/** @brief Renders rectangle according to camera offset.
 * 
 * Renders rectangle according to camera offset according to params camOffsetX, camOffsetY
*/
void RectangleComponent::Render(std::uintptr_t rendererAddress, int camOffsetX, int camOffsetY) {
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    SDL_SetRenderDrawColor(renderer, redValue, greenValue, blueValue, alphaValue);
    SDL_Rect fillRect = {transform->xPos - camOffsetX, transform->yPos - camOffsetY, width, height};
    SDL_RenderFillRect(renderer, &fillRect);
}

/** @brief Setter: sets width and height
 * 
 * Setter method: sets width and height
*/
void RectangleComponent::setDimensions(int w, int h) {
    width = w;
    height = h;
}

/** @brief Setter: sets color values
 * 
 * Setter method: sets color values
*/
void RectangleComponent::setColor(int r, int g, int b, int a) {
    redValue = r;
    greenValue = g;
    blueValue = b;
    alphaValue = a;
}

/** @brief Getter: returns width
 * 
 * Getter method that returns width
*/
int RectangleComponent::getWidth() {
    return width;
}

/** @brief Getter: returns height
 * 
 * Getter method that returns height
*/
int RectangleComponent::getHeight() {
    return height;
}

/** @brief Getter: returns x position
 * 
 * Getter method: returns x position (xPos) from Transform component.
*/
int RectangleComponent::getX() {
    return transform->xPos;
}

/** @brief Getter: return y position
 * 
 * Getter method: returns y position (yPos) from Transform component.
*/
int RectangleComponent::getY() {
    return transform->yPos;
}

/** @brief Getter: returns x coordinate of center of rectangle.
 * 
 * Getter method: returns x coordinate of center of rectangle based on Transform component's xPos.
*/
int RectangleComponent::getCenterX() {
    return transform->xPos + width / 2;
}

/** @brief Getter: returns y coordinate of center of rectangle.
 * 
 * Getter method: returns y coordinate of center of rectangle based on Transform component's yPos.
*/
int RectangleComponent::getCenterY() {
    return transform->yPos + height / 2;
}

/** @brief Collision check for two rectangle components
 * 
 *  Return if this rectangle overlaps with rectangle r2
*/
bool RectangleComponent::checkCollision(RectangleComponent* r2) {
    return getX() < r2->getX() + r2->getWidth() &&
            getX() + getWidth() > r2->getX() &&
            getY() < r2->getY() + r2->getHeight() &&
            getHeight() + getY() > r2->getY();
}