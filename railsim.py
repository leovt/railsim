import pygame
import time
from pygame.locals import QUIT, VIDEORESIZE, HWSURFACE, DOUBLEBUF, RESIZABLE
from math import sin, cos, pi, atan2
EMPTY = 0
XX = 1
NS = 2
EW = 3
SE = 4
SW = 5
NE = 6
NW = 7

class Track:

    length = 3.5 * 2 * pi + 10

    def pos(self, s):
        s %= self.length
        arc = 3.5 * 0.5 * pi
        if 0 <= s < arc:
            return (8 + 3.5 * cos(s / 3.5), 4 - 3.5 * sin(s / 3.5))
        elif s < arc + 4:
            u = s - arc
            return (8-u, 0.5)
        elif s < 2*arc+4:
            u = s - arc - 4
            return (4 - 3.5 * sin(u / 3.5), 4 - 3.5 * cos(u / 3.5))
        elif s < 2*arc+5:
            u = s - 2*arc - 4
            return (0.5, 4+u)
        elif s < 3*arc+5:
            u = s - 2*arc - 5
            return (4 - 3.5 * cos(u / 3.5), 5 + 3.5 * sin(u / 3.5))
        elif s < 3*arc+9:
            u = s - 3*arc - 5
            return (4+u, 8.5)
        elif s < 4*arc+9:
            u = s - 3*arc - 9
            return (8 + 3.5 * sin(u / 3.5), 5 + 3.5 * cos(u / 3.5))
        else:
            u = s - 4*arc - 9
            return (11.5, 5-u)


class Coach:
    def __init__(self, dummy):

        car_png = pygame.image.load('car.png').convert_alpha()
        print(car_png)
        self.images = [
            car_png.subsurface((0, k*32, 32, 32))
            for k in range(60)
        ]
        assert len(self.images) == 60

    def draw(self, display, x, y, angle):
        a = int(angle / pi * 30 + 0.5) % 60
        print(a)
        display.blit(self.images[-a], (x*32-15.5, y*32-15.5))
        for i,img in enumerate(self.images[::6]):
            display.blit(img, (32*i, 288))


class Game:
    def __init__(self, display):
        self.display = display
        tile_png = pygame.image.load('tiles.png').convert_alpha()

        self.tiles = [
            tile_png.subsurface((32,0,32,32)),
            None,
            tile_png.subsurface((0,0,32,32)),
            tile_png.subsurface((0,32,32,32)),
            tile_png.subsurface((32,0,128,128)),
            tile_png.subsurface((160,0,128,128)),
            tile_png.subsurface((32,128,128,128)),
            tile_png.subsurface((160,128,128,128)),
        ]

        self.ball = tile_png.subsurface((192,256,32,32))

        self.track = Track()
        self.coach = Coach(tile_png)

        self.map = [
        [SE,XX,XX,XX,EW,EW,EW,EW,SW,XX,XX,XX],
        [XX,XX,XX,XX, 0, 0, 0, 0,XX,XX,XX,XX],
        [XX,XX,XX,XX, 0, 0, 0, 0,XX,XX,XX,XX],
        [XX,XX,XX,XX, 0, 0, 0, 0,XX,XX,XX,XX],
        [NS, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,NS],
        [NE,XX,XX,XX, 0, 0, 0, 0,NW,XX,XX,XX],
        [XX,XX,XX,XX, 0, 0, 0, 0,XX,XX,XX,XX],
        [XX,XX,XX,XX, 0, 0, 0, 0,XX,XX,XX,XX],
        [XX,XX,XX,XX,EW,EW,EW,EW,XX,XX,XX,XX],
        ]

    def draw(self, t):
        for y, row in enumerate(self.map):
            for x, tc in enumerate(row):
                src = self.tiles[tc]
                if src:
                    self.display.blit(src, (x*32, y*32))

        for c in range(1):
            x0, y0 = self.track.pos(t-c)
            x1, y1 = self.track.pos(t-0.6-c)
            x, y = 0.5*(x1+x0), 0.5*(y1+y0)

            a = atan2(y0-y1, x0-x1)
            if a<0:
                a += 2*pi
            print(a)
            self.coach.draw(self.display, x, y, a)
        x, y = self.track.pos(t+4)
        self.display.blit(self.ball, (x*32-15.5,y*32-15.5))
    def resize(self, event):
        self.display = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)

def main():
    global tiles
    global display
    pygame.init()
    display = pygame.display.set_mode((600,800), HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.set_caption('Hello 미영!')

    game = Game(display)

    t0 = time.perf_counter()
    t2 = t0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == VIDEORESIZE:
                game.resize(event)

        t = time.perf_counter()
        game.draw(3*t)
        pygame.display.flip()
        t1 = time.perf_counter()
        if t1 > t2+1:
            print('Framerate %0.1f' % (1.0 / (t1-t0)))
            t2 = t1
        t0 = t1
        time.sleep(0.01)

if __name__ == '__main__':
    main()
