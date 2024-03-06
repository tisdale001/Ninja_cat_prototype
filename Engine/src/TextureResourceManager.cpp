#include "TextureResourceManager.hpp"
#include <iterator>
#include <iostream>

/** @brief Returns instance of TextureResourceManager: Singleton pattern
 * 
*/
TextureResourceManager& TextureResourceManager::instance() {

    static TextureResourceManager* instance = new TextureResourceManager();
    return *instance;
}

/** @brief Memory management
 * 
*/
void TextureResourceManager::shutDown() {
    for (auto it = mTextureMap.begin(); it != mTextureMap.end(); it++) {
        SDL_Surface* surf = it->first;
        SDL_DestroyTexture(it->second);
    }
    
    mTexture = nullptr;
}

/** @brief Constructor
 * 
*/
TextureResourceManager::TextureResourceManager(){
}

/** @brief Loads resource only once
 * 
 * Loads resource only once: mTexture.
*/
void TextureResourceManager::LoadResource(SDL_Surface* surface, SDL_Renderer* renderer){

    // Create iterator for resource map
    std::unordered_map<SDL_Surface*, SDL_Texture*>::const_iterator got = mTextureMap.find(surface);

    if (got == mTextureMap.end()) {
        // An SDL surface has not been created from the associated file...
        // It is created and inserted in the unordered map here
        SDL_Texture* text = SDL_CreateTextureFromSurface(renderer, surface);
        std::pair<SDL_Surface*, SDL_Texture*> newPair (surface, text);
        mTextureMap.insert(newPair);
        mTexture = text;
    } else {
        // An SDL surface has previously been created from the associated filename.
        // mSpriteSheet is set to the surface.
        mTexture = got->second;
    }
}

/** @brief Getter: returns mTexture
 * 
*/
SDL_Texture* TextureResourceManager::GetResource(SDL_Surface* surface){
    return mTexture;
}

/** @brief Removes a resource from Manager
 * 
 * Removes a resource from Manager by calling erase(surface) on mTextureMap.
*/
void TextureResourceManager::RemoveResource(SDL_Surface* surface) {

    mTextureMap.erase(surface);
}
