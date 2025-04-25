import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Шрифты
font_small = pygame.font.SysFont(None, 30)
font_large = pygame.font.SysFont(None, 60)


def draw_text(text, font, color, surface, x, y):
    """Отрисовка текста на экране"""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def random_position():
    """Случайная позиция на сетке"""
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return x, y


def game_loop():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL_SIZE, 0)
    apple = random_position()
    score = 0
    speed = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        # Перемещение змейки
        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])
        snake.insert(0, new_head)

        # Съедание яблока
        if new_head == apple:
            score += 1
            apple = random_position()
            # Увеличиваем скорость каждые 5 очков
            if score % 5 == 0:
                speed += 2
        else:
            snake.pop()

        # Проверка завершения игры
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake[1:]
        ):
            return score

        # Отрисовка
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*apple, CELL_SIZE, CELL_SIZE))
        draw_text(f"Score: {score}", font_small, WHITE, screen, 10, 10)
        pygame.display.flip()
        clock.tick(speed)


def main():
    while True:
        # Экран приветствия
        screen.fill(BLACK)
        draw_text("Змейка", font_large, GREEN, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text("Нажми любую клавишу, чтобы начать", font_small, WHITE, screen, WIDTH // 2 - 130, HEIGHT // 2 + 20)
        pygame.display.flip()

        # Ожидание нажатия клавиши
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

        # Основной игровой цикл
        score = game_loop()

        # Экран конца игры
        screen.fill(BLACK)
        draw_text("Игра окончена", font_large, RED, screen, WIDTH // 2 - 150, HEIGHT // 2 - 50)
        draw_text(f"Твой счёт: {score}", font_small, WHITE, screen, WIDTH // 2 - 70, HEIGHT // 2 + 20)
        draw_text("Нажми R для рестарта или Q для выхода", font_small, WHITE, screen, WIDTH // 2 - 160, HEIGHT // 2 + 60)
        pygame.display.flip()

        # Ожидание решения игрока
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False  # рестарт
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    main()
