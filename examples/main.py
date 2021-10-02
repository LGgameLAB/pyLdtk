import json
import pygame
import os, sys
import imgLoaders 

def get_data(file):
    with open(file, "r") as data:
        return json.loads(data.read())

## This is object holds all the data for a .ldtk file
class Ldtk:
    def __init__(self, ldtkfile, **kwargs): ## It takes in the file path
        self.ldtkData = get_data(ldtkfile) ## Loads the JSON
        self.ldtkFile = ldtkfile
        self.header = self.ldtkData['__header__'] ## Sets the header info to something more convenient

        for k, v in self.ldtkData.items(): ## Here what it does is load all the floating information into the object as attributes  
            if not isinstance(v, dict) or not isinstance(v, list): ## but it ignores all the lists and dictionary to handle them seperately
                self.__dict__[k] = v
            else:
                print(v)
        
        self.scaler = kwargs.get("scaler", 1)
        self.imageLoader = kwargs.get("imageLoader", imgLoaders.pygameLoader)
        self.levels = []

        for l in self.ldtkData['levels']:
            self.levels.append(Ldtklevel(self, l))

class Ldtklevel:
    def __init__(self, ldtk, data):
        self.ldtk = ldtk
        self.data = data
        for k, v in self.data.items():
            self.__dict__[k] = v

        self.scaler=ldtk.scaler
        self.layers = [layer(l, self) for l in self.layerInstances]
        self.layers.reverse() 

        self.width, self.height = self.pxWid*self.scaler, self.pxHei*self.scaler   
    
    def getTileLayers(self):
        return list(l for l in self.layers if l._type == "Tiles")
    
    def autoPgTileRender(self):
        image = pygame.Surface((self.width, self.height))
        for layer in self.getTileLayers():
            for tile in layer.tiles:
                image.blit(tile.getImg(), tile.pos)
        return image
    
    def autoPilTileRender(self):
        from PIL import Image
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0))
        for layer in self.getTileLayers():
            for tile in layer.tiles:
                img.paste(tile.getImg(), (int(tile.pos.x), int(tile.pos.y)))#, int(tile.srcRect[2]), int(tile.srcRect[3])))
        return img

class layer:
    def __init__(self, data, level):
        self.data = data
        self.level = level
        for k, v in self.data.items():
            if k[0:2] == '__':      ## Note this part where python seems to dislike the use of __ so I reduced it to a single underscore
                self.__dict__[k[1:]] = v
            else:
                self.__dict__[k] = v
        
        self.scaler = level.scaler
        if self._type == "Tiles":
            self.loadTileSheet()

    def loadTileSheet(self):
        self.tileset = Tileset(self)
        self.tiles = [tile(t, self) for t in self.gridTiles]

class Tileset:
    def __init__(self, layer):
        self.layer = layer
        self.tilesetPath = layer._tilesetRelPath
        os.chdir(os.path.split(self.layer.level.ldtk.ldtkFile)[0])
        self.imageLoader = self.layer.level.ldtk.imageLoader(self.tilesetPath)
        
    def getTileImg(self, rect, scaler=1):
        return self.imageLoader.getTileImage(rect, scaler)

class tile:
    def __init__(self, data, layer):
        self.data = data
        self.layer = layer
        for k, v in self.data.items():
            if k[0:2] == '__':      
                self.__dict__[k[1:]] = v
            else:
                self.__dict__[k] = v
        
        self.scaler = self.layer.scaler
        self.pos = pygame.Vector2(tuple(self.px))*self.scaler
        self.src = pygame.Vector2(tuple(self.src))
        self.srcRect = (self.src.x, self.src.y, self.layer._gridSize, self.layer._gridSize)
    
    def getImg(self):
        tileImg = self.layer.tileset.getTileImg(self.srcRect, self.scaler)
        return tileImg
