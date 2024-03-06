#pragma once

// Center camera on rectangle while staying within level bounds
class ICamera {
    public:
        virtual void Update() = 0;

        int GetXOffset() {
            return x;
        }
        
        int GetYOffset() {
            return y;
        }

        int x;
        int y;
};