import copy
import random


class Tetris:
    class block:
        def __init__(self, idx, rot):
            self.mat = []
            if idx == 'i':
                self.mat = \
                    [[0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0]]
            if idx == 'j':
                self.mat = \
                    [[0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]
            if idx == 'l':
                self.mat = \
                    [[0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]
            if idx == 'o':
                self.mat = \
                    [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]
            if idx == 's':
                self.mat = \
                    [[0, 0, 0, 0],
                     [0, 0, 1, 1],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]
            if idx == 'z':
                self.mat = \
                    [[0, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]
            if idx == 't':
                self.mat = \
                    [[0, 0, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 1, 0],
                     [0, 0, 0, 0]]
            for _ in range(rot):
                self.rotate()
            self.x = 0 - self.left()
            self.y = self.bottom() - 4

        def bottom(self):
            for y in range(4):
                for c in self.mat[3 - y]:
                    if c == 1:
                        return y

        def top(self):
            for y in range(4):
                for c in self.mat[y]:
                    if c == 1:
                        return y

        def left(self):
            for x in range(4):
                for y in range(4):
                    if self.mat[y][x] == 1:
                        return x

        def right(self):
            for x in range(4):
                for y in range(4):
                    if self.mat[y][3 - x] == 1:
                        return 3 - x

        def rotate(self):
            self.mat[:] = map(list, zip(*self.mat[::-1]))

    def __init__(self):
        self.map = []
        self.lastmap = []
        self.blocks_index = 'ijloszt'
        self.next = None
        self.now = None
        self.score = 0
        self.over = False

        for _ in range(10):
            col = []
            for _ in range(20):
                col.append(0)
            self.map.append(col)
            self.lastmap.append(col)

    def drop(self, fall):
        self.clear()
        while True:
            self.map = copy.deepcopy(self.lastmap)
            if self.now is None:
                if self.next is None:
                    self.now = self.block(random.choice(self.blocks_index),
                                          int(random.choice('0123')))
                else:
                    self.now = self.next
                self.next = self.block(random.choice(self.blocks_index),
                                       int(random.choice('0123')))
            reach = False
            if self.now.y < 16 + self.now.bottom():
                self.now.y += 1
            else:
                reach = True
            for x in range(4):
                for y in range(4):
                    if self.now.mat[y][x] == 1:
                        if x + self.now.x in range(10):
                            if y + self.now.y in range(20):
                                self.map[x + self.now.x][y + self.now.y] = 1
                                if y + self.now.y + 1 < 20:
                                    if self.map[x + self.now.x][y + self.now.y + 1] == 1:
                                        reach = True
            if self.now.top() + self.now.y < 1 and reach:
                self.over = True
            if reach:
                self.now = None
                self.lastmap = copy.deepcopy(self.map)
                return
            if not fall:
                return

    def clear(self):
        for y in range(20):
            clear = True
            for x in range(10):
                if self.lastmap[x][y] == 0:
                    clear = False
            if clear:
                self.score += 1
                for ny in range(y - 1, -1, -1):
                    for nx in range(10):
                        self.lastmap[nx][ny + 1] = self.lastmap[nx][ny]
                for nx in range(10):
                    self.lastmap[nx][0] = 0

    def move(self, to):
        if self.now is None:
            pass
        else:
            if to == 'Left':
                if self.now.left() + self.now.x > 0:
                    self.now.x -= 1
            if to == 'Right':
                if self.now.x + self.now.right() < 9:
                    self.now.x += 1
            if to == 'Down':
                self.drop(True)
                return
            if to == 'Up':
                test_b = copy.deepcopy(self.now)
                test_b.rotate()
                for x in range(4):
                    for y in range(4):
                        if test_b.mat[y][x] == 1:
                            if x + test_b.x in range(0, 10) and y + test_b.y in range(-4, 20):
                                if self.lastmap[x + test_b.x][y + test_b.y] == 0:
                                    if y + test_b.y + 1 < 20:
                                        if self.map[x + test_b.x][y + test_b.y + 1] == 1:
                                            pass
                                else:
                                    return
                            else:
                                return
                self.now = test_b
            self.map = copy.deepcopy(self.lastmap)
            for x in range(4):
                for y in range(4):
                    if self.now.mat[y][x] == 1:
                        if x + self.now.x in range(10):
                            if y + self.now.y in range(20):
                                self.map[x + self.now.x][y + self.now.y] = 1

    def add(self):
        for ny in range(19):
            for nx in range(10):
                self.lastmap[nx][ny] = self.lastmap[nx][ny + 1]
        for nx in range(10):
            self.lastmap[nx][19] = (nx+int(random.choice('01'))) % 2

    def get_score(self):
        return self.score

    def get_over(self):
        return self.over
