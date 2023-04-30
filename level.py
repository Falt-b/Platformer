import pygame
import json
from animator import get_image
from tiles import Tile


class Level:
    def __init__(self):
        self.tiles = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.tile_sets = []

        self.width = 0
        self.height = 0
        self.center = (0, 0)
        self.scale = 0

    def set_dimensions(
        self, width: int, height: int, tilewidth: int, tileheight: int, scale: int
    ):
        self.width = width * tilewidth * scale
        self.height = height * tileheight * scale
        self.center = (self.width / 2, self.height / 2)
        self.scale = scale

    def load_tile_set(self, tile_set: str, scale: int):
        tiles = []
        with open(tile_set[3:], "r") as file:
            tile_data = json.load(file)
            img_set = pygame.image.load("Tile_Sets/" + tile_data["image"])
            img_set = pygame.transform.scale(
                img_set,
                (tile_data["imagewidth"] * scale, tile_data["imageheight"] * scale),
            )
            # find width and height of image based on tiles
            for y in range(int(tile_data["imageheight"] / tile_data["tileheight"])):
                for x in range(int(tile_data["imagewidth"] / tile_data["tilewidth"])):
                    tiles.append(
                        get_image(
                            img_set,
                            y,
                            x,
                            tile_data["tilewidth"] * scale,
                            tile_data["tileheight"] * scale,
                        )
                    )
        return tuple(tiles)

    def create_tiles(
        self, layer_data: dict, tilewidth: int, tileheight: int, scale: int, *groups
    ):
        for y in range(layer_data["height"]):
            for x in range(layer_data["width"]):
                current_tile = layer_data["data"][(y * layer_data["width"]) + x]
                if current_tile != 0:
                    Tile(
                        pygame.Vector2(x * tilewidth * scale, y * tileheight * scale),
                        self.tile_sets[current_tile - 1],
                        tilewidth,
                        tileheight,
                        scale,
                        False,
                        *groups,
                    )

    def load_level(self, level_file: str, scale: int):
        with open(level_file, "r") as file:
            level_data = json.load(file)
            self.set_dimensions(
                level_data["width"],
                level_data["height"],
                level_data["tilewidth"],
                level_data["tileheight"],
                scale,
            )
            # load tile sets
            for tile_set in level_data["tilesets"]:
                self.tile_sets += self.load_tile_set(tile_set["source"], scale)
            # load create layers from layer data
            for layer in level_data["layers"]:
                group_list = [self.tiles]
                if (
                    layer["properties"][0]["name"] == "collidable"
                    and layer["properties"][0]["value"]
                ):
                    group_list.append(self.colliders)
                self.create_tiles(
                    layer,
                    level_data["tilewidth"],
                    level_data["tileheight"],
                    scale,
                    group_list,
                )
        del self.tile_sets
