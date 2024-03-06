#include "SurfaceResourceManager.hpp"
#include <iterator>
#include <iostream>

/** @brief Returns instance of SurfaceResourceManager: Singleton pattern
 * 
*/
SurfaceResourceManager& SurfaceResourceManager::instance() {

    static SurfaceResourceManager* instance = new SurfaceResourceManager();
    return *instance;
}

/** @brief Memory management
 * 
*/
void SurfaceResourceManager::shutDown() {
    for (auto it = mSurfaceMap.begin(); it != mSurfaceMap.end(); it++) {
        std::string filename = it->first;
        SDL_FreeSurface(it->second);
    }
    
    mSpriteSheet = nullptr;
}

/** @brief Constructor
 * 
*/
SurfaceResourceManager::SurfaceResourceManager(){
}

/** @brief Loads resource only once from param image_filename.
 * 
 * Loads resource onlly once to mSpriteSheet.
*/
void SurfaceResourceManager::LoadResource(std::string image_filename){

    // Create iterator for resource map
    std::unordered_map<std::string, SDL_Surface*>::const_iterator got = mSurfaceMap.find(image_filename);

    if (got == mSurfaceMap.end()) {
        // An SDL surface has not been created from the associated file...
        // It is created and inserted in the unordered map here
        // SDL_Surface* newImageFilename = SDL_LoadBMP(image_filename.c_str());
        SDL_Surface* newImageFilename = IMG_Load(image_filename.c_str()); // const char *file
        std::pair<std::string, SDL_Surface*> newPair (image_filename, newImageFilename);
        mSurfaceMap.insert(newPair);
        mSpriteSheet = newImageFilename;
    } else {
        // An SDL surface has previously been created from the associated filename.
        // mSpriteSheet is set to the surface.
        mSpriteSheet = got->second;
    }
}

/** @brief Getter: returns mSpriteSheet
 * 
*/
SDL_Surface* SurfaceResourceManager::GetResource(std::string image_filename){
    return mSpriteSheet;
}

/** @brief Removes resource from Manager
 * 
 * Removes resource, param image_filename, from manager by calling erase() on mSurfaceMap.
*/
void SurfaceResourceManager::RemoveResource(std::string image_filename) {

    mSurfaceMap.erase(image_filename);
}

