import pygame
from random import randint

# Инициализация pygame
pygame.init()

# Установка разрешения экрана
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# Установка цвета фона
screen.fill((0, 0, 0))

circle_radius = 5
circle_count = 20

circles = []
for i in range(circle_count):
    circles.append({
        "circle_x": randint(0, screen_width - circle_radius), 
        "circle_y": randint(0, screen_height - circle_radius),
        "velocity_x": randint(-5, 5), 
        "velocity_y": randint(-5, 5),
        "circle_radius": circle_radius
    })
    
print(circles)

# Функция для отрисовки круга
def draw_circle(x, y):
    pygame.draw.circle(screen, (255, 255, 255), (x, y), circle_radius)
    pygame.draw.rect(screen, (255, 255, 255), rect=3, border_radius=circle_radius)

# Основной цикл игры
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    for i in range(len(circles)-1):
        # Обновление положения круга
        circles[i]["circle_x"] += circles[i]["velocity_x"]
        circles[i]["circle_y"] += circles[i]["velocity_y"]

        # Отскок от границ экрана
        if circles[i]["circle_x"] <= circles[i]["circle_radius"] or\
                circles[i]["circle_x"] >= screen_width - circles[i]["circle_radius"]:
            circles[i]["velocity_x"] = -circles[i]["velocity_x"]
        
        if circles[i]["circle_y"] <= circles[i]["circle_radius"] or\
                circles[i]["circle_y"] >= screen_height - circles[i]["circle_radius"]:
            circles[i]["velocity_y"] = -circles[i]["velocity_y"]

        # Отрисовка круга
        draw_circle(circles[i]["circle_x"], circles[i]["circle_y"])

    pygame.display.update()
    clock.tick(60)  # FPS

    # Обработка событий выхода из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

