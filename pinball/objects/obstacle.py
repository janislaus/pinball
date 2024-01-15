from math import cos, sin, pi
import pygame


def rotate_vector(vector, angle):
    """vector = x,y tuple"""
    rotated_vector = (
        cos(angle) * vector[0] - sin(angle) * vector[1],
        sin(angle) * vector[0] + cos(angle) * vector[1],
    )
    return rotated_vector


def vector(A, B):
    return (A[0] - B[0], A[1] - B[1])


def give_highest_value(a, b, c):
    max = a
    if a < b:
        if c < b:
            max = b
        max = c
    return max


class Pendulum:
    def __init__(self, x, y, r, length, screen, colour):
        self.x = x
        self.y = y
        self.radius = r
        self.length = length
        self.colour = colour
        self.angle = pi / 4
        self.angle_velocity = 0.01
        self.angle_acceleration = 0
        self.origin = screen.get_width() // 2, self.y

    def draw(self, screen):
        pygame.draw.line(
            screen, (0, 0, 0), (screen.get_width() // 2, 0), (self.x, self.y)
        )
        pygame.draw.circle(screen, self.colour, [self.x, self.y], self.radius)

    def move(self, screen, GRAVITY_Y):
        """gleichung vom harmonischen oszillator"""
        force = GRAVITY_Y * sin(self.angle)
        self.angle_acceleration = (-1 * force) / self.length
        self.angle_velocity += self.angle_acceleration
        self.angle += self.angle_velocity

        self.x = self.length * sin(self.angle) + self.origin[0]
        self.y = self.length * cos(self.angle) + self.origin[1]
        if self.y <= self.length:
            self.angle_velocity *= -1


class Rectangle:
    """spinning rectangle"""

    def __init__(self, x, y, width, height, colour):
        """initiates instance rectanlgle:
        x,y => Coordinates of the center of the rectangle which also characterises its spinning axis
        widht, height , colour => properties of the rectangle"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        """Now we can calculate the 4 corners of the rectangle when it is resting in horizontally """
        self.corner1 = self.x - self.width // 2, self.y - self.height
        """upper right corner"""
        self.corner2 = self.x + self.width // 2, self.y - self.height
        """upper left corner"""
        self.corner3 = self.x + self.width // 2, self.y + self.height
        """lower left corner"""
        self.corner4 = self.x - self.width // 2, self.y + self.height
        """lower right corner"""
        self.angle = 0
        self.angle_velocity = -0.0001

    def rotate(self):
        self.angle += self.angle_velocity

        rot_corner1 = rotate_vector(self.corner1, self.angle)
        rot_corner2 = rotate_vector(self.corner2, self.angle)
        rot_corner3 = rotate_vector(self.corner3, self.angle)
        rot_corner4 = rotate_vector(self.corner4, self.angle)
        return [rot_corner1, rot_corner2, rot_corner3, rot_corner4]

    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.rotate())


class RightTriangle:
    def __init__(self, A, B, C, colour):
        """A , B , C => (x,y)-tuples of the 3 corners"""

        self.A = A
        self.B = B
        self.C = C
        self.colour = colour
        self.AB = vector(self.A, self.B)
        self.BC = vector(self.B, self.C)
        self.CA = vector(self.C, self.A)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, [self.A, self.B, self.C])

