// #include "Engine.hpp"
// #include "Transform.hpp"
// #include "Rectangle.hpp"
// #include "PhysicsComponent.hpp"
// #include "GameObject.hpp"
// #include <iostream>
// #include "CenterCamera.hpp"
// #include "SideScrollerCamera.hpp"
// #include "LevelReader.hpp"
// #include "Sound.hpp"
// #include "Music.hpp"

// // TestGame to try out engine functions and see what needs to be exposed through pybind
// int main(int argc, char** argv) {
//     // So far, the tilemap component supports the player being smaller or bigger than the tile size
//     // int rows = 20;
//     // int cols = 20;
//     // int tileSize = 50;
//     // auto tileMapComponent = new TileMapComponent(rows, cols, tileSize);
//     int screenWidth = 800;
//     int screenHeight = 800;
// 	SDLGraphicsProgram e(screenWidth, screenHeight);
//     auto tileMapComponent = new TileMapComponent("Assets/Levels/MarioTiles/nish-test2.lvl");
//     tileMapComponent->loadTileset(std::string("Assets/tilesets/mario-like-tileset-32x32.png"), e.getSDLRenderer());

//     int levelWidth = tileMapComponent->getCols() * tileMapComponent->getSize();
//     int levelHeight = tileMapComponent->getRows() * tileMapComponent->getSize();
//     auto inputs = e.getInput();

//     auto playerTransform = new Transform();
//     playerTransform->setPosition(levelWidth/2, levelHeight/2); // Note: I kept constructor args in a separate function to
//     // make an addComponent template function simpler, might go back on this

//     auto rect = new RectangleComponent(playerTransform);
//     rect->setDimensions(15, 15);

//     auto physicsComponent = new PhysicsComponent();

//     GameObject player(e.getSDLRenderer());
//     player.addTransformComponent(playerTransform);
//     player.addRectangleComponent(rect);
//     player.addPhysicsComponent(physicsComponent);
//     GameObject tileMap(e.getSDLRenderer());
//     tileMap.addTileMapComponent(tileMapComponent);
//     SideScrollerCamera camera(screenWidth, screenHeight, levelWidth, levelHeight, *rect);
//     // CenterCamera camera(screenWidth, screenHeight, levelWidth, levelHeight, *rect);
//     // Creating/adding/updating game objects could be in a GameWorld or level class, or we can let the game logic handle it

//     // Sounds
//     const std::string high_note_string = "high.wav";
//     const int high_note_length = high_note_string.length();
//     char* high_note_cstring = new char[high_note_length + 1];
//     strcpy(high_note_cstring, high_note_string.c_str());

//     auto soundEffect = Sound();
//     soundEffect.SetSound(high_note_cstring);
//     // soundEffect.PlaySound();

//     const std::string beat_string = "beat.wav";
//     const int beat_length = beat_string.length();
//     char* beat_cstring = new char[beat_length + 1];
//     strcpy(beat_cstring, beat_string.c_str());

//     auto musicPlayer = Music();
//     musicPlayer.SetMusic(beat_cstring);
//     // musicPlayer.PlayMusic();

//     size_t frame_count = 0;
//     Uint32 startTime = SDL_GetTicks();
//     int targetFPS = 60;
//     size_t maxTicksPerFrame = 1000 / targetFPS; // 16.66ms per frame
//     Uint32 frameStartTime = 0;
//     Uint32 timeElapsed = 0;
//     size_t frameTicks = 0;
//     float fps = 0.0f;
//     int speed = 3;
//     bool isJumping = false;
//     // int decY = -2;
//     int initialJumpY = -22;
//     int jumpY = initialJumpY; // TODO: We might want the state pattern from gamepatterns book to cleanup logic
//     while (!inputs[QUIT_EVENT]) { // Note: We can add more keys if we want more than WASD or key up/key release events
//         frameStartTime = SDL_GetTicks();
//         timeElapsed = 0;

//         inputs = e.getInput();
//         int oldX = rect->getX();
//         int oldY = rect->getY();
//         // Apply gravity if not on ground
//         // TODO: Should gravity be a c++ component or implemented in game? Same for something like jump
//         // Note: We might want a concept of timesteps somewhere for smoother FPS independent physics
//         player.xVel = 0;
//         // player.yVel = 0;
//         // if (inputs[W_PRESSED]) {
//         //     player.yVel -= speed;
//         // }

//         if (tileMapComponent->isOnGround(&player)) {
//             player.yVel = 0;
//             jumpY = initialJumpY;
//         }
//         if (inputs[W_PRESSED] && tileMapComponent->isOnGround(&player)) { // Only let the player jump on ground
//             if (!isJumping) {
//                 // soundEffect.PlaySound();
//             }
//             isJumping = true;
//         }

//         if (isJumping) {
//             player.yVel += jumpY;
//             isJumping = false;
//         }
//         else if (!tileMapComponent->isOnGround(&player)) {
//             player.yVel += 2;
//             isJumping = false;
//         }

//         if (inputs[S_PRESSED]) {
//             player.yVel += speed;
//         }
//         if (inputs[A_PRESSED]) {
//             player.xVel -= speed;
//         }
//         if (inputs[D_PRESSED]) {
//             player.xVel += speed;
//         }
//         if (inputs[DOWN_PRESSED]) {
//             std::cout << "Current Position: " << playerTransform->xPos << " " << playerTransform->yPos << std::endl;
//             // std::cout << "isJumping" << isJumping << std::endl;
//             std::cout << "CamX: " << camera.x << " CamY: " << camera.y << std::endl;
//         }


//         // Update X position, then Y position to handle moving into corners
//         physicsComponent->UpdateX(&player);
//         // Currently, this returns the first tile collided. We should consider if we want to return a list of all tiles collided
//         // For now, we can use tileAtXY to get the tile at a specific pixel, such as 1 pixel above or below player bounds (This could also be a tilemapcomponent function tileBelow, tileAbove, etc)
//         auto c = tileMapComponent->checkCollision(&player);
//         if (c.isColliding) {
//             // std::cout << "CollisionX" << std::endl;
//             if (player.xVel < 0) {
//                 int newX = (c.col + 1) * tileMapComponent->getSize();
//                 playerTransform->setPosition(newX, oldY);
//             }
//             if (player.xVel > 0) {
//                 int newX = c.col * tileMapComponent->getSize() - rect->getWidth();
//                 playerTransform->setPosition(newX, oldY);
//             }
//         }

//         oldX = rect->getX();
//         oldY = rect->getY();
//         physicsComponent->UpdateY(&player);
//         c = tileMapComponent->checkCollision(&player);
//         if (c.isColliding) {
//             // std::cout << "CollisionY" << std::endl;
//             if (player.yVel < 0) {
//                 int newY = (c.row + 1) * tileMapComponent->getSize();
//                 playerTransform->setPosition(oldX, newY);
//             }
//             if (player.yVel > 0) {
//                 int newY = c.row * tileMapComponent->getSize() - rect->getHeight();
//                 playerTransform->setPosition(oldX, newY);
//             }
//         }
//         e.clear(32, 32, 32, 255);

//         camera.Update();
//         // camX = playerTransform->xPos - levelWidth/2;
//         // camY = playerTransform->yPos - levelHeight/2;
//         // if (camX < 0) {
//         //     camX = 0;
//         // }
//         // if (camX > levelWidth - levelWidth/2) {
//         //     camX = levelWidth - levelWidth/2;
//         // }
//         // if (camY < 0) {
//         //     camY = 0;
//         // }
//         // if (camY > levelHeight - levelHeight/2) {
//         //     camY = levelHeight - levelHeight/2;
//         // }

//         tileMap.Render(camera.x, camera.y);
//         // tileMapComponent->Render(e.getSDLRenderer(), 0, 0);
//         // tileMapComponent->Render(e.getSDLRenderer(), playerTransform->xPos, playerTransform->yPos);
//         player.Render(camera.x, camera.y);
//         e.flip();

//         // e.delay(15);
//         frameTicks = SDL_GetTicks() - frameStartTime;
//         if (frameTicks < maxTicksPerFrame) { // Move this logic into the engine?
//             SDL_Delay(maxTicksPerFrame - frameTicks);
//         }
//         else {
//             std::cout << "Exceeding frametime: " << frameTicks << "ms" << std::endl;
//         }

//         // Calculate average fps and display
//         frame_count++;
//         fps = frame_count / ((SDL_GetTicks() - startTime) / 1000.0f);
//         e.setTitle(std::to_string(fps));
//     }
//     delete playerTransform;
//     delete rect;
//     delete physicsComponent;
//     delete tileMapComponent;
// 	return 0;
// }