from math import sqrt, cos, sin, atan2
from random import random, randint

from fireworks.util import flatten


class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise NotImplemented

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return self + (-other)
        raise NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        raise NotImplemented

    def __truediv__(self, other):
        return self * (1/other)

    def normalised(self):
        return self / self.length()

    def length(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def clone(self):
        return Vec2(self.x, self.y)

    def screen_space(self, window):
        return self.x * window.width / 2 + window.width / 2, self.y * (window.width / 3 * 2)

    def as_tri(self, window, size=0.0025):
        return flatten([(self + Vec2(0, size)).screen_space(window), (self + Vec2(size, -size)).screen_space(window), (self + Vec2(-size, -size)).screen_space(window)])


class Particle(object):
    __slots__ = [
        "position",
        "velocity",
        "_colour",
        "lifespan",
        "timer"
    ]

    def __init__(self, position, speed, colour, lifespan=None):
        self.position = position
        self.velocity = speed
        self._colour = colour
        self.lifespan = lifespan
        self.timer = 0

    @property
    def colour(self):
        r, g, b = self._colour
        if self.lifespan is not None:
            l = 1 - (self.timer / self.lifespan)
            r = int(r * l)
            g = int(g * l)
            b = int(b * l)
        return r, g, b

    def update(self, dt, acceleration, window):
        self.timer += dt
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        x, y = self.position.screen_space(window)
        if x < 0 or x > window.width or y < 0:
            return []

        if self.lifespan is not None:
            if self.timer >= self.lifespan:
                return []

        return [self]


class Firework(Particle):
    __slots__ = [
        "position",
        "velocity",
        "_colour",
        "lifespan",
        "timer",
        "last_spark"
    ]

    def __init__(self, position, speed, colour, lifespan):
        super().__init__(position, speed, colour, lifespan)
        self.last_spark = 0

    @property
    def colour(self):
        r, g, b = 250, 209, 70
        f = random() * 0.4 + 0.8
        r = int(min(255, r * f))
        g = int(min(255, g * f))
        b = int(min(255, b * f))
        return r, g, b

    def update(self, dt, acceleration, window):
        particles = super().update(dt, acceleration, window)
        self.last_spark += dt
        if not particles:
            colour = (randint(0, 255), randint(0, 255), randint(0, 255))
            for _ in range(randint(25, 100)):
                diff = Vec2(random() * 2 - 1, random() * 2 - 1).normalised() * (random() * 0.15 + 0.05)
                particles.append(Particle(self.position.clone(), self.velocity + diff, colour, random() * 10 + 2))
        elif self.last_spark > 0.125 * (self.velocity.length() / 100):
            self.last_spark = 0
            particles.append(Particle(self.position.clone(), -self.velocity.normalised() * 0.2, self.colour, random() * 2))
        return particles


class SuperFirework(Particle):
    __slots__ = [
        "position",
        "velocity",
        "_colour",
        "lifespan",
        "timer",
        "last_spark"
    ]

    def __init__(self, position, speed, colour, lifespan):
        super().__init__(position, speed, colour, lifespan)
        self.last_spark = 0

    @property
    def colour(self):
        r, g, b = 250, 209, 70
        f = random() * 0.4 + 0.8
        r = int(min(255, r * f))
        g = int(min(255, g * f))
        b = int(min(255, b * f))
        return r, g, b

    def update(self, dt, acceleration, window):
        particles = super().update(dt, acceleration, window)
        self.last_spark += dt
        if not particles:
            colour = (randint(100, 255), randint(100, 255), randint(100, 255))
            for _ in range(randint(5, 10)):
                diff = Vec2(random() * 2 - 1, random() * 2 - 1).normalised() * (random() * 0.15 + 0.05)
                particles.append(Firework(self.position.clone(), self.velocity + diff, colour, random() * 3 + 1))
        elif self.last_spark > 0.125 * (self.velocity.length() / 100):
            self.last_spark = 0
            particles.append(Particle(self.position.clone(), -self.velocity.normalised() * 0.2, self.colour, random() * 2))
        return particles
