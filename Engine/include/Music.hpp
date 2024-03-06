#pragma once

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
    #include <SDL2/SDL_mixer.h>
#else // This works for Mac
    #include <SDL.h>
    #include <SDL_mixer.h>
#endif

#include <stdio.h>

class Music {
    public:
        Music();

        ~Music();

        void SetMusic(char* fileName);

        void PlayMusic();

        void PauseMusic();

        void UnPauseMusic();

        void StopMusic();

    private:
        Mix_Music *musicFile;
};