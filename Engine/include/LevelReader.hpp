#pragma once

#include <string>
#include <vector>

class LevelReader {
    public:
        LevelReader(const std::string& levelPath);

        ~LevelReader();

        int getRows();

        int getCols();
        
        int getTileSize();
        
        int getTilesetRows();

        int getTilesetCols();

        std::vector<int> getTiles();

    private:
        int rows;
        int cols;
        int size;
        int tilesetRows;
        int tilesetCols;
        std::vector<int> tiles;

        void loadLevel(const std::string& levelPath);
};