import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Initialize grid
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def draw_grid(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)


def draw_tetrimino(surface, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (tetrimino.x + x) * BLOCK_SIZE,
                    (tetrimino.y + y) * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                pygame.draw.rect(surface, tetrimino.color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)


def check_collision(tetrimino, dx=0, dy=0):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetrimino.x + x + dx
                new_y = tetrimino.y + y + dy
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or grid[new_y][new_x]:
                    return True
    return False


def merge_tetrimino(tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetrimino.y + y][tetrimino.x + x] = tetrimino.color


def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < GRID_HEIGHT:
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])


def draw_grid_blocks(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, grid[y][x], rect)
                pygame.draw.rect(surface, BLACK, rect, 1)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    current_tetrimino = Tetrimino()
    fall_time = 0
    fall_speed = 500  # Milliseconds

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(screen)
        draw_grid_blocks(screen)
        draw_tetrimino(screen, current_tetrimino)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(current_tetrimino, dx=-1):
                    current_tetrimino.x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(current_tetrimino, dx=1):
                    current_tetrimino.x += 1
                if event.key == pygame.K_DOWN and not check_collision(current_tetrimino, dy=1):
                    current_tetrimino.y += 1
                if event.key == pygame.K_UP:
                    current_tetrimino.rotate()
                    if check_collision(current_tetrimino):
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()
                if event.key == pygame.K_SPACE:
                    # Move the tetrimino down until it collides
                    while not check_collision(current_tetrimino, dy=1):
                        current_tetrimino.y += 1
                    merge_tetrimino(current_tetrimino)
                    clear_lines()
                    current_tetrimino = Tetrimino()
                    if check_collision(current_tetrimino):
                        running = False

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            fall_time = 0
            if not check_collision(current_tetrimino, dy=1):
                current_tetrimino.y += 1
            else:
                merge_tetrimino(current_tetrimino)
                clear_lines()
                current_tetrimino = Tetrimino()
                if check_collision(current_tetrimino):
                    running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()