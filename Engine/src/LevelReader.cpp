#include <fstream>
#include <iostream>
#include <string>

#include "LevelReader.hpp"
/** @brief Constructor. Takes in level path name
 * 
 * Constructor that calls loadLevel() method with input as level path name
*/
LevelReader::LevelReader(const std::string& levelPath) {
    loadLevel(levelPath);
}

/** @brief Deconstructor
 * 
*/
LevelReader::~LevelReader() {}

/** @brief Internal method that takes in level path name
 * 
 * Internal method, called at constructor, that sets all member variables
*/
void LevelReader::loadLevel(const std::string& levelPath) {
    std::ifstream fileReader;
    fileReader.open(levelPath);
    if (!fileReader) {
        std::cout << "Failed to open level file: " << levelPath << std::endl;
        exit(1);
    }
    fileReader >> rows >> cols >> size >> tilesetRows >> tilesetCols;
    tiles.reserve(rows * cols);
    int tileType;
    while (fileReader >> tileType) {
        tiles.push_back(tileType);
    }
    // std::cout << "Rows: " << rows << " Cols: " << cols << " Size: " << tiles.size() << std::endl;
}

/** @brief Getter: returns rows
 * 
 * Getter method that returns rows
*/
int LevelReader::getRows() {
    return rows;
}

/** @brief Getter: return cols
 * 
 * Getter method that returns cols
*/
int LevelReader::getCols() {
    return cols;
}

/** @brief Getter: returns size
 * 
 * Getter method that returns size
*/
int LevelReader::getTileSize() {
    return size;
}

/** @brief Getter: returns tilesetRows
 * 
 * Getter method that returns tilesetRows
*/
int LevelReader::getTilesetRows() {
    return tilesetRows;
}

/** @brief Getter: returns tilesetCols
 * 
 * Getter method that returns tilesetCols
*/
int LevelReader::getTilesetCols() {
    return tilesetCols;
}

/** @brief Getter: returns tiles
 * 
 * Getter method that returns tiles
*/
std::vector<int> LevelReader::getTiles() {
    return tiles;
}


