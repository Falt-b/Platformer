import pygame
from math import floor, ceil


class Hash_Map:
    def __init__(self, container_size: int, map_width: int) -> None:
        self.container_size = container_size
        self.width = ceil(map_width / container_size)
        self.objects = {}

    def hash_vector(self, position: pygame.Vector2):
        return (
            floor(position.x / self.container_size)
            + floor(position.y / self.container_size) * self.width
        )

    def get_rect_dimensions(self, rect: pygame.Rect):
        topleft = (
            floor(rect.topleft[0] / self.container_size),
            floor(rect.topleft[1] / self.container_size),
        )
        return (
            floor(rect.topright[0] / self.container_size) - topleft[0] + 1,  # x
            floor(rect.bottomleft[1] / self.container_size) - topleft[1] + 1,  # y
            topleft[0] + (topleft[1] * self.width),  # topleft position
        )

    def insert_object(self, object: object, hash: int):
        if hash in self.objects:
            self.objects[hash].append(object)
        else:
            self.objects.setdefault(hash, [object])

    def insert_rect(self, object: object):
        # assumes object has rect in class
        dimensions = self.get_rect_dimensions(object.rect)
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                self.objects[dimensions[2] + x + (y * self.width)].append(object)

    def remove_object(self, object: object, hash: int):
        # assumes that hash is known and object is already in list
        self.objects[hash].remove(object)
        if len(self.objects[hash]) == 0:
            del self.objects[hash]

    def remove_rect(self, object: object):
        # assumes object has rect in class
        dimensions = self.get_rect_dimensions(object.rect)
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                self.remove_object(
                    object, [dimensions[2] + x + (y * self.width)].remove(object)
                )

    def query(self, hash: int):
        if hash in self.objects:
            return self.objects[hash]
        return []

    def query_rect(self, rect: pygame.Rect):
        found_objects = []
        dimensions = self.get_rect_dimensions(rect)
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                found_objects += self.query(dimensions[2] + x + (y * self.width))
        return found_objects
