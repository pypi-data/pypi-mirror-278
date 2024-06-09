from typing import NamedTuple

Vec2 = tuple[float, float]
class Corners(NamedTuple):
    tl: Vec2
    tr: Vec2
    br: Vec2
    bl: Vec2