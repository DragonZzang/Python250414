import pygame
import time
import random

# 초기화
pygame.init()

# 색상 정의
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 화면 크기
width = 800
height = 600

# 게임 화면 생성
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('뱀 게임: 사람 vs 기계')

# 시계 객체
clock = pygame.time.Clock()

# 뱀 크기
snake_block = 10
snake_speed = 15

# 폰트 설정
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# 점수 표시 함수
def your_score(player_score, ai_score):
    value = score_font.render(f"사람 점수: {player_score}  기계 점수: {ai_score}", True, yellow)
    game_display.blit(value, [0, 0])

# 뱀 그리기 함수
def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(game_display, color, [x[0], x[1], snake_block, snake_block])

# 메시지 표시 함수
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [width / 6, height / 3])

# 게임 루프
def game_loop():
    game_over = False
    game_close = False

    # 사람 뱀 초기 위치
    x1 = width / 4
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1

    # 기계 뱀 초기 위치
    ai_x = 3 * width / 4
    ai_y = height / 2
    ai_snake_list = []
    ai_length_of_snake = 1

    # 음식 위치
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    player_score = 0
    ai_score = 0

    while not game_over:

        while game_close:
            game_display.fill(blue)
            message("게임 오버! 다시 시작하려면 C를 누르세요. 종료하려면 Q를 누르세요.", red)
            your_score(player_score, ai_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 사람 뱀 이동
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # 기계 뱀 이동 (간단한 알고리즘)
        if ai_x < foodx:
            ai_x += snake_block
        elif ai_x > foodx:
            ai_x -= snake_block
        if ai_y < foody:
            ai_y += snake_block
        elif ai_y > foody:
            ai_y -= snake_block

        # 화면 업데이트
        game_display.fill(blue)
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block, snake_block])

        # 사람 뱀 업데이트
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # 기계 뱀 업데이트
        ai_snake_head = [ai_x, ai_y]
        ai_snake_list.append(ai_snake_head)
        if len(ai_snake_list) > ai_length_of_snake:
            del ai_snake_list[0]

        for x in ai_snake_list[:-1]:
            if x == ai_snake_head:
                game_close = True

        # 뱀과 음식 충돌 처리
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            player_score += 1

        if ai_x == foodx and ai_y == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            ai_length_of_snake += 1
            ai_score += 1

        # 뱀 그리기
        our_snake(snake_block, snake_list, black)
        our_snake(snake_block, ai_snake_list, green)
        your_score(player_score, ai_score)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()