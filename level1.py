import pygame
import random


class Cell:
    def __init__(self, sc, x, y, cell_size):
        self.sc = sc
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.visited = False
        self.walls = {"top": True, "left": True, "right": True, "bottom": True}
        self.end = None

    def draw_current_cell(self):
        self.visited = True
        pygame.draw.rect(self.sc, "#25f792",
                         (self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size))

    def draw(self):
        if not self.visited:
            pygame.draw.rect(self.sc, "black",
                             (self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size))
        else:
            if self.end:
                pygame.draw.rect(self.sc, "#ff5d00", (self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size))

        if self.walls["top"]:
            pygame.draw.line(self.sc, "#254c69", (self.x * self.cell_size, self.y * self.cell_size),
                             (self.x * self.cell_size + self.cell_size, self.y * self.cell_size), 2)
        if self.walls["bottom"]:
            pygame.draw.line(self.sc, "#254c69",
                             (self.x * self.cell_size, self.y * self.cell_size + self.cell_size),
                             (self.x * self.cell_size + self.cell_size, self.y * self.cell_size + self.cell_size), 2)
        if self.walls["left"]:
            pygame.draw.line(self.sc, "#254c69", (self.x * self.cell_size, self.y * self.cell_size),
                             (self.x * self.cell_size, self.y * self.cell_size + self.cell_size), 2)
        if self.walls["right"]:
            pygame.draw.line(self.sc, "#254c69",
                             (self.x * self.cell_size + self.cell_size, self.y * self.cell_size),
                             (self.x * self.cell_size + self.cell_size, self.y * self.cell_size + self.cell_size), 2)

    def check_next(self, map: list):
        next_cells = []

        if self.x + 1 < len(map[self.y]) and not map[self.y][self.x + 1].visited:
            next_cells.append(map[self.y][self.x + 1])
        if self.x - 1 >= 0 and not map[self.y][self.x - 1].visited:
            next_cells.append(map[self.y][self.x - 1])
        if self.y + 1 < len(map) and not map[self.y + 1][self.x].visited:
            next_cells.append(map[self.y + 1][self.x])
        if self.y - 1 >= 0 and not map[self.y - 1][self.x].visited:
            next_cells.append(map[self.y - 1][self.x])


        if not next_cells:
            if game.history:
                game.current = game.map[game.history[-1][1]][game.history[-1][0]]
                del game.history[-1]
                return False
            return True

        self.new = next_cells[random.randint(0, len(next_cells) - 1)]
        self.remove_walls()
        for i in range(len(map)):
            for cell in range(len(map[i])):
                if map[i][cell] == self.new:
                    map[i][cell].visited = True
        game.current = self.new
        game.map = map

    def remove_walls(self):
        dx = game.current.x - self.new.x
        if dx == 1:
            game.current.walls["left"] = False
            self.new.walls["right"] = False
        elif dx == -1:
            game.current.walls["right"] = False
            self.new.walls["left"] = False
        dy = game.current.y - self.new.y
        if dy == 1:
            game.current.walls["top"] = False
            self.new.walls["bottom"] = False
        elif dy == -1:
            game.current.walls["bottom"] = False
            self.new.walls["top"] = False


def keyboard_control():
    key = pygame.key.get_pressed()
    if key[pygame.K_w] or key[pygame.K_UP]:
        return 1
    elif key[pygame.K_s] or key[pygame.K_DOWN]:
        return 2
    elif key[pygame.K_a] or key[pygame.K_LEFT]:
        return 3
    elif key[pygame.K_d] or key[pygame.K_RIGHT]:
        return 4
    else:
        return None


class Game:
    def __init__(self, fps: int):
        self.col = 30
        self.__size = random.randint(20, 25) * self.col, random.randint(20, 25) * self.col  # разрешение экрана
        self.__fps = fps  # fps
        pygame.init()
        self.__screen = pygame.display.set_mode(self.__size)  # отрисовка рабочего окна
        self.__clock = pygame.time.Clock()  # fps
        self.map = [[Cell(self.__screen, j, i, self.col) for j in range(self.__size[0] // self.col)] for i in
                    range(self.__size[1] // self.col)]
        self.current = self.map[0][0]
        self.map[0][0].visited = True
        self.history = list()
        self.history.append((0, 0))
        self.map[-1][-1].end = True

    def run(self) -> None:
        """
        Основной цикл игры
        :return: None
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.__screen.fill('#69afff')
            for i in self.map:
                for cell in i:
                    if cell != self.current:
                        cell.draw()

            result = self.current.check_next(self.map)
            if result != False:
                self.history.append((self.current.x, self.current.y))
            if result:
                break
            self.current.draw_current_cell()
            pygame.display.update()
            pygame.display.flip()
            self.__clock.tick(self.__fps)

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.__screen.fill('#69afff')
            for i in self.map:
                for cell in i:
                    if cell != self.current:
                        cell.draw()
            if self.current == self.map[-1][-1]:
                break

            result = keyboard_control()
            if result == 1:
                y, x = self.find_coord_cur()
                if self.current.y - 1 >= 0 and not self.current.walls["top"]:
                    self.current = self.map[y - 1][x]
            elif result == 2:
                y, x = self.find_coord_cur()
                if self.current.y + 1 < len(self.map) and not self.current.walls["bottom"]:
                    self.current = self.map[y + 1][x]
            elif result == 3:
                y, x = self.find_coord_cur()
                if self.current.x - 1 >= 0 and not self.current.walls["left"]:
                    self.current = self.map[y][x - 1]
            elif result == 4:
                y, x = self.find_coord_cur()
                if self.current.x + 1 < len(self.map[self.current.y]) and not self.current.walls["right"]:
                    self.current = self.map[y][x + 1]


            self.current.draw_current_cell()
            pygame.display.update()
            pygame.display.flip()
            self.__clock.tick(self.__fps)

    def find_coord_cur(self):
        for i in range(len(self.map)):
            for cell in range(len(self.map[i])):
                if self.map[i][cell] == self.current:
                    return i, cell



game = Game(30)

