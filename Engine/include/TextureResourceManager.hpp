#ifndef TEXTURE_RESOURCE_MANAGER_HPP
#define TEXTURE_RESOURCE_MANAGER_HPP

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

// I recommend a map for filling in the resource manager
#include <unordered_map>
#include <string>

class TextureResourceManager{
public:

    static TextureResourceManager& instance();

    void shutDown();
    
    void LoadResource(SDL_Surface* surface, SDL_Renderer* renderer);
    
    SDL_Texture* GetResource(SDL_Surface* surface);

    void RemoveResource(SDL_Surface* surface);

private:
    // Private constructor
    TextureResourceManager();

    std::unordered_map<SDL_Surface*, SDL_Texture*> mTextureMap;

    SDL_Texture* mTexture;
};


#endif