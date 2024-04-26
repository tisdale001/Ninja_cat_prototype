#pragma once

#include <iostream>
#include <string>
#include <memory>
#include <sstream>
#include <fstream>
#include <vector>
#include <cstdint>

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

class GameObject;

enum Key {
    W_PRESSED = 0,
    S_PRESSED = 1,
    UP_PRESSED = 2,
    DOWN_PRESSED = 3,
    A_PRESSED = 4,
    D_PRESSED = 5,
    LEFT_PRESSED = 6,
    RIGHT_PRESSED = 7,
    SPACE_PRESSED = 8,
    ESCAPE_PRESSED = 9,
    QUIT_EVENT = 10,
    W_TAPPED = 11,
    S_TAPPED = 12,
    UP_TAPPED = 13,
    DOWN_TAPPED = 14,
    A_TAPPED = 15,
    D_TAPPED = 16,
    LEFT_TAPPED = 17,
    RIGHT_TAPPED = 18,
    SPACE_TAPPED = 19,
    ESCAPE_TAPPED = 20,
    J_PRESSED = 21,
    J_TAPPED = 22,
    H_PRESSED = 23,
    H_TAPPED = 24,
    K_PRESSED = 25,
    K_TAPPED = 26,
    Z_PRESSED = 27,
    X_PRESSED = 28,
    TOTAL_KEYS
};

// Purpose:
class SDLGraphicsProgram {
public:
    // Constructor
    SDLGraphicsProgram(int w, int h);
    // Destructor
    ~SDLGraphicsProgram();
    // Clears the screen
    void clear(Uint8 r, Uint8 g, Uint8 b, Uint8 a);
    // Flips to new buffer
    void flip();
    // Delay rendering
    void delay(int milliseconds);
    // Read and return state of input keys
    std::vector<bool> getInput();
    // Set color of gRenderer
    void setRenderColor(Uint8 r, Uint8 g, Uint8 b, Uint8 a);
    // Get Pointer to Window
    SDL_Window* getSDLWindow();
    // Get Pointer to Renderer
    std::uintptr_t getSDLRenderer();
    // std::shared_ptr<SDL_Renderer> getSDLRenderer();
    // Draw a simple filled rectangle
    void DrawRectangle(int x, int y, int w, int h);
    // Set title of SDL window
    void setTitle(const std::string &title);
    // Add GameObject to gameObjects vector for auto update and render
    void addGameObject(GameObject* obj);
    // Render each GameObject
    void Render();
    // Get time in milliseconds since SDL library initialization
    Uint32 getTimeMS();
    // Return status of each input in Keys at frame
    std::vector<bool>& getInputAtFrame(int frame);
    // Set to renderer to default blend mode - no transparency
    void setBlendModeNone();
    // Set to blend mode alpha - transparency
    void setBlendModeAlpha();

private:
    // Screen dimension constants
    int screenHeight;
    int screenWidth;
    // The window we'll be rendering to
    SDL_Window* gWindow;
    // Our renderer
    SDL_Renderer* gRenderer;
    // std::shared_ptr<SDL_Renderer> gRenderer;
    // Read events in getInput SDL_PollEvent
    SDL_Event event;
    // Store state of all inputs
    const Uint8* keys;
    // Store state of game inputs
    std::vector<bool> inputs = std::vector<bool>(TOTAL_KEYS, false);
    std::vector<std::vector<bool>> inputRecord;
    std::vector<GameObject*> gameObjects;
};
