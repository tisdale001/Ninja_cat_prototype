#pragma once

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

#include "ICamera.hpp"
#include "Rectangle.hpp"

// Center camera on rectangle while staying within level bounds
class CenterCamera : public ICamera {
    public:
        CenterCamera(int camWidth, int camHeight, int levelWidth, int levelHeight, RectangleComponent* r);

        ~CenterCamera();

        void Update();

        int cameraWidth;
        int cameraHeight;
        int levelWidth;
        int levelHeight;

    private:
        RectangleComponent* target;
};
