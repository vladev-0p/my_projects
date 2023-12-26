import pygame
import sys
import random

pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLUE = (0, 250, 255)
BLACK = (60, 70, 50)
YELLOW = (255, 207, 64)
GREEN = (34, 139, 34)
RED = (255, 0, 0)

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ПакМАН")

smile = pygame.image.load("smile.png")  # Заменяем переменную и название изображения на свои
smile = pygame.transform.scale(smile, (20, 20))  # Шарик размером 20x20 пикселей
burger_img = pygame.image.load("hamburger.png")
burger_img = pygame.transform.scale(burger_img, (20, 20))

rock_img = pygame.image.load("rock.png")
rock_img = pygame.transform.scale(rock_img, (20, 20))

start_time = pygame.time.get_ticks()
# Определение класса игрока
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def move_left(self):
        if self.x > 0:
            self.x -= 5

    def move_right(self):
        if self.x < SCREEN_WIDTH - 20:
            self.x += 5

    def move_up(self):
        if self.y > 0:
            self.y -= 5

    def move_down(self):
        if self.y < SCREEN_HEIGHT - 20:
            self.y += 5


# Определение класса Бургер
class Burgerclass:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 20)
        self.y = random.randint(0, SCREEN_HEIGHT - 20)

    def redraw(self):
        screen.blit(burger_img, (self.x, self.y))
        # pygame.draw.rect(screen, GREEN, (self.x, self.y, 20, 20))


class Blockers:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - 20)
        self.y = random.randint(0, SCREEN_HEIGHT - 20)

    def redraw(self):
        screen.blit(rock_img, (self.x, self.y))


player = Player()
burger_list = []
rock_list = []
for _ in range(random.randint(3, 5)):  # Создаем 3 камней
    rock = Blockers()
    rock_list.append(rock)

for _ in range(random.randint(8, 12)):  # Создаем 10 бургеров
    burger = Burgerclass()
    burger_list.append(burger)

clock = pygame.time.Clock()

restart = False
score = 0
score_rock=0
while True:
    screen.fill(BLACK)
    # Рассчитываем прошедшее время
    elapsed_time = pygame.time.get_ticks() - start_time

    # Преобразуем время в секунды
    seconds = elapsed_time // 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart = True
            start_time=pygame.time.get_ticks()


    # Отображаем время на экране

    if restart:
        seconds=0
        score = 0
        score_rock = 0
        player = Player()
        burger_list = []
        rock_list = []
        for _ in range(random.randint(8, 10)):
            rock = Blockers()
            rock_list.append(rock)
        for _ in range(random.randint(8, 15)):
            burger = Burgerclass()
            burger_list.append(burger)
        restart = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_UP]:
        player.move_up()
    if keys[pygame.K_DOWN]:
        player.move_down()

    screen.fill(BLACK)

    for burger in burger_list:
        burger.redraw()
        # Проверяем, столкнулся ли игрок с камнем
        if (
                player.x < burger.x + 20
                and player.x + 20 > burger.x
                and player.y < burger.y + 20
                and player.y + 20 > burger.y
        ):
            burger_list.remove(burger)
            score += 1
    for rock in rock_list:
        rock.redraw()
        if (
                player.x < rock.x + 20
                and player.x + 20 > rock.x
                and player.y < rock.y + 20
                and player.y + 20 > rock.y
        ):
            rock_list.remove(rock)
            score_rock -= 1

    font = pygame.font.SysFont('callibri', 25)
    text = font.render("{}".format(seconds), True, BLUE)
    timer = font.render('Timer', True, BLUE)
    score_count = font.render("Result : " + str(score) +'  ', True, BLUE)
    score_rocks = font.render(str(score_rock), True, RED )
    x=SCREEN_WIDTH // 2
    screen.blit(timer,(20,20))
    screen.blit(text,(27+timer.get_width(),20))
    screen.blit(score_count, (x-6, 25))
    screen.blit(score_rocks,(x+score_count.get_width(),25))
    # pygame.draw.rect(screen, YELLOW, (player.x, player.y, 20, 20))
    screen.blit(smile, (player.x,
                        player.y))  # отображение изображения вместо прямоугольника Заменяем переменную и название изображения на свои
    pygame.display.update()

    clock.tick(60)  # cкорость движения
