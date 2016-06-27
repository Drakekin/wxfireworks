from random import randint, random, choice

import pyglet

from fireworks.particle import Firework, Vec2, SuperFirework
from fireworks.util import flatten


class FireworksWindow(pyglet.window.Window):
    def __init__(self, particles, *args, **kwargs):
        super().__init__(resizable=True, *args, **kwargs)
        self.particles = particles
        self.dt = 1

    def on_draw(self):
        self.clear()
        vertexes = flatten((p.position.as_tri(window) for p in self.particles))
        colours = flatten((flatten([p.colour, p.colour, p.colour]) for p in self.particles))
        pyglet.graphics.draw(
            len(window.particles) * 3, pyglet.gl.GL_TRIANGLES,
            ("v2f", vertexes),
            ("c3B", colours),
        )

        label = pyglet.text.Label(
            '{:,} particles, {:.0f}fps, {}x{}'.format(
                len(self.particles),
                1/self.dt if self.dt else 999,
                self.width,
                self.height
            ),
            font_name='Times New Roman',
            font_size=12,
            x=self.width//2, y=self.height,
            anchor_x='center', anchor_y='top')
        label.draw()


def update(dt):
    window.dt = dt
    window.particles = flatten(map(lambda p: p.update(dt, Vec2(0, -0.1), window), window.particles))
    if random() > 0.9:
        window.particles.append(choice(firework_set)(Vec2(random() * 1.5 - 0.75, 0), Vec2(random() * 0.1 - 0.05, random() * 0.25 + 0.25), (255, 255, 255), randint(1, 5)))


def main():
    global firework_set, window
    firework_set = [Firework, Firework, SuperFirework]
    window = FireworksWindow([
                                 choice(firework_set)(Vec2(random() * 1.5 - 0.75, 0),
                                                      Vec2(random() * 0.1 - 0.05, random() * 0.25 + 0.25),
                                                      (255, 255, 255), randint(1, 5)) for _ in range(randint(5, 20))
                                 ])
    pyglet.clock.schedule(update)
    pyglet.app.run()


if __name__ == "__main__":
    main()
