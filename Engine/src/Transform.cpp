#include "Transform.hpp"

/** @brief Constructor
 * 
*/
Transform::Transform() {}

/** @brief Deconstructor
 * 
*/
Transform::~Transform() {}

/** @brief Empty method: not used*/
void Transform::Update() {}

// void Transform::Render(SDL_Renderer* renderer) {}
/** @brief Setter: sets x and y positions
 * 
 * Setter method that sets xPos and yPos according to parameters x and y
*/
void Transform::setPosition(int x, int y) {
    xPos = x;
    yPos = y;
}