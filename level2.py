import pygame
from pathlib import Path
from typing import Tuple, ClassVar

TILE_SIZE = 32


class Labyrinth:
    """
    Класс создания карты
    """
    def __init__(self, free_tiles, finish_tile):
        self.maps_dir = Path('map')
        self.map = list()  # матрица карты
        with open(self.maps_dir) as input_file:
            self.map = [list(map(int, line.split())) for line in input_file]
            self.height = len(self.map)
            self.width = len((self.map[0]))
            self.tile_size = TILE_SIZE
            self.free_tiles = free_tiles  # список номеров клеток, по которым можно ходить
            self.finish_tile = finish_tile  # номер клетки в которой находится выход с карты

    def render(self, screen: ClassVar) -> None:
        """
        Отрисовывает карту на главном экране
        :param screen: экземпляр главного экрана
        :return: None
        """
        color = {0: (0, 0, 0), 1: (61, 74, 191), 2: (50, 50, 50)}  # цвета карты
        for y in range(self.height):
            for x in range(self.width):
                if self.get_tile_id((x, y)) == 2:
                    pygame.draw.rect(game1.screen, color[self.get_tile_id((x, y))],
                                     (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(game1.screen, color[self.get_tile_id((x, y))], (x * self.tile_size, y * self.tile_size,
                                    self.tile_size, self.tile_size), 1)


    def get_tile_id(self, position: Tuple) -> int:
        """
        Возвращает id тайла на карте (номер)
        :param position: координаты тайла
        :return: int
        """
        return self.map[position[1]][position[0]]

    def if_free(self, position: Tuple):
        """
        Проверяет можно ли ходить по клетке
        :param position: координаты тайла
        :return: bool
        """
        if self.get_tile_id(position) in self.free_tiles:
            if self.get_tile_id(position) == 2:
                return 5
            return 1
        return False

class Hero:
    """
    Класс создания персонажа
    """
    def __init__(self, position: Tuple):
        self.x, self.y = position  # позиция спауна игрока

    def get_position(self) -> Tuple[int, int]:
        """
        Возвращает текущую позицию игрока
        :return: tuple
        """
        return self.x, self.y

    def set_position(self, position: Tuple) -> None:
        """
        Задаёт новую позицию для игрока
        :param position: новые координаты
        :return: None
        """
        self.x, self.y = position

    def render(self, screen, color) -> None:
        """
        Отрисовка игрока
        :param screen: экземпляр главного экрана
        :return: None
        """
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, color, center, TILE_SIZE // 2)


class Game:
    def __init__(self, height: int, weight: int, fps: int):
        self.__size = self.height, self.weight = height, weight  # разрешение экрана
        self.__fps = fps  # fps
        pygame.init()
        self.screen = pygame.display.set_mode(self.__size)  # отрисовка рабочего окна
        self.__clock = pygame.time.Clock()  # fps

        self.labyrinth = Labyrinth([0, 2], 2)
        self.hero = Hero((7, 7))
        self.opponent = Hero((3, 3))

    def run(self) -> None:
        """
        Основной цикл игры
        :return: None
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill('black')
            self.labyrinth.render(self.screen)  # рисуем карту
            self.hero.render(self.screen, "#f8fc00")  # рисуем персонажа
            if self.update_hero():
                break
            self.opponent.render(self.screen, "#0400fc")  # рисуем персонажа
            self.update_opp()
            if self.check_loss():
                break
            pygame.display.flip()
            self.__clock.tick(self.__fps)

    def update_hero(self):
        """
        Обновление позиции героя
        :return: None
        """
        next_x, next_y = self.hero.get_position()
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            next_y -= 1
        if key[pygame.K_s]:
            next_y += 1
        if key[pygame.K_a]:
            next_x -= 1
        if key[pygame.K_d]:
            next_x += 1
        if self.labyrinth.if_free((next_x, next_y)) == 1:
            # если тайл свободен, то задаём новое положение персонажу
            self.hero.set_position((next_x, next_y))
        elif self.labyrinth.if_free((next_x, next_y)) == 5:
            return True

    def update_opp(self):
        if self.opponent.x >= 3 and self.opponent.x < 11 and self.opponent.y == 3:
            if self.labyrinth.map[self.opponent.y][self.opponent.x + 1] == 0:
                self.opponent.x += 1
                return
        if self.opponent.x == 3:
            if self.labyrinth.map[self.opponent.y - 1][self.opponent.x] == 0:
                self.opponent.y -= 1
                return
        if self.opponent.x > 3 and self.opponent.x <= 11 and self.opponent.y == 11:
            if self.labyrinth.map[self.opponent.y][self.opponent.x - 1] == 0:
                self.opponent.x -= 1
                return
        if self.opponent.x == 11:
            if self.labyrinth.map[self.opponent.y + 1][self.opponent.x] == 0:
                self.opponent.y += 1
                return

    def check_loss(self):
        if self.opponent.x == self.hero.x and self.opponent.y == self.hero.y:
            return True
        return False

game1 = Game(480, 480, 15)
