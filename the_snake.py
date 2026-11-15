from random import randint

import pygame


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

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс."""

    def __init__(self, color=BORDER_COLOR):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def draw(self):
        """
        Метод отрисовки базового класса,
        переопределяется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс яблоко.
    Args:
       color (tuple): цвет объекта, по умолчанию APPLE_COLOR.
    """

    def __init__(self, color=APPLE_COLOR):
        super().__init__(color)
        self.randomize_position()

    def randomize_position(self, invalid_value=None):
        """
        Генерирует случайное расположение яблока на игровом поле
        с исключением недопустимых значений.
        Args:
            invalid_value (list): Список недопустимых значений.
        """
        if invalid_value is None:
            invalid_value = []
        while True:
            self.position = (randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
                             * GRID_SIZE,
                             randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)
                             * GRID_SIZE)
            # Проверка на допустимое значение.
            if self.position not in invalid_value:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс змейка.
    Args:
       color (tuple): цвет объекта, по умолчанию SNAKE_COLOR.
    """

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(color)
        self.length = 1  # Длинна змейки.
        self.positions = [self.position]  # Список сегментов.
        self.direction = RIGHT  # Tекущее направление движения.
        self.next_direction = None  # Следующее направление.
        self.last = None  # Координаты последнего сегмента перед его удалением.

    def get_head_position(self):
        """Возвращает текущую координату головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновление направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Расчет следующей координаты при движении
        змейки с учетом направления.
        """
        head_pos = self.get_head_position()
    # Новая позиция головы: шаг на одну клетку в текущем направлении
        self.update_direction()
        dx, dy = self.direction  # Направление движения хранится кака кортеж
        new_head = (
            (head_pos[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_pos[1] + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)  # Новая голова — в начало списка
        # Если змейка длиннее нужного — убираем хвост и запоминаем его
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Возврат змейки в начальное состояние."""
        self.length = 1
        self.positions.clear()
        self.positions.append(self.position)
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        # Отрисовка кроме последнего сегмента
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента если он есть
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главнвя функция."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Создаем экземпляры классов.
    apple = Apple()
    snake = Snake()

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
        if snake.length > 4:
            if head_pos in snake.positions[1:]:  # Столкновения змейки с собой.
                screen.fill(BOARD_BACKGROUND_COLOR)
                snake.reset()
                apple.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
