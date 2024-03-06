#include "Sound.hpp"
#include "SoundResourceManager.hpp"

/** @brief Constructor
 * 
*/
Sound::Sound() {
    
}

/** @brief Deconstructor
 * 
*/
Sound::~Sound() {
    Mix_Quit();
}

/** @brief Setter: sets soundFile according to param fileName
 * 
 * Setter method that uses the SoundResourceManager to set soundFile according to param fileName.
*/
void Sound::SetSound(char* fileName) {
	soundFile = SoundResourceManager::instance().LoadSoundResource(fileName);
}

/** @brief Play sound
 * 
 * Method plays sound by calling Mix_PlayChannel(). Performs null check.
*/
void Sound::PlaySound() {
    if(soundFile != NULL)
	{
        // Mix_Volume(-1, 128);
        Mix_PlayChannel( -1, soundFile, 0 );
	}
}