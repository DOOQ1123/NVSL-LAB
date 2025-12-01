import pygame
import random
import sys

# 게임 설정
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.25
FLAP_STRENGTH = -5
PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_SPEED = 3
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# 새 클래스 정의
class Bird:
    def __init__(self):
        self.original_image = pygame.image.load('bird.png')
        self.scaled_image = pygame.transform.scale(self.original_image, (50, 40))  # 새의 크기 조절
        self.rect = self.scaled_image.get_rect()
        self.rect.center = (50, HEIGHT // 2)
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def draw(self, screen):
        screen.blit(self.scaled_image, self.rect)

# 파이프 클래스 정의
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.gap_y = random.randint(PIPE_GAP, HEIGHT - PIPE_GAP)
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = HEIGHT - self.gap_y - PIPE_GAP // 2
        self.width = PIPE_WIDTH
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, BLUE, (self.x, self.gap_y + PIPE_GAP // 2, self.width, self.bottom_height))

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
bird = Bird()
pipes = []
score = 0
font = pygame.font.SysFont(None, 40)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # 게임 로직 업데이트
    bird.update()

    # 파이프 생성 및 이동
    if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
        pipes.append(Pipe())

    for pipe in pipes:
        pipe.move()
        if pipe.x + PIPE_WIDTH < bird.rect.centerx and not pipe.passed:
            pipe.passed = True
            score += 1
        if pipe.x + PIPE_WIDTH < 0:
            pipes.remove(pipe)

    # 충돌 검사
    for pipe in pipes:
        if (bird.rect.colliderect(pipe.x, 0, PIPE_WIDTH, pipe.top_height) or
            bird.rect.colliderect(pipe.x, pipe.gap_y + PIPE_GAP // 2, PIPE_WIDTH, pipe.bottom_height) or
            bird.rect.top < 0 or bird.rect.bottom > HEIGHT):
            running = False
            break

    # 그리기
    screen.fill(WHITE)
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    # 점수 표시
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
