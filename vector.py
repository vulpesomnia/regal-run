#TODO: check if this is really required. Pygame has a vector class.

import pygame, math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def convert(self):
        return pygame.math.Vector2(self.x, self.y)
    
    def normalize(self):
        mag = math.sqrt(self.x ** 2 + self.y ** 2)
        if mag != 0:
            self.x, self.y = self.x / mag, self.y / mag
        else:
            self.x, self.y = 0, 0
    

class Vector3:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"