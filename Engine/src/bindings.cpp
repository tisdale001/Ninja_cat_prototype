#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include "ICamera.hpp"
#include "Transform.hpp"
#include "JumpComponent.hpp"
#include "Rectangle.hpp"
#include "TileMapComponent.hpp"
#include "GameObject.hpp"
#include "PhysicsComponent.hpp"
#include "CenterCamera.hpp"
#include "SideScrollerCamera.hpp"
#include "StaticCamera.hpp"
#include "Engine.hpp"
#include "Sound.hpp"
#include "Music.hpp"
#include "Sprite.hpp"
#include "SpriteCenterCamera.hpp"
#include "SpriteSideScrollerCamera.hpp"
#include "SpriteVerticalScrollerCamera.hpp"

namespace py = pybind11;

/** @brief Pybind module for all methods in Engine.
 *
*/
PYBIND11_MODULE(engine, e) {
    e.doc() = "Game Engine Library";

    py::class_<Transform>(e, "Transform")
        .def(py::init())
        .def_readwrite("xPos", &Transform::xPos)
        .def_readwrite("yPos", &Transform::yPos)
        .def("setPosition", &Transform::setPosition);

    py::class_<Sprite>(e, "Sprite")
        .def(py::init<Transform*, bool>(), py::arg("_transform"), py::arg("readLeftToRight") = true)
        .def("getWidth", &Sprite::getWidth)
        .def("getHeight", &Sprite::getHeight)
        .def("getX", &Sprite::getX)
        .def("getY", &Sprite::getY)
        .def("getCenterX", &Sprite::getCenterX)
        .def("getCenterY", &Sprite::getCenterY)
        .def("setPosition", &Sprite::setPosition)
        .def("update", &Sprite::update)
        .def("render", &Sprite::render)
        .def("loadImage", &Sprite::loadImage)
    	.def("loadImageForPreview", &Sprite::loadImageForPreview)
	    .def("setRectangleDimensions", &Sprite::setRectangleDimensions)
        .def("setSpriteSheetDimensions", &Sprite::setSpriteSheetDimensions)
        .def("removeFromResourceManager", &Sprite::removeSpriteFromManager)
        .def("shutDownManager", &Sprite::shutDownManager);

    py::class_<RectangleComponent>(e, "RectangleComponent")
        .def(py::init<Transform*>())
        .def("getWidth", &RectangleComponent::getWidth)
        .def("getHeight", &RectangleComponent::getHeight)
        .def("getX", &RectangleComponent::getX)
        .def("getY", &RectangleComponent::getY)
        .def("getCenterX", &RectangleComponent::getCenterX)
        .def("getCenterY", &RectangleComponent::getCenterY)
        .def("setDimensions", &RectangleComponent::setDimensions)
        .def("setColor", &RectangleComponent::setColor)
        .def("checkCollision", &RectangleComponent::checkCollision)
        .def("Render", &RectangleComponent::Render);

    py::class_<Collision>(e, "Collision")
        .def(py::init())
        .def_readwrite("isColliding", &Collision::isColliding)
        .def_readwrite("allTileTypes", &Collision::allTileTypes)
        .def_readwrite("firstTileID", &Collision::firstTileID)
        .def_readwrite("firstTileRow", &Collision::firstTileRow)
        .def_readwrite("firstTileColumn", &Collision::firstTileColumn);

    py::class_<TileMapComponent>(e, "TileMapComponent")
        .def(py::init<const std::string&, int, int>())
        .def("ExtendTilemap", &TileMapComponent::ExtendTilemap)
        .def("Render", &TileMapComponent::Render)
        .def("checkCollision", &TileMapComponent::checkCollision)
        .def("isOnGround", &TileMapComponent::isOnGround)
        .def("isOnCeiling", &TileMapComponent::isOnCeiling)
        .def("isTouchingRightWall", &TileMapComponent::isTouchingRightWall)
        .def("isTouchingLeftWall", &TileMapComponent::isTouchingLeftWall)
        .def("isTouchingType", &TileMapComponent::isTouchingType)
        .def("getRows", &TileMapComponent::getRows)
        .def("getCols", &TileMapComponent::getCols)
        .def("getSize", &TileMapComponent::getSize)
        .def("loadTileset", &TileMapComponent::loadTileset)
        .def("PrintTiles", &TileMapComponent::PrintTiles)
        .def("isValidTile", &TileMapComponent::isValidTile)
        .def("tileAt", &TileMapComponent::tileAt)
        .def("tileAtXY", &TileMapComponent::tileAtXY)
        .def("getTileIdx", &TileMapComponent::getTileIdx)
        .def("setTile", &TileMapComponent::setTile);

    py::class_<GameObject>(e, "GameObject")
        .def(py::init<>())
        .def("addCamera", &GameObject::addCamera)
        .def("addTransformComponent", &GameObject::addTransformComponent)
        .def("addJumpComponent", &GameObject::addJumpComponent)
        .def("addRectangleComponent", &GameObject::addRectangleComponent)
        .def("addPhysicsComponent", &GameObject::addPhysicsComponent)
        .def("addTileMapComponent", &GameObject::addTileMapComponent)
        .def("addSpriteComponent", &GameObject::addSpriteComponent)
        .def("InitiateJump", &GameObject::InitiateJump)
        .def_readwrite("mTransform", &GameObject::mTransform)
        .def_readwrite("mJumpComponent", &GameObject::mJumpComponent)
        .def_readwrite("mRectangle", &GameObject::mRectangle)
        .def_readwrite("mPhysicsComponent", &GameObject::mPhysicsComponent)
        .def_readwrite("mTileMapComponent", &GameObject::mTileMapComponent)
        .def_readwrite("mSprite", &GameObject::mSprite)
        .def_readwrite("xVel", &GameObject::xVel)
        .def_readwrite("yVel", &GameObject::yVel);

    py::class_<JumpComponent>(e, "JumpComponent")
        .def(py::init<int, int, float, int>())
        .def("Update", &JumpComponent::Update)
        .def("changeInitialY", &JumpComponent::changeInitialY)
        .def("EndJump", &JumpComponent::EndJump)
        .def("stillJumping", &JumpComponent::stillJumping)
        .def_readwrite("isJumping", &JumpComponent::isJumping)
        .def_readwrite("xVelocity", &JumpComponent::xVelocity);

    py::class_<PhysicsComponent>(e, "PhysicsComponent")
        .def(py::init())
        .def("UpdateX", &PhysicsComponent::UpdateX)
        .def("UpdateY", &PhysicsComponent::UpdateY);

    py::class_<ICamera>(e, "ICamera");

    py::class_<CenterCamera, ICamera>(e, "CenterCamera")
        .def(py::init<int, int, int, int, RectangleComponent*>())
        .def("Update", &CenterCamera::Update)
        .def_readwrite("x", &CenterCamera::x)
        .def_readwrite("y", &CenterCamera::y)
        .def_readwrite("cameraWidth", &CenterCamera::cameraWidth)
        .def_readwrite("cameraHeight", &CenterCamera::cameraHeight)
        .def_readwrite("levelWidth", &CenterCamera::levelWidth)
        .def_readwrite("levelHeight", &CenterCamera::levelHeight);

    py::class_<SideScrollerCamera, ICamera>(e, "SideScrollerCamera")
        .def(py::init<int, int, int, int, RectangleComponent*>())
        .def("Update", &SideScrollerCamera::Update)
        .def_readwrite("x", &SideScrollerCamera::x)
        .def_readwrite("y", &SideScrollerCamera::y)
        .def_readwrite("cameraWidth", &SideScrollerCamera::cameraWidth)
        .def_readwrite("cameraHeight", &SideScrollerCamera::cameraHeight)
        .def_readwrite("levelWidth", &SideScrollerCamera::levelWidth)
        .def_readwrite("levelHeight", &SideScrollerCamera::levelHeight)
        .def_readwrite("target", &SideScrollerCamera::target);

    py::class_<StaticCamera, ICamera>(e, "StaticCamera")
        .def(py::init())
        .def("Update", &StaticCamera::Update)
        .def_readwrite("x", &StaticCamera::x)
        .def_readwrite("y", &StaticCamera::y);

    py::class_<SpriteCenterCamera>(e, "SpriteCenterCamera")
        .def(py::init<int, int, int, int, Sprite*>())
        .def("Update", &SpriteCenterCamera::Update)
        .def_readwrite("x", &SpriteCenterCamera::x)
        .def_readwrite("y", &SpriteCenterCamera::y)
        .def_readwrite("cameraWidth", &SpriteCenterCamera::cameraWidth)
        .def_readwrite("cameraHeight", &SpriteCenterCamera::cameraHeight)
        .def_readwrite("levelWidth", &SpriteCenterCamera::levelWidth)
        .def_readwrite("levelHeight", &SpriteCenterCamera::levelHeight);

    py::class_<SpriteSideScrollerCamera>(e, "SpriteSideScrollerCamera")
        .def(py::init<int, int, int, int, Sprite*>())
        .def("Update", &SpriteSideScrollerCamera::Update)
        .def_readwrite("x", &SpriteSideScrollerCamera::x)
        .def_readwrite("y", &SpriteSideScrollerCamera::y)
        .def_readwrite("cameraWidth", &SpriteSideScrollerCamera::cameraWidth)
        .def_readwrite("cameraHeight", &SpriteSideScrollerCamera::cameraHeight)
        .def_readwrite("levelWidth", &SpriteSideScrollerCamera::levelWidth)
        .def_readwrite("levelHeight", &SpriteSideScrollerCamera::levelHeight);

    py::class_<SpriteVerticalScrollerCamera>(e, "SpriteVerticalScrollerCamera")
        .def(py::init<int, int, int, int, Sprite*>())
        .def("Update", &SpriteVerticalScrollerCamera::Update)
        .def_readwrite("x", &SpriteVerticalScrollerCamera::x)
        .def_readwrite("y", &SpriteVerticalScrollerCamera::y)
        .def_readwrite("cameraWidth", &SpriteVerticalScrollerCamera::cameraWidth)
        .def_readwrite("cameraHeight", &SpriteVerticalScrollerCamera::cameraHeight)
        .def_readwrite("levelWidth", &SpriteVerticalScrollerCamera::levelWidth)
        .def_readwrite("levelHeight", &SpriteVerticalScrollerCamera::levelHeight);

    py::class_<Sound>(e, "Sound")
        .def(py::init<>())
        .def("SetSound", &Sound::SetSound)
        .def("PlaySound", &Sound::PlaySound);

    py::class_<Music>(e, "Music")
        .def(py::init<>())
        .def("SetMusic", &Music::SetMusic)
        .def("PlayMusic", &Music::PlayMusic)
        .def("PauseMusic", &Music::PauseMusic)
        .def("UnPauseMusic", &Music::UnPauseMusic)
        .def("StopMusic", &Music::StopMusic);

    py::bind_vector<std::vector<bool>>(e, "VectorBool");

    py::enum_<Key>(e, "Key")
        .value("W_PRESSED", W_PRESSED)
        .value("S_PRESSED", S_PRESSED)
        .value("A_PRESSED", A_PRESSED)
        .value("D_PRESSED", D_PRESSED)
        .value("J_PRESSED", J_PRESSED)
        .value("Z_PRESSED", Z_PRESSED)
        .value("H_PRESSED", H_PRESSED)
        .value("K_PRESSED", K_PRESSED)
        .value("X_PRESSED", X_PRESSED)
        .value("UP_PRESSED", UP_PRESSED)
        .value("DOWN_PRESSED", DOWN_PRESSED)
        .value("LEFT_PRESSED", LEFT_PRESSED)
        .value("RIGHT_PRESSED", RIGHT_PRESSED)
        .value("SPACE_PRESSED", SPACE_PRESSED)
        .value("ESCAPE_PRESSED", ESCAPE_PRESSED)
        .value("W_TAPPED", W_TAPPED)
        .value("S_TAPPED", S_TAPPED)
        .value("A_TAPPED", A_TAPPED)
        .value("D_TAPPED", D_TAPPED)
        .value("J_TAPPED", J_TAPPED)
        .value("H_TAPPED", H_TAPPED)
        .value("K_TAPPED", K_TAPPED)
        .value("UP_TAPPED", UP_TAPPED)
        .value("DOWN_TAPPED", DOWN_TAPPED)
        .value("LEFT_TAPPED", LEFT_TAPPED)
        .value("RIGHT_TAPPED", RIGHT_TAPPED)
        .value("SPACE_TAPPED", SPACE_TAPPED)
        .value("ESCAPE_TAPPED", ESCAPE_TAPPED)
        .value("QUIT_EVENT", QUIT_EVENT)
        .export_values();

    py::class_<SDLGraphicsProgram>(e, "SDLGraphicsProgram")
        .def(py::init<int, int>(), py::arg("w"), py::arg("h"))
        .def("clear", &SDLGraphicsProgram::clear)
        .def("delay", &SDLGraphicsProgram::delay)
        .def("flip", &SDLGraphicsProgram::flip)
        .def("getInput", &SDLGraphicsProgram::getInput)
        .def("setRenderColor", &SDLGraphicsProgram::setRenderColor)
        .def("getSDLRenderer", &SDLGraphicsProgram::getSDLRenderer)
        .def("DrawRectangle", &SDLGraphicsProgram::DrawRectangle)
        .def("addGameObject", &SDLGraphicsProgram::addGameObject)
        .def("Render", &SDLGraphicsProgram::Render)
        .def("getTimeMS", &SDLGraphicsProgram::getTimeMS)
        .def("setTitle", &SDLGraphicsProgram::setTitle)
        .def("getInputAtFrame", &SDLGraphicsProgram::getInputAtFrame)
        .def("setBlendModeNone", &SDLGraphicsProgram::setBlendModeNone)
        .def("setBlendModeAlpha", &SDLGraphicsProgram::setBlendModeAlpha);
}
