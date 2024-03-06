#include "MusicResourceManager.hpp"
#include <iterator>
#include <iostream>

MusicResourceManager& MusicResourceManager::instance() {

    static MusicResourceManager* instance = new MusicResourceManager();
    return *instance;
}

void MusicResourceManager::shutDown() {
    std::cout << "==========" << "Commencing shutDown" << "==========" << std::endl;
    std::cout << "Freeing music in resource manager..." << std::endl;
    for (auto it = mMusicMap.begin(); it != mMusicMap.end(); it++) {
        char* mus = it->first;
        Mix_FreeMusic(it->second);
        std::cout << "Sound associated with char* '" << mus << "' has been destroyed" << std::endl;
    }

    // Mix_Quit();      // Should this be here?
    
    mMusic = nullptr;
}

MusicResourceManager::MusicResourceManager(){
}


void MusicResourceManager::LoadResource(char* fileName){

    // Create iterator for resource map
    std::unordered_map<char*, Mix_Music*>::const_iterator got = mMusicMap.find(fileName);

    if (got == mMusicMap.end()) {
        std::cout << "Music name is not in resource map...adding sound " << fileName << " to map" << std::endl;
        Mix_Music* music = Mix_LoadMUS(fileName);
        if(music == NULL)
        {
            printf("Failed to load music! SDL_mixer Error: %s\n", Mix_GetError());
        }
        std::pair<char*, Mix_Music*> newPair (fileName, music);
        mMusicMap.insert(newPair);
        mMusic = music;
    } else {
        // An SDL surface has previously been created from the associated filename.
        // mSpriteSheet is set to the surface.
        std::cout << "Music " << fileName << " located in resource map!" << std::endl;
        mMusic = got->second;
    }
}

Mix_Music* MusicResourceManager::GetResource(char* fileName){
    std::cout << "Retrieved saved copy of " << fileName << " from music resource map\n";
    return mMusic;
}