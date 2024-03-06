#pragma once

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

// #include "Rectangle.hpp"
#include "Sprite.hpp"

// Center camera on rectangle while staying within level bounds
class SpriteSideScrollerCamera {
    public:
        SpriteSideScrollerCamera(int camWidth, int camHeight, int levelWidth, int levelHeight, Sprite* sp);

        ~SpriteSideScrollerCamera();

        void Update();

        int x;
        int y;
        int cameraWidth;
        int cameraHeight;
        int levelWidth;
        int levelHeight;

    private:
        Sprite* target;
};