#include "SoundResourceManager.hpp"
#include <iterator>
#include <iostream>
#include <string.h>

/** @brief Returns instance of SoundResourceManager: Singleton pattern
 * 
*/
SoundResourceManager& SoundResourceManager::instance() {

    static SoundResourceManager* instance = new SoundResourceManager();
    return *instance;
}

/** @brief Memory management
 * 
*/
void SoundResourceManager::shutDown() {
    for (auto it = mSoundMap.begin(); it != mSoundMap.end(); it++) {
        char* chunk = it->first;
        Mix_FreeChunk(it->second);
    }
    for (auto it = mMusicMap.begin(); it != mMusicMap.end(); it++) {
        char* music = it->first;
        Mix_FreeMusic(it->second);
    }

    Mix_Quit();
}

/** @brief Constructor
 * 
*/
SoundResourceManager::SoundResourceManager(){
    if(Mix_OpenAudio( 44100, MIX_DEFAULT_FORMAT, 2, 2048 ) < 0)
	{
		printf("SoundResourceManager could not initialize! SDL_mixer Error: %s\n", Mix_GetError());
	}
}

/** @brief Loads sound resource only once, returns resource
 * 
 * Loads resource only once. Error messages if load fails. Returns loaded resource or the resource if it already exists.
*/
Mix_Chunk* SoundResourceManager::LoadSoundResource(char* fileName){
    // Search for sound in saved resources
    for (auto i : mSoundMap) {
        if (strcmp(fileName, i.first) == 0) {
            // Return sound if it has been loaded
            return i.second;
        }
    }

    // Load resource if it was not found
    Mix_Chunk* sound = Mix_LoadWAV(fileName);
    if(sound == NULL)
    {
        printf("Failed to load sound! SDL_mixer Error: %s\n", Mix_GetError());
        return NULL;
    }
    char* fileNameCopy = new char[strlen(fileName) + 1];
    strcpy(fileNameCopy,fileName);
    mSoundMap[fileNameCopy] = sound;
    return sound;
}

/** @brief Loads music resource only once, returns resource
 * 
 * Loads resource only once. Error messages if load fails. Returns loaded resource or the resource if it already exists.
*/
Mix_Music* SoundResourceManager::LoadMusicResource(char* fileName){
    // Search for music in saved resources
    for (auto i : mMusicMap) {
        if (strcmp(fileName, i.first) == 0) {
            // Return music if it has been loaded
            return i.second;
        }
    }

    // Load resource if it was not found
    Mix_Music* music = Mix_LoadMUS(fileName);
    if(music == NULL)
    {
        printf("Failed to load music! SDL_mixer Error: %s\n", Mix_GetError());
        return NULL;
    }
    char* fileNameCopy = new char[strlen(fileName) + 1];
    strcpy(fileNameCopy,fileName);
    mMusicMap[fileNameCopy] = music;
    return music;
}