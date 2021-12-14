import pygame
import random
from typing import Optional, List, Tuple
import time
import random

TILE_SIZE = 20


# TODO: Spielklassen
class Item:
    def __init__(self, x: int, y: int) -> None:
        self._x: int = x
        self._y: int = y

    def occupies(self, x: int, y: int) -> bool:
        if self._x == x and self._y == y:
            return True
        else:
            return False


class Brick(Item):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(
            (50, 50, 50),
            pygame.Rect(
                self._x * TILE_SIZE,
                self._y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
        )


class Cherry(Item):

    def __init__(self, gameboard_width: int, gameboard_height: int) -> None:
        super().__init__(0, 0)
        self._width_restraint = gameboard_width - 1
        self._height_restraint = gameboard_height - 1
        self._was_eaten = -1

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(
            surface,
            (168, 36, 0),
            pygame.Rect(
                self._x * TILE_SIZE,
                self._y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
        )

    def move(self, forbidden: List[Tuple[int, int]]) -> None:
        while True:
            self._x = random.randint(0, self._width_restraint)
            self._y = random.randint(0, self._height_restraint)
            if (self._x, self._y) not in forbidden:
                print(self._x, self._y)
                self._was_eaten += 1
                return

    def get_score(self) -> int:
        return self._was_eaten


class Snake:
    def __init__(self, x: int, y: int, color: List) -> None:
        self._occupies: List[Tuple[int, int]] = []
        self._occupies.append((x, y))
        self._color = color
        self._direction = (-1, 0)
        self._grow = 0
        self.grow(3)
        self._realdirection = (0, 0)

    def get_head(self) -> Tuple[int, int]:
        return self._occupies[0]

    def set_direction(self, t: Tuple[int, int]) -> None:
        if t[0] == self._realdirection[0] * -1 and t[1] == self._realdirection[1] * -1:
            return
        self._direction = t

    def occupies(self, x: int, y: int) -> bool:
        for part in self._occupies:
            if (x, y) == part:
                return True

        return False

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(
            (20, 200, 100),
            pygame.Rect(
                self._occupies[0][0] * TILE_SIZE,
                self._occupies[0][1] * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
        )
        for x, y in self._occupies[1:]:
            # draws checkered snake
            padding = 0.1 * TILE_SIZE
            surface.fill(
                (10, 150, 70),
                pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
            )
            surface.fill(
                (20, 200, 100),
                pygame.Rect(
                    x * TILE_SIZE + padding,
                    y * TILE_SIZE + padding,
                    TILE_SIZE - padding * 2,
                    TILE_SIZE - padding * 2
                )
            )

    def grow(self, how_much: int) -> None:
        self._grow += how_much

    def step(self, forbidden: List[Tuple[int, int]]) -> bool:
        # create new head
        old_head = self._occupies[0]
        new_head = (old_head[0] + self._direction[0], old_head[1] + self._direction[1])

        # grow or not grow
        if self._grow > 0:
            self._grow -= 1
        else:
            self._occupies = self._occupies[:-1]

        # check for collision
        if new_head in forbidden or new_head in self._occupies:
            return False

        # create new snake length
        self._occupies = [new_head] + self._occupies

        # register real step
        self._realdirection = self._direction

        return True


def main() -> None:
    width = 20
    height = 15
    speed = 5

    pygame.init()
    screen = pygame.display.set_mode((
        TILE_SIZE * width,
        TILE_SIZE * height
    ))

    clock = pygame.time.Clock()

    # TODO: Spielobjekte anlegen
    wall_coordinates = [(x, y) for x in range(0, width) for y in [0, height - 1]] + [(x, y) for x in [0, width - 1] for
                                                                                     y in range(0, height)] + [(4, 4),
                                                                                                               (6, 6),
                                                                                                               (14, 11),
                                                                                                               (14, 10),
                                                                                                               (14, 9),
                                                                                                               (10, 4)]
    wall = [Brick(x, y) for (x, y) in wall_coordinates]

    starting_point = (int((width - 1) // 2), int((height - 1) // 2))
    snake = Snake(starting_point[0], starting_point[1], [125, 125, 255])

    cherry = Cherry(gameboard_width=width, gameboard_height=height)
    cherry.move(forbidden=wall_coordinates)

    # font
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 18)

    running = True

    while running:
        screen.fill((20, 20, 20))

        # TODO: Mauer zeichnen
        for brick in wall:
            brick.draw(surface=screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Spiel beenden
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                t = (0, 0)
                if event.key == pygame.K_LEFT:
                    t = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    t = (1, 0)
                elif event.key == pygame.K_UP:
                    t = (0, -1)
                elif event.key == pygame.K_DOWN:
                    t = (0, 1)
                snake.set_direction(t)

        if not running:
            break

        # TODO: Schlange bewegen
        if not snake.step(wall_coordinates):
            break
        # TODO: Schlange zeichnen

        snake.draw(surface=screen)

        # TODO: Ueberpruefen, ob die Kirsche erreicht wurde, falls ja, wachsen und Kirsche bewegen.
        head = snake.get_head()
        if cherry.occupies(head[0], head[1]):
            cherry.move(forbidden=wall_coordinates)
            snake.grow(4)

        # TODO: Kirsche zeichnen
        cherry.draw(surface=screen)

        #  score
        screen.blit(font.render(f"Score: {cherry.get_score()}", True, (255, 255, 255)), (1, 1))

        pygame.display.flip()
        clock.tick(speed)

    screen.blit(font.render(f"--GAME OVER-- final Score: {cherry.get_score()}", True, (255, 255, 255)), (1, 1))
    pygame.display.flip()
    clock.tick(1)

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
