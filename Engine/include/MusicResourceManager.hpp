#ifndef MUSIC_RESOURCE_MANAGER_HPP
#define MUSIC_RESOURCE_MANAGER_HPP

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
    #include <SDL2/SDL_mixer.h>
#else // This works for Mac
    #include <SDL.h>
    #include <SDL_mixer.h>
#endif

#include <unordered_map>

class MusicResourceManager{
    public:

        static MusicResourceManager& instance();

        void shutDown();
        
        // TODO: Refactor to be a static function
        void LoadResource(char* fileName);
        // TODO: Refactor to be a static function
        Mix_Music* GetResource(char* fileName);

    private:
        // Private constructor
        MusicResourceManager();

        std::unordered_map<char*, Mix_Music*> mMusicMap;

        Mix_Music* mMusic;
};


#endif