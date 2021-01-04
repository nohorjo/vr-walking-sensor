import math

class MoveablePoint:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
        self.angle = 0

    def val(self):
        return [self.x, self.y]

    def up(self, v: float):
        self.y += v
        return self

    def down(self, v: float):
        self.y -= v
        return self

    def left(self, v: float):
        self.x -= v
        return self

    def right(self, v: float):
        self.x += v
        return self

    def set(self, x = None, y = None, angle = None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if angle is not None:
            self.angle = angle
        return self

    def reset(self):
        return self.set(0, 0, 0)

    def rotate(self, degrees):
        self.angle += degrees
        self.angle %= 360
        return self

    def forward(self, v):
        self.x += v * math.cos(math.radians(self.angle))
        self.y += v * math.sin(math.radians(self.angle))
        return self

