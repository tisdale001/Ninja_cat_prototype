#include "StaticCamera.hpp"

/** @brief Constructor
 * 
 * A static camera has no parameters and sets the camera offset to 0, 0 by default  
 * 
*/
StaticCamera::StaticCamera() {
        x = 0;
        y = 0;
}
/** @brief Deconstructor
 * 
*/
StaticCamera::~StaticCamera() {}

/** @brief Update function that offsets camera x position
 * 
 * Update function is not used in a static camera
 * 
*/
void StaticCamera::Update() {}