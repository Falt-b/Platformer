import pygame
import json
from animator import get_image
from hash_map import Hash_Map


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        position: tuple,
        width: int,
        height: int,
        collidable: bool,
    ):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(position, (width, height))
        self.collidable = collidable

class Level(Hash_Map):
    def __init__(self, container_size: int, map_width: int):
        super().__init__(container_size, map_width)
        self.layers = {}
        self.tile_sets = []
        self.hash_map = hash_map
        self.width = 0
        self.height = 0

    def load_tile_set(self, tile_set: str):
        tiles = []
        with open(tile_set[3:], "r") as file:
            tile_data = json.load(file)
            img_set = pygame.image.load("Tile_Sets/" + tile_data["image"])
            # find width and height of image based on tiles
            for y in range(int(tile_data["imageheight"] / tile_data["tileheight"])):
                for x in range(int(tile_data["imagewidth"] / tile_data["tilewidth"])):
                    tiles.append(
                        get_image(
                            img_set,
                            y,
                            x,
                            tile_data["tilewidth"],
                            tile_data["tileheight"],
                        )
                    )
        return tuple(tiles)

    def create_tiles(
        self, layer_data: dict, tilewidth: int, tileheight: int, collidable: bool
    ):
        tiles = []
        for y in range(layer_data["height"]):
            for x in range(layer_data["width"]):
                current_tile = layer_data["data"][(y * layer_data["width"]) + x]
                if current_tile != 0:
                    tiles.append(
                        Tile(
                            self.tile_sets[current_tile - 1],
                            pygame.Vector2(x * tilewidth, y * tileheight),
                            tilewidth,
                            tileheight,
                            collidable,
                        )
                    )
        return tiles

    def hash_tiles(self):
        for layer in self.layers:
            for tile in self.layers[layer]:
                self.hash_map.insert_rect(tile)

    def load_level(self, level_file: str):
        with open(level_file, "r") as file:
            level_data = json.load(file)
            self.width = level_data["width"] * level_data["tilewidth"]
            self.height = level_data["height"] * level_data["tileheight"]
            # load tile sets
            for tile_set in level_data["tilesets"]:
                self.tile_sets += self.load_tile_set(tile_set["source"])
            # load create layers from layer data
            for layer in level_data["layers"]:
                layer_settings = {}
                for setting in layer["properties"]:
                    layer_settings[setting["name"]] = setting["value"]
                self.layers[layer["id"]] = self.create_tiles(
                    layer,
                    level_data["tilewidth"],
                    level_data["tileheight"],
                    layer_settings["collidable"],
                )
        del self.tile_sets
        self.hash_tiles()

    def get_rect_dimensions(self, rect: pygame.Rect):
        topleft = (
            floor(rect.topleft[0] / self.container_size),
            floor(rect.topleft[1] / self.container_size),
        )
        return (
            floor(rect.topright[0] / self.container_size) - topleft[0] + 1,  # x
            floor(rect.bottomleft[1] / self.container_size) - topleft[1] + 1,  # y
            topleft[0],
            topleft[1],
            topleft[0] + (topleft[1] * self.width),  # topleft position
        )

    def query_rect(self, rect: pygame.Rect):
        found_objects = []
        dimensions = self.get_rect_dimensions(rect)
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                found_objects += self.query(dimensions[2] + x + (y * self.width))
        return found_objects, dimensions

    def get_nearest_colliders(self, query_rect: pygame.Rect):
        return [
            tile for tile in self.query_rect(query_rect)[0] if tile.collidable
        ]

    def get_active_tiles(self, query_rect: pygame.Rect):
        return self.query_rect(query_rect)
