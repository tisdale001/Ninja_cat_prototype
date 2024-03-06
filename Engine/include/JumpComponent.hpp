#ifndef JUMPCOMPONENT_HPP
#define JUMPCOMPONENT_HPP

#include "GameObject.hpp"
#include <iostream>
#include <cstdlib>

class GameObject;

class JumpComponent {
    public:
        JumpComponent(int, int, float, int);
        ~JumpComponent();
        
        void Update(GameObject*);
        void changeInitialY(int delta);
        void EndJump();
        bool stillJumping();
        
        bool isJumping = false;
        float xVelocity;

    private:
        void Initiate(int, int);

        int x;
        int y;
        float height;
        int init_y;
        int init_x;
        float init_velocity;
        float up_velocity;
        float gravity;
        int distance;
        
        
        


};


#endif