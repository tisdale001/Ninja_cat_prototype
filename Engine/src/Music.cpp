#include "Music.hpp"
#include "SoundResourceManager.hpp"
#include <iostream>


/** @brief Constructor
 * 
*/
Music::Music() {
    
}

/** @brief Deconstructor
 * 
*/
Music::~Music() {

}

/** @brief Setter: sets musicFile with param fileName
 * 
 * Setter method that uses the SoundResourceManager to set music for musicFile.
*/
void Music::SetMusic(char* fileName) {
	musicFile = SoundResourceManager::instance().LoadMusicResource(fileName);
}

/** @brief Play music
 * 
 * Method plays music contained in musicFile. Performs null check.
*/
void Music::PlayMusic() {
	// std::cout << "HERE-1" << std::endl;
    if(musicFile != NULL)
	{
		Mix_VolumeMusic(50);
        Mix_PlayMusic(musicFile, -1);
	}
}

/** @brief Pause music
 * 
 * Method pauses music contained in musicFile. Performs null check.
*/
void Music::PauseMusic() {
    if(musicFile != NULL)
	{
        Mix_PauseMusic();
	}
}

/** @brief Unpause music
 * 
 * Method unpauses music contained in musicFile. Performs null check.
*/
void Music::UnPauseMusic() {
    if(musicFile != NULL)
	{
        Mix_ResumeMusic();
	}
}

/** @brief Stop music
 * 
 * Method stops music conatined in musicFile. Performs null check.
*/
void Music::StopMusic() {
    if(musicFile != NULL)
	{
        Mix_HaltMusic();
	}
}