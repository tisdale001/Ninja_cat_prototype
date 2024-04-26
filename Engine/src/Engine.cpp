#include "Engine.hpp"
#include "GameObject.hpp"

// struct SDL_RendererDeleter {
//     inline void operator()(SDL_Renderer* renderer) {
//         SDL_DestroyRenderer(renderer);
//     }
// };

// Initialization function
// Returns a true or false value based on successful completion of setup.
// Takes in dimensions of window.

/** @brief Constructor: sets up initial graphics window
 * 
 * Constructor. Takes screen width and height as parameters. Creates graphcis window and renderer and initializes "keys" to reveive keyboard input.
*/
SDLGraphicsProgram::SDLGraphicsProgram(int w, int h):screenWidth(w),screenHeight(h) {
	// Initialization flag
	bool success = true;
	// String to hold any errors that occur.
	std::stringstream errorStream;
	// The window we'll be rendering to
	gWindow = NULL;
	// Render flag

	// Initialize SDL
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		errorStream << "SDL could not initialize! SDL Error: " << SDL_GetError() << "\n";
		success = false;
	}
	else {
	    //Create window
    	gWindow = SDL_CreateWindow("Game", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, screenWidth, screenHeight, SDL_WINDOW_SHOWN);

        // Check if Window did not create.
        if (gWindow == NULL) {
			errorStream << "Window could not be created! SDL Error: " << SDL_GetError() << "\n";
			success = false;
		}

		//Create a Renderer to draw on
        gRenderer = SDL_CreateRenderer(gWindow, -1, SDL_RENDERER_ACCELERATED);
        // gRenderer = std::make_shared<SDL_Renderer>(renderer);
        // SDL_Renderer* renderer = SDL_CreateRenderer(gWindow, -1, SDL_RENDERER_ACCELERATED);
        // gRenderer = std::shared_ptr<SDL_Renderer>(SDL_CreateRenderer(gWindow, -1, SDL_RENDERER_ACCELERATED), SDL_RendererDeleter{});
    //     auto window = std::unique_ptr<SDL_Window, std::function<void(SDL_Window *)>>(
    //         SDL_CreateWindow("Test", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, kWindowWidth, kWindowHeight, 0),
    //         SDL_DestroyWindow
    // );
        // Check if Renderer did not create.
        if (gRenderer == NULL) {
            errorStream << "Renderer could not be created! SDL Error: " << SDL_GetError() << "\n";
            success = false;
        }
  	}

    // If initialization did not work, then print out a list of errors in the constructor.
    if (!success) {
        errorStream << "SDLGraphicsProgram::SDLGraphicsProgram - Failed to initialize!\n";
        std::string errors=errorStream.str();
        SDL_Log("%s\n",errors.c_str());
    } else {
        SDL_Log("SDLGraphicsProgram::SDLGraphicsProgram - No SDL, GLAD, or OpenGL, errors detected during initialization\n\n");
    }
    SDL_StartTextInput();
    keys = SDL_GetKeyboardState(NULL);
}


// Proper shutdown of SDL and destroy initialized objects
/** @brief Deconstructor
 * 
 * Deconstructor: destroys window and renderer and calls SDL_Quit()
*/
SDLGraphicsProgram::~SDLGraphicsProgram() {
    //Destroy window
	SDL_DestroyWindow(gWindow);
	SDL_DestroyRenderer(gRenderer);
	// Point gWindow to NULL to ensure it points to nothing.
	gWindow = NULL;
	//Quit SDL subsystems
	SDL_Quit();
}


// Clears the screen
/** @brief Clears the screen using rgba values as input
 * 
 * Clears the screen according to rgba values. Calls to SDL_SetRenderDrawColor() and SDL_RenderClear().
*/
void SDLGraphicsProgram::clear(Uint8 r, Uint8 g, Uint8 b, Uint8 a) {
    SDL_SetRenderDrawColor(gRenderer, r, g, b, a);
    SDL_RenderClear(gRenderer);
}


// The flip function gets called once per loop
// It swaps out the previous frame in a double-buffering system
/** @brief flip() function swaps out the previous frame in double-buffering system
 * 
*/
void SDLGraphicsProgram::flip() {
    SDL_RenderPresent(gRenderer);
}

/** @brief Method calls SDL_Delay. Takes in milliseconds as parameter.
 * 
 * Method creates a delay in terms of milliseconds. Used to create a pause for frame-capping.
*/
void SDLGraphicsProgram::delay(int milliseconds) {
    SDL_Delay(milliseconds);
}

/** @brief Getter: returns pointer gRenderer
 * 
 * Getter method that returns pointer gRenderer
*/
std::uintptr_t SDLGraphicsProgram::getSDLRenderer() {
    return reinterpret_cast<std::uintptr_t>(gRenderer);
}


// Read and return state of input keys
/** @brief Method records and returns keyboard state as member variable "inputs"
 * 
 * Method records and then returns keyboard state as member variable "inputs", which is a vector of acceptable keyboard entries according to enum "Key".
*/
std::vector<bool> SDLGraphicsProgram::getInput() {
    while (SDL_PollEvent(&event) != 0) {
        if (event.type == SDL_QUIT) {
            inputs[QUIT_EVENT] = true;
        }
    }
    // "Tapped" means was pressed down just now, and was not pressed down before
    inputs[W_TAPPED] = keys[SDL_SCANCODE_W] && !inputs[W_PRESSED];
    inputs[S_TAPPED] = keys[SDL_SCANCODE_S] && !inputs[S_PRESSED];
    inputs[A_TAPPED] = keys[SDL_SCANCODE_A] && !inputs[A_PRESSED];
    inputs[D_TAPPED] = keys[SDL_SCANCODE_D] && !inputs[D_PRESSED];
    inputs[H_TAPPED] = keys[SDL_SCANCODE_H] && !inputs[H_PRESSED];
    inputs[K_TAPPED] = keys[SDL_SCANCODE_K] && !inputs[K_PRESSED];
    inputs[UP_TAPPED] = keys[SDL_SCANCODE_UP] && !inputs[UP_PRESSED];
    inputs[DOWN_TAPPED] = keys[SDL_SCANCODE_DOWN] && !inputs[DOWN_PRESSED];
    inputs[LEFT_TAPPED] = keys[SDL_SCANCODE_LEFT] && !inputs[LEFT_PRESSED];
    inputs[RIGHT_TAPPED] = keys[SDL_SCANCODE_RIGHT] && !inputs[RIGHT_PRESSED];
    inputs[SPACE_TAPPED] = keys[SDL_SCANCODE_SPACE] && !inputs[SPACE_PRESSED];
    inputs[J_TAPPED] = keys[SDL_SCANCODE_J] && !inputs[J_PRESSED];
    inputs[ESCAPE_TAPPED] = keys[SDL_SCANCODE_ESCAPE] && !inputs[ESCAPE_PRESSED];
    // "Pressed" means is currently being pressed down
    inputs[W_PRESSED] = keys[SDL_SCANCODE_W];
    inputs[S_PRESSED] = keys[SDL_SCANCODE_S];
    inputs[A_PRESSED] = keys[SDL_SCANCODE_A];
    inputs[D_PRESSED] = keys[SDL_SCANCODE_D];
    inputs[H_PRESSED] = keys[SDL_SCANCODE_H];
    inputs[K_PRESSED] = keys[SDL_SCANCODE_K];
    inputs[X_PRESSED] = keys[SDL_SCANCODE_X];
    inputs[UP_PRESSED] = keys[SDL_SCANCODE_UP];
    inputs[DOWN_PRESSED] = keys[SDL_SCANCODE_DOWN];
    inputs[LEFT_PRESSED] = keys[SDL_SCANCODE_LEFT];
    inputs[RIGHT_PRESSED] = keys[SDL_SCANCODE_RIGHT];
    inputs[SPACE_PRESSED] = keys[SDL_SCANCODE_SPACE];
    inputs[J_PRESSED] = keys[SDL_SCANCODE_J];
    inputs[Z_PRESSED] = keys[SDL_SCANCODE_Z];
    inputs[ESCAPE_PRESSED] = keys[SDL_SCANCODE_ESCAPE];
    // Save inputs for replay
    inputRecord.push_back(inputs);
    // Return inputs
    return inputs;
}


// Get Pointer to Window
/** @brief Getter: returns pointer gWindow
 * 
 * Getter method that returns pointer to SDLWindow (gWindow).
*/
SDL_Window* SDLGraphicsProgram::getSDLWindow() {
  return gWindow;
}


// Okay, render our rectangles!
/** @brief Creates rectangle according to dimensions as inputs on gRenderer
 * 
 * Creates a rectangle according to x/y position, witdth and height as inputs on gRenderer
*/
void SDLGraphicsProgram::DrawRectangle(int x, int y, int w, int h) {
    SDL_Rect fillRect = {x,y,w,h};
    SDL_RenderFillRect(gRenderer, &fillRect);
}

/** @brief Setter: sets title of window
 * 
 * Setter method: sets title of SDLWindow
*/
void SDLGraphicsProgram::setTitle(const std::string &title) {
    SDL_SetWindowTitle(getSDLWindow(), title.c_str());
}

/** @brief Setter: sets render draw color by rgba input params
 * 
 * Setter method: sets render draw color according to rgba inputs
*/
void SDLGraphicsProgram::setRenderColor(Uint8 r, Uint8 g, Uint8 b, Uint8 a) {
    SDL_SetRenderDrawColor(gRenderer, r, g, b, a);
}

/** @brief Adds GameObject to gameObjects vector
 * 
*/
void SDLGraphicsProgram::addGameObject(GameObject* obj) {
    gameObjects.push_back(obj);
}

/** @brief Calls Render() for all GameObjects in gameObjects vector
 * 
 * Iterates through all GameObjects and calls Render() on each.
*/
void SDLGraphicsProgram::Render() {
    for (auto gameObject : gameObjects) {
        gameObject->Render(getSDLRenderer());
    }
}

/** @brief Getter: get time
 * 
 * Getter method that gets time in milliseconds by calling SDL_GetTicks().
*/
Uint32 SDLGraphicsProgram::getTimeMS() {
    return SDL_GetTicks();
}

/** @brief Getter: gets vector of booleans for param frame
 * 
 * Getter method that returns boolean vector that represents the input associated to frame number. Gets vector from inputRecord.
*/
std::vector<bool>& SDLGraphicsProgram::getInputAtFrame(int frame) {
    return inputRecord.at(frame);
}

/** @brief Sets renderer to default blend mode
 * Set renderer to SDL_BLENDMODE_NONE (no transparency)
*/
void SDLGraphicsProgram::setBlendModeNone() {
    SDL_SetRenderDrawBlendMode(gRenderer, SDL_BLENDMODE_NONE);
}

/** @brief Sets renderer to alpha blend mode
 * Set renderer to SDL_BLENDMODE_BLEND (transparency supported)
*/
void SDLGraphicsProgram::setBlendModeAlpha() {
    SDL_SetRenderDrawBlendMode(gRenderer, SDL_BLENDMODE_BLEND);
}