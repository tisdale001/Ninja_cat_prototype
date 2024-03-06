#pragma once

class Transform {
    public:
        int xPos = 0;
        int yPos = 0;

        Transform();

        ~Transform();

        void Update();

        // void Render(SDL_Renderer* renderer);

        void setPosition(int x, int y);
};
