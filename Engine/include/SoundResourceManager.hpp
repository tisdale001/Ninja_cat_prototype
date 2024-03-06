#ifndef SOUND_RESOURCE_MANAGER_HPP
#define SOUND_RESOURCE_MANAGER_HPP

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
    #include <SDL2/SDL_mixer.h>
#else // This works for Mac
    #include <SDL.h>
    #include <SDL_mixer.h>
#endif

#include <unordered_map>

class SoundResourceManager{
    public:

        static SoundResourceManager& instance();

        void shutDown();
        
        Mix_Chunk* LoadSoundResource(char* fileName);
        
        Mix_Music* LoadMusicResource(char* fileName);

    private:
        // Private constructor
        SoundResourceManager();

        std::unordered_map<char*, Mix_Chunk*> mSoundMap;
        std::unordered_map<char*, Mix_Music*> mMusicMap;
};


#endif