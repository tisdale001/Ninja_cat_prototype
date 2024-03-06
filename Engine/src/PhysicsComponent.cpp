#include "PhysicsComponent.hpp"
#include "GameObject.hpp"

/** @brief Constructor
 * 
 * Simple Constructor for PhysicsComponent
*/
PhysicsComponent::PhysicsComponent() {}

/** @brief Deconstructor
 * 
*/
PhysicsComponent::~PhysicsComponent() {}

/** @brief Updates x position of GameObject
 * 
 * Takes in GameObject as parameter. Changes xPos of TransformComponent within GameObject by adding the x velocity (xVel) of GameObject.
*/
void PhysicsComponent::UpdateX(GameObject* o) {
    o->mTransform->xPos += o->xVel;
    
    // o->xVel = 0;
}

/** @brief Updates y position of GameObject
 * 
 * Takes in GameObject as parameter. Changes yPos of TransformComponent within GameObject by adding the y velocity (yVel) of GameObject.
*/
void PhysicsComponent::UpdateY(GameObject* o) {
    o->mTransform->yPos += o->yVel;
    // o->yVel = 0;
}