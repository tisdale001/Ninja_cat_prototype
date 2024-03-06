#pragma once

#include "ICamera.hpp"

// Center camera on rectangle while staying within level bounds
class StaticCamera : public ICamera {
    public:
        StaticCamera();

        ~StaticCamera();

        void Update();
};
