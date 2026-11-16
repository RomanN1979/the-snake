from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет головы змейки
HEAD_COLOR = (0, 100, 0)

# Скорость движения змейки:
SPEED = 5

# Центр игрового поля
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка:  (Для выхода нажмите ESC)')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self, color=BORDER_COLOR) -> None:
        self.position = SCREEN_CENTER
        self.body_color = color

    def draw(
        self,
        position: tuple[int, int] | None = None,
        body_color: tuple[int, int, int] | None = None,
        border_color: tuple[int, int, int] | None = None,
    ) -> None:
        """
        Метод отрисовки базового класса,
        рисует прямоугольник в заданной позиции с заданным цветом тела
        и цветом бордюра.
        Args:
            position (tuple(int, int)): левый верхний угол;
                по умолчанию self.position.
            body_color (tuple(int, int, int)): цвет заливки;
                по умолчанию self.body_color.
            border_color (tuple(int, int, int)): цвет рамки;
                по умолчанию BORDER_COLOR.
        """
        rect = pg.Rect(position or self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color or self.body_color, rect)
        pg.draw.rect(screen, border_color or BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс яблоко.
    Args:
       color (tuple): цвет объекта, по умолчанию APPLE_COLOR.
    """

    def __init__(
        self,
        occupied_positions: list[tuple[int, int]] | None = None,
        color: tuple[int, int, int] = APPLE_COLOR,
    ) -> None:

        super().__init__(color)
        self.randomize_position(occupied_positions)

    def randomize_position(self,
                           occupied_positions: list[tuple] | None = None
                           ) -> None:
        """
        Генерирует случайное расположение яблока на игровом поле
        с исключением недопустимых значений.
        Args:
            occupied_positions (list): Список занятых позиций.
        """
        occupied_positions = occupied_positions or []

        while True:
            self.position = (
                randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE,
            )
            # Проверка на допустимое значение.
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        super().draw()


class Snake(GameObject):
    """
    Класс змейка.
    Args:
       color (tuple[int, int, int]): цвет объекта, по умолчанию SNAKE_COLOR.
    """

    def __init__(self, color: tuple[int, int, int] = SNAKE_COLOR) -> None:
        super().__init__(color)
        self.positions: list = []
        self.reset()

    def reset(self) -> None:
        """Возврат змейки в начальное состояние."""
        self.length = 1  # Длинна змейки.
        self.positions.clear()
        self.positions.append(self.position)  # Список сегментов.
        self.direction = RIGHT  # Tекущее направление движения.
        self.next_direction = None  # Следующее направление.
        self.last = None  # Координаты последнего сегмента перед его удалением.

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает текущую координату головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновление направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """
        Расчет следующей координаты при движении
        змейки с учетом направления.
        """
        head_x, head_y = self.get_head_position()
        # Новая позиция головы: шаг на одну клетку в текущем направлении
        self.update_direction()
        dx, dy = self.direction  # Направление движения хранится кака кортеж
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)  # Новая голова — в начало списка
        # Если змейка длиннее нужного — убираем хвост и запоминаем его
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        # Отрисовка всего тела кроме головы
        for position in self.positions[1:]:
            super().draw(position)
        # Отрисовка головы змейки
        super().draw(self.get_head_position(), HEAD_COLOR)
        # Затирание старой позиции хвоста, если змейка сдвинулась.
        if self.last is not None:
            super().draw(self.last,
                         BOARD_BACKGROUND_COLOR,
                         BOARD_BACKGROUND_COLOR)


def handle_keys(game_object) -> None:
    """Обработка действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главнвя функция."""
    screen.fill(BOARD_BACKGROUND_COLOR)  # Первичная заливка

    # Создаем экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)

    apple.draw()
    while True:
        handle_keys(snake)
        snake.move()
        snake.draw()
        head_pos = snake.get_head_position()
        if head_pos == apple.position:  # Змейка съела яблоко.
            snake.length += 1
            # Яблоко не должно попасть на тело змейки.
            apple.randomize_position(snake.positions)
            apple.draw()
        elif head_pos in snake.positions[4:]:  # Столкновения змейки с собой.
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)
            apple.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
