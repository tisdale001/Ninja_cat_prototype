import os

import tkinter as tk
from tkinter import ttk, Toplevel, Label, Entry, StringVar
from PIL import Image, ImageTk

from lib import engine


class tileset:
    """
    This is a class to create a Dictionary of tiles to use for "tile-bar" in editor.
    Main function is getter which returns tileDict
    """
    def __init__(self, tilemapImagePath, pixelWidth, pixelHeight, tileSize, tileNumList, tilesetName, offSetX, offSetY):
        self.tilemapImage = Image.open(tilemapImagePath)
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        self.tileSize = tileSize
        self.tileNumList = tileNumList
        self.tilesetName = tilesetName
        self.offSetX = offSetX
        self.offSetY = offSetY
        self.tileDict = self.createTileDict()
    
    def createTileDict(self):
        if not all([isinstance(item, int) for item in self.tileNumList]):
            return {}
        tempPathName = "Assets/tileImages/" + self.tilesetName + "/"
        if not os.path.exists(tempPathName):
            os.makedirs(tempPathName)
        numRows = self.pixelHeight // self.tileSize
        numCols = self.pixelWidth // self.tileSize
        tileDict = {}
        for i in range(len(self.tileNumList)):
            tileNum = self.tileNumList[i]
            row = tileNum // numCols
            col = tileNum
            if row != 0:
                col = tileNum % (numCols * row)
            ph = self.tilemapImage.crop((self.tileSize * col + self.offSetX, self.tileSize * row + self.offSetY,
                                        self.tileSize * (col + 1) + self.offSetX, self.tileSize * (row + 1) + self.offSetY))
            pathName = tempPathName + str(i) + ".png"
            ph.save(pathName)
            tileDict[i] = pathName
        return tileDict
    
    def getTileDict(self):
        return self.tileDict
    
    def getTilesetName(self):
        return self.tilesetName
    
class currentTile:
    # this is a simple class that solves a problem: it acts like a global variable to keep track of current-tile number
    def __init__(self):
        self.current_tile = 0
        self.mouse_down = 0
        self.previous_tile = 0
    
    def getCurrentTile(self):
        return self.current_tile

    def setCurrentTile(self, int_):
        if int_ == self.current_tile:
            return
        self.previous_tile = self.current_tile
        self.current_tile = int_

    def setCurrentTileToPrevious(self):
        self.current_tile = self.previous_tile
    
    def getMouseDown(self):
        return self.mouse_down

    def setMouseDown(self, int_):
        self.mouse_down = int_


def setTile(e, currentTile):
    # If the current tile is -1, erase instead
    if currentTile.getCurrentTile() == -1:
        clearTile(e)
        return
    e.widget.config(image=TILE_ARRAY[currentTile.getCurrentTile()], borderwidth=0, 
                    textvariable=str(currentTile.getCurrentTile()))

def clearTile(e):
    e.widget.config(image='', borderwidth=2, bg="#d9d9d9", textvariable="-1")

def setCurrentTile(e, currentTile):
    currentTile.setCurrentTile(int(str(e.widget.cget('textvariable'))))

def setMouseDown(e, currentTile, setValue):
    currentTile.setMouseDown(setValue)
    setTile(e, currentTile)

# Sets the current tile to -1, aka erase
def setCurrentTileToClear(e, currentTile):
    currentTile.setCurrentTile(-1)
    setTile(e, currentTile)

# Reverts the current tile to the previous tile
def backToPreviousTile(e, currentTile):
    currentTile.setCurrentTileToPrevious()

# The "place" button action (left click)
def placeButton(e, currentTile):
    # "unclick" if mousedown variable is true
    if currentTile.getMouseDown() == 1:
        currentTile.setMouseDown(0)
        print("MODE: single place/erase")
    # if the current tile is erase, set it to the previous tile
    if currentTile.getCurrentTile() == -1:
        backToPreviousTile(e, currentTile)
    # then place the tile
    setTile(e, currentTile)

# The "multi place" button action (left click)
def multiPlaceButton(e, currentTile):
    # set mouse down to true
    currentTile.setMouseDown(1)
    print("MODE: multi place")
    # if the current tile is erase, set it to the previous tile
    if currentTile.getCurrentTile() == -1:
        backToPreviousTile(e, currentTile)
    # then place the tile
    setTile(e, currentTile)

# The "erase" button action (right click)
def eraseButton(e, currentTile):
    # "unclick" if mousedown variable is true
    if currentTile.getMouseDown() == 1:
        currentTile.setMouseDown(0)
        print("MODE: single place/erase")
    # erase tile
    clearTile(e)

# The "multi erase" button action (right click)
def multiEraseButton(e, currentTile):
    # set mousedown to true
    currentTile.setMouseDown(1)
    print("MODE: multi erase")
    # set current tile to clear
    setCurrentTileToClear(e, currentTile)
    # then place the current tile (or erase)
    setTile(e, currentTile)

# Mouse entered a tile
def mouseEntered(e, currentTile):
    if currentTile.getMouseDown() == 1:
        setTile(e, currentTile)

def loadLevel(levelFile):
    levelFilePath = os.path.join(levelAssetsPath + tilesetName + "/", levelFile)
    if not os.path.exists(levelFilePath):
        return
    grid = []
    with open(levelFilePath, "r") as f:
        metadata = f.readline().split()
        rows = int(metadata[0])
        cols = int(metadata[1])
        tileSize = int(metadata[2])
        for line in f:
            row = list(map(int, line.split()))
            grid.append(row)
    createEditor(root, grid, tiles.getTileDict(), curTile, rows, cols, tileSize, tilesetName)


def saveLevel(window, rows, cols, tileSize, tileFrame, tilesetName):
    def saveLevel3(window2, window3, levelName):
        tempPathName = levelAssetsPath + tilesetName + "/"
        if not os.path.exists(tempPathName):
            os.makedirs(tempPathName)
        levelPath = os.path.join(levelAssetsPath, tilesetName + "/", levelName)
        with open(levelPath, "w") as f:
            f.write(f"{rows} {cols} {tileSize} {tilesetRows} {tilesetCols}\n")
            tiles = tileFrame.winfo_children()
            for idx, tile in enumerate(tiles, 1):
                f.write(str(tile.cget("textvariable")))
                if idx % cols == 0:
                    f.write("\n")
                else:
                    f.write("\t")
            # destroy popups
            if window3 != None:
                window3.destroy()
            if window2 != None:
                window2.destroy()

    def saveLevel2(window2, levelName):
        # overwrite check: popup
        window3 = Toplevel(window2)
        window3.geometry("300x200")
        window3.title("Overwrite?")
        label = tk.Label(window3, text="Level already exists, overwrite?", font="Arial 15", pady=20)
        label.pack()
        newFrame = tk.Frame(window3)
        newFrame.pack(pady=50)
        yesButton = tk.Button(newFrame, text="Yes", command=lambda:saveLevel3(window2, window3, levelName))
        noButton = tk.Button(newFrame, text="No", command=window3.destroy)
        yesButton.pack(side=tk.LEFT, padx=20)
        noButton.pack(side=tk.LEFT, padx=20)
    
    def checkSave(window2, levelName, levelList):
        # parse levelName: look for '.lvl'
        x = levelName.split(".")
        if x[-1] != "lvl":
            levelName += ".lvl"
        if levelName in levelList:
            saveLevel2(window2, levelName)
        else:
            saveLevel3(window2, None, levelName)
        
    # first create folder for current tileset
    tempNewPathName = levelAssetsPath + tilesetName  + "/"
    if not os.path.exists(tempNewPathName):
        os.makedirs(tempNewPathName)
    # code for saveLevel window begins here
    window2 = Toplevel(window)
    window2.geometry("300x200")
    window2.title("Save level as...")
    label = tk.Label(window2, text="Enter name for level", font="Arial 15")
    label.pack()
    levelFiles = os.listdir(tempNewPathName)
    levelList = list(levelFiles)
    combo = ttk.Combobox(window2, values=levelList)
    combo.pack(expand=True)
    frame = tk.Frame(window2)
    frame.pack()
    saveButton = tk.Button(frame, text="Save", command=lambda:checkSave(window2, combo.get(), levelList))
    cancelButton = tk.Button(frame, text="Cancel", command=window2.destroy)
    saveButton.pack(side=tk.LEFT, padx=20)
    cancelButton.pack(side=tk.LEFT, padx = 20)




def enforceNumeric(input):
    return input.isdigit()

def createWindow(pixelWidth, pixelHeight):
    geometry_str = str(pixelWidth) + "x" + str(pixelHeight)
    root = tk.Tk()
    root.title("Editor")
    root.geometry(geometry_str)
    return root

# Creates a tile (tk label) at a position with its bindings
def placeTkLabelTile(label, xPos, yPos, tileSize, currentTile):
    label.place(x=xPos, y=yPos, width=tileSize, height=tileSize)
    label.bind("<Button-1>", lambda e: placeButton(e, currentTile))
    label.bind("<Double-Button-1>", lambda e: multiPlaceButton(e, currentTile))

    label.bind("<Button-3>", lambda e: eraseButton(e, currentTile))
    label.bind("<Double-Button-3>", lambda e: multiEraseButton(e, currentTile))

    label.bind("<Enter>", lambda e: mouseEntered(e, currentTile))

class SpritePlayer():
    def __init__(self, windowWidth, windowHeight):
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.transform = engine.Transform()

        self.sprite = engine.Sprite(self.transform, True)

        self.currentFrame = 0
        self.maxFrame = 0
        self.delay = 16

    def setMaxFrame(self, mf):
        self.maxFrame = mf
        print("maxframe: ",self.maxFrame)

    def setSpriteSheet(self, ss):
        self.sprite.loadImageForPreview("Assets/spritesheets/"+ss, self.sdl.getSDLRenderer())
        print("sheet: ", ss)

    def setSpriteDisplaySize(self, wid, hei):
        self.sprite.setRectangleDimensions(wid, hei)
        print(wid, hei)

    def setSpriteSheetInfo(self, sp_wid, sp_hei, spr, tns, ofst):
        self.sprite.setSpriteSheetDimensions(sp_wid, sp_hei, spr, tns, ofst)
        print(sp_wid, sp_hei, spr, tns, ofst)

    def setDelay(self, delay):
        self.delay = delay

    def runloop(self):
        inputs = self.sdl.getInput()
        while not inputs[engine.QUIT_EVENT]:
            self.update(inputs := self.sdl.getInput())
            self.render()
            self.sdl.delay(self.delay)
    
    def update(self, inputs):
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True

        if self.currentFrame > self.maxFrame:
            self.currentFrame = 0
        else:
            self.currentFrame += 1

        self.sprite.update(0, 0, self.currentFrame)

    def render(self):
        self.sdl.clear(255, 255, 255, 255) # Set background to gray
        self.sprite.render(self.sdl.getSDLRenderer(), 0, 0)
        self.sdl.flip()

    def remove(self):
        self.sprite.removeFromResourceManager()

    def shutDownManagers(self):
        self.sprite.shutDownManager()

def createEditor(root, grid, tileDict, currentTile, rows, cols, tileSize, tilesetName):
    """
    Does: Refreshes the editor by adding or subtracting rows/columns to create new scrollable frame
    so old work is not lost
    Input: grid can be None
    """
    
    # destroy everything in old window
    for widgets in root.winfo_children():
        widgets.destroy()
        

    pixelHeight = rows * tileSize
    pixelWidth = cols * tileSize
    canvasRows = 10
    canvasCols = 20
    canvasHeight = canvasRows * tileSize
    canvasWidth = canvasCols * tileSize

    # create tile-bar
    numTiles = len(tileDict)
    numTileRows = max(2, numTiles // canvasCols + 1)
    numTileCols = canvasCols
    tileBarWidth = canvasWidth
    tileBarHeight = numTileRows * tileSize

    tileBarContainer = ttk.Frame(root)
    tileBarCanvas = tk.Canvas(tileBarContainer, width=tileBarWidth, height=2 * tileSize)
    vScrollbarTileBar = ttk.Scrollbar(tileBarContainer, orient="vertical", command=tileBarCanvas.yview)
    tileScrollFrame = ttk.Frame(tileBarCanvas, width=tileBarWidth, height=tileBarHeight)
    tileScrollFrame.bind("<Configure>", lambda e: tileBarCanvas.configure(scrollregion=tileBarCanvas.bbox("all")))
    tileBarCanvas.create_window((0,0), window=tileScrollFrame, anchor="nw")
    tileBarCanvas.configure(yscrollcommand=vScrollbarTileBar.set)

    tile = 0
    global TILE_ARRAY
    TILE_ARRAY = []
    for r in range(numTileRows):
        for c in range(numTileCols):
            if tile >= numTiles:
                # create empty square (no image)
                label = tk.Label(tileScrollFrame, image='', borderwidth=2, relief="solid", textvariable='-1')
                label.place(x=c * tileSize, y=r * tileSize, width=tileSize, height=tileSize)
            else:
                # create image square
                im = Image.open(tileDict[tile])
                ph = ImageTk.PhotoImage(im)
                TILE_ARRAY.append(ph)
                label = tk.Label(tileScrollFrame, image=ph, borderwidth=2, relief="solid", textvariable=str(tile))
                label.image=ph
                # placeTkLabelTile(label, c * tileSize, r * tileSize, tileSize, currentTile)
                label.place(x=c * tileSize, y=r * tileSize, width=tileSize, height=tileSize)
                label.bind("<Button-1>", lambda e: setCurrentTile(e, currentTile))
            tile += 1
    
    tileBarContainer.pack()
    
    vScrollbarTileBar.pack(side="right", fill="y")
    tileBarCanvas.pack(side="left", fill="both", expand=True)
    
    # create editor grid
    container = ttk.Frame(root, padding=10)
    canvas = tk.Canvas(container, width=canvasWidth, height=canvasHeight)
    hScrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    vScrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, width=pixelWidth, height=pixelHeight)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=hScrollbar.set)
    canvas.configure(yscrollcommand=vScrollbar.set)

    if grid == None:
        for yPos in range(0, pixelHeight, tileSize):
            for xPos in range(0, pixelWidth, tileSize):
                label = tk.Label(scrollable_frame, image='', borderwidth=2, relief="solid", bg="#d9d9d9", textvariable='-1')
                placeTkLabelTile(label, xPos, yPos, tileSize, currentTile)
                # label.place(x=xPos, y=yPos, width=tileSize, height=tileSize)
                # label.bind("<Button-1>", lambda e: setTile(e, currentTile))
                # label.bind("<Button-3>", lambda e: clearTile(e))
    else:
        # there is a grid: old work must be copied
        gridHeight = len(grid)
        gridWidth = len(grid[0])
        for r in range(rows):
            for c in range(cols):
                if r >= gridHeight or c >= gridWidth:
                    # bigger than grid: create new white tile
                    label = tk.Label(scrollable_frame, image='', borderwidth=2, relief="solid", textvariable="-1")
                    placeTkLabelTile(label, c * tileSize, r * tileSize, tileSize, currentTile)
                    # label.place(x=c * tileSize, y=r * tileSize, width=tileSize, height=tileSize)
                    # label.bind("<Button-1>", lambda e: setTile(e, currentTile))
                    # label.bind("<Button-3>", lambda e: clearTile(e))
                else:
                    # set tile to grid value
                    label = tk.Label(scrollable_frame, image=TILE_ARRAY[grid[r][c]] if grid[r][c] != -1 else '', 
                                     borderwidth=0 if grid[r][c] != -1 else 2, relief="solid", textvariable=str(grid[r][c]))                 
                    placeTkLabelTile(label, c * tileSize, r * tileSize, tileSize, currentTile)
                    # label.place(x=c * tileSize, y=r * tileSize, width=tileSize, height=tileSize)
                    # label.bind("<Button-1>", lambda e: setTile(e, currentTile))
                    # label.bind("<Button-3>", lambda e: clearTile(e))


    container.pack()

    hScrollbar.pack(side="bottom", fill="x")
    vScrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    def saveGrid():
        # this internal method creates and returns "grid" (from current level data)
        tiles = scrollable_frame.winfo_children()
        grid = []
        cur_row = []
        for idx, tile in enumerate(tiles):
            if idx > 0 and idx % cols == 0:
                grid.append(cur_row)
                cur_row = []
            cur_row.append(int(str(tile.cget("textvariable"))))
        grid.append(cur_row)
        return grid
    
    def previewSprite():
        new_window = tk.Toplevel()
        new_window.title("Sprite Previewer")
        new_window.geometry("640x480")

        spritesheetVar = StringVar(new_window)
        spritesheetDropdown = None
        spritesheets = os.listdir("Assets/spritesheets/")
        if spritesheets:
            spritesheetVar.set("Select spritesheet") # initial value
            spritesheetDropdown = tk.OptionMenu(new_window, spritesheetVar, *spritesheets)
            spritesheetDropdown.grid(row=7, column=1)

        num_sprites_label = StringVar()
        num_sprites_label.set("Total # of sprites: ")
        sprites_label=Label(new_window, textvariable=num_sprites_label, height=4)
        sprites_label.grid(row=0, column=0)

        num_sprites_input=StringVar(None)
        num_sprites_input=Entry(new_window,textvariable=num_sprites_input,width=5)
        num_sprites_input.grid(row=0, column=1)

        sprites_per_line_label = StringVar()
        sprites_per_line_label.set("Sprites per row: ")
        per_line_label=Label(new_window, textvariable=sprites_per_line_label, height=4)
        per_line_label.grid(row=0, column=2)

        per_line_input=StringVar(None)
        per_line_input=Entry(new_window,textvariable=per_line_input,width=5)
        per_line_input.grid(row=0, column=3)

        sprite_w_label = StringVar()
        sprite_w_label.set("Sprite Width: ")
        sprite_width_label=Label(new_window, textvariable=sprite_w_label, height=4);
        sprite_width_label.grid(row=1, column=0)

        sprite_width_input = StringVar(None)
        sprite_width_input = Entry(new_window,textvariable=sprite_width_input,width=5)
        sprite_width_input.grid(row=1, column=1)

        sprite_h_label = StringVar()
        sprite_h_label.set("Sprite Height: ")
        sprite_height_label=Label(new_window, textvariable=sprite_h_label, height=4);
        sprite_height_label.grid(row=1, column=2)

        sprite_height_input = StringVar(None)
        sprite_height_input = Entry(new_window,textvariable=sprite_height_input,width=5)
        sprite_height_input.grid(row=1, column=3)

        off_label = StringVar()
        off_label.set("Offset: ")
        offset_label=Label(new_window, textvariable=off_label, height=4)
        offset_label.grid(row=2, column=0)

        offset_input = StringVar(None)
        offset_input = Entry(new_window,textvariable=offset_input,width=4)
        offset_input.grid(row=2, column=1)

        del_label = StringVar()
        del_label.set("Delay (ms): ")
        delay_label=Label(new_window, textvariable=del_label, height=4)
        delay_label.grid(row=2, column=2)

        delay_input = StringVar(None)
        delay_input = Entry(new_window, textvariable=delay_input, width=5)
        delay_input.grid(row=2, column=3)

        display_w_label = StringVar()
        display_w_label.set("Display Width: ")
        display_width_label=Label(new_window, textvariable=display_w_label, height=4);
        display_width_label.grid(row=4, column=0)

        display_width_input = StringVar(None)
        display_width_input = Entry(new_window,textvariable=display_width_input,width=5)
        display_width_input.grid(row=4, column=1)

        display_h_label = StringVar()
        display_h_label.set("Display Height: ")
        display_height_label=Label(new_window, textvariable=display_h_label, height=4);
        display_height_label.grid(row=4, column=2)

        display_height_input = StringVar(None)
        display_height_input = Entry(new_window,textvariable=display_height_input,width=5)
        display_height_input.grid(row=4, column=3)
    
        def runSpritePreviewer():

            display_height = display_height_input.get()
            display_width = display_width_input.get()
            offset = offset_input.get()
            sprite_height = sprite_height_input.get()
            sprite_width = sprite_width_input.get()
            num_sp = num_sprites_input.get()
            sprites_per_ln = per_line_input.get()
            sheet = spritesheetVar.get()
            current_delay = delay_input.get()

            if display_height and display_width and offset and sprite_height and sprite_width and num_sp and sprites_per_ln and sheet and current_delay:

                try:
                    sprite_player = SpritePlayer(int(display_width), int(display_height))
                    sprite_player.setSpriteSheet(sheet)
                    sprite_player.setMaxFrame(int(num_sp))
                    sprite_player.setSpriteDisplaySize(int(display_width), int(display_height))
                    sprite_player.setSpriteSheetInfo(int(sprite_width), int(sprite_height), int(sprites_per_ln), int(num_sp), int(offset))
                    sprite_player.setDelay(int(current_delay))

                    sprite_player.runloop()
                    sprite_player = None
                except Exception:
                    print("Something went wrong")

        StartB = tk.Button(new_window, text ="Start", command=runSpritePreviewer)
        StartB.grid(row=7, column=0)

    # pack all buttons
    btn_container1 = ttk.Frame(root, padding=10)
    btn_container2 = ttk.Frame(root, padding=10)
    btn_container3 = ttk.Frame(root, padding=10)
    # btn_container.pack(side=tk.TOP)

    vcmd = (root.register(enforceNumeric), "%P")
    rowLabel = tk.Label(btn_container1, text="Rows", width=5)
    rowLabel.pack(side=tk.LEFT)
    # rowLabel.grid(row=0, column=0)
    rowEntry = tk.Entry(btn_container1, validate="key", validatecommand=vcmd, width=5)
    rowEntry.insert(0, rows)
    rowEntry.pack(side=tk.LEFT)
    # rowEntry.grid(row=0, column=1)
    columnLabel = tk.Label(btn_container1, text="Columns", width=7)
    columnLabel.pack(side=tk.LEFT)
    # columnLabel.grid(row=0, column=2)
    columnEntry = tk.Entry(btn_container1, validate="key", validatecommand=vcmd, width=5)
    columnEntry.insert(0, cols)
    columnEntry.pack(side=tk.LEFT)
    # columnEntry.grid(row=0, column=3)
    refreshButton = tk.Button(btn_container1, text="Refresh", width=5, command=lambda:createEditor(
        root=root, grid=saveGrid(), tileDict=tileDict, currentTile=currentTile, rows=int(rowEntry.get()), 
        cols=int(columnEntry.get()), tileSize=tileSize, tilesetName=tilesetName))
    # refreshButton.grid(row=0, column=5)
    refreshButton.pack(side=tk.LEFT)
    
    previewSpriteButton = tk.Button(btn_container3, text="Preview Sprite", command=previewSprite)
    # previewSpriteButton.grid(row=3, column=2)
    previewSpriteButton.pack(side=tk.LEFT)
    saveButton = tk.Button(btn_container3, text="Save", command=lambda:saveLevel(root, rows, cols, tileSize, scrollable_frame, tilesetName))
    # saveButton.grid(row=3, column=3)
    saveButton.pack(side=tk.LEFT)
    
    loadLevelDropdown = None
    levelFiles = os.listdir(levelAssetsPath + tilesetName + "/")
    if levelFiles:
        loadLevelVar.set("Select level to load") # initial value
        loadLevelDropdown = tk.OptionMenu(btn_container2, loadLevelVar, *levelFiles)
        loadLevelDropdown.pack(side=tk.LEFT)
        # loadLevelDropdown.grid(row=1, column=2)
    loadButton = tk.Button(btn_container2, text="Load", command=lambda:loadLevel(loadLevelVar.get()))
    # loadButton.grid(row=1, column=3)
    loadButton.pack(side=tk.LEFT)


    btn_container1.pack(side=tk.TOP)
    btn_container2.pack(side=tk.TOP)
    btn_container3.pack(side=tk.TOP)

    # currentEditorMode = tk.Label(tileBarContainer, image='', borderwidth=2, relief="solid", textvariable='2')



root = createWindow(1000, 700)
levelAssetsPath = "Assets/Levels/"
loadLevelVar = tk.StringVar(root)
# tilemapImagePath = 'Assets/tilesets/mario-like-tileset-32x32.png'
# tilesetRows = 3 # The number of rows displayed from tileset
# tilesetCols = 16 # The number of columns displayed from tileset
# tileSize = 32
# tilesetName = "MarioTiles"

# Tileset5
tilemapImagePath = 'Assets/tilesets/Tileset5.png'
tilesetRows = 5
tilesetCols = 11
tileSize = 32
offSetXPixels = 0
offSetYPixels = 0
tilesetName = "Tileset5"

pixelWidth = tilesetCols * tileSize
pixelHeight = tilesetRows * tileSize
tileNumList = list(range(0, tilesetRows*tilesetCols + 1))
# tileNumList = [0, 1, 2, 7, 8, 9, 3, 4, 5, 6, 52, 53, 11, 12, 13, 14, 54, 55, 56, 57, 
#                 16, 17, 18, 23, 24, 25, 19, 20, 21, 22, 10, 26, 27, 28, 29, 30, 0, 0, 0, 0,
#                 32, 33, 34, 39, 40, 41, 35, 36, 37, 38]

tiles = tileset(tilemapImagePath, pixelWidth, pixelHeight, tileSize, tileNumList, tilesetName, offSetXPixels, offSetYPixels)
curTile = currentTile()

def main():
    print("Editor:")
    print("Left click to place tile.")
    print("Right click to erase tile.")
    print("Left click tiles in tilesheet section to select which tile to place.")
    print("Double-click left click to enter \"multi-place\" mode, which will place tiles in all tiles that the mouse moves over.")
    print("Double-click right click to enter \"multi-erase\" mode, which will erase all tiles that the mouse moves over.")
    print("Left click or right click to exit \"multi-place\" or \"multi-erase\" modes.")

    if not os.path.exists(levelAssetsPath + tilesetName + "/"):
        os.makedirs(levelAssetsPath + tilesetName + "/")
    
    numRows = 10
    numCols = 20

    tileDict = tiles.getTileDict()

    createEditor(root, None, tileDict, curTile, numRows, numCols, tileSize, tiles.getTilesetName())

    root.update()
    root.mainloop()

if __name__ == "__main__":
    main()
