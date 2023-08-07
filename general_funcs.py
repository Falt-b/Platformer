import pygame
import math


def limit_range(n: float, max_num: float, min_num: float):
    return max(min(n, max_num), min_num)


def map_range(n: float, max_num: float, min_num: float, new_range: int):
    return (n - min_num) / (max_num - min_num) * new_range


def lerp(p1: pygame.Vector2, p2: pygame.Vector2, t: float):
    return ((1 - t) * p1) + (t * p2)


def quad_bezier(points: list[pygame.Vector2], t: float):
    return (
        (math.pow(1 - t, 2) * points[0])
        + (2 * (1 - t) * t * points[1])
        + (math.pow(t, 2) * points[2])
    )


def cubic_bezier(
    points: list[pygame.Vector2],
    t: float,
):
    return (
        (math.pow(1 - t, 3) * points[0])
        + (3 * math.pow(1 - t, 2) * t * points[1])
        + (3 * (1 - t) * math.pow(t, 2) * points[2])
        + (math.pow(t, 3) * points[3])
    )


def create_quad_curve(points: list[pygame.Vector2], num_points: int):
    t_step = 1 / num_points
    return (
        tuple(
            [points[0]]
            + [
                quad_bezier(points, (point + 1) * t_step)
                for point in range(num_points - 1)
            ]
            + [points[2]]
        ),
        points,
    )


def create_cubic_curve(points: list[pygame.Vector2], num_points: int):
    t_step = 1 / num_points
    return (
        tuple(
            [points[0]]
            + [
                cubic_bezier(points, (point + 1) * t_step)
                for point in range(num_points - 1)
            ]
            + [points[3]]
        ),
        points,
    )
