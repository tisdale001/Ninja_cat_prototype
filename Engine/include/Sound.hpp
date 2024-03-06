#pragma once

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
    #include <SDL2/SDL_mixer.h>
#else // This works for Mac
    #include <SDL.h>
    #include <SDL_mixer.h>
#endif

#include <stdio.h>

class Sound {
    public:
        Sound();

        ~Sound();

        void SetSound(char* fileName);

        void PlaySound();

    private:
        Mix_Chunk *soundFile;
};