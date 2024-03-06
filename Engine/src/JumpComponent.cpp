#include "JumpComponent.hpp"

JumpComponent::JumpComponent(int _height, int _total_distance, float _xVelocity, int _gravity_factor){
    height = _height; // start with -400
    distance = _total_distance / 2; // start with 1000
    xVelocity = _xVelocity;
    gravity = (_gravity_factor * height) / (distance * distance);
    up_velocity = (2 * height) / distance;
}
JumpComponent::~JumpComponent(){}

void JumpComponent::Initiate(int x_, int y_){
    init_x = x_;
    init_y = y_;
    x = 0;
    y = y_;
    init_velocity = std::abs(xVelocity);

}

void JumpComponent::Update(GameObject* obj){
    if (obj->mInitiateJump) {
        isJumping = true;
        Initiate(obj->mTransform->xPos, obj->mTransform->yPos);
        obj->mInitiateJump = false;
    }
    if (!isJumping) {
        return;
    }
    x += init_velocity;
    y = 0.5 * gravity * x * x + up_velocity * x + init_y;
    //std::cout << y << std::endl;
    if ((height <= 0 && y > init_y) || (height > 0 && y < init_y)) {
        // std::cout << "isJumping = false" << std::endl;
        y = init_y;
        isJumping = false;
    }
    // only update the y value, this allows for controlled jump
    obj->yVel = y - obj->mTransform->yPos;
}

void JumpComponent::changeInitialY(int delta) {
    if (isJumping) {
        init_y += delta;
    }
}

void JumpComponent::EndJump() {
    isJumping = false;
}

bool JumpComponent::stillJumping() {
    return isJumping;
}
