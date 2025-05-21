import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
FPS = 60
GRAVITY = 0.8
JUMP_SPEED = -15
GROUND_HEIGHT = 80

# Colors
BACKGROUND_COLOR = (20, 20, 30)
GROUND_COLOR = (50, 50, 70)
PLAYER_COLOR = (240, 60, 60)
OBSTACLE_COLOR = (220, 220, 220)
TEXT_COLOR = (185, 185, 245)

# Setup the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash - Pygame")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Segoe UI", 30, bold=True)

# Sound setup
try:
    jump_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound('jump.wav')))
except:
    jump_sound = None

# Player class
class Player:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = 100
        self.y = HEIGHT - GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.on_ground = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        if self.y >= HEIGHT - GROUND_HEIGHT - self.height:
            self.y = HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
            if jump_sound:
                jump_sound.play()

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=8)


# Obstacle class
class Obstacle:
    def __init__(self, x):
        self.width = 30
        self.height = 40
        self.x = x
        self.y = HEIGHT - GROUND_HEIGHT - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, speed):
        self.x -= speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        points = [
            (self.x, self.y + self.height),
            (self.x + self.width // 2, self.y),
            (self.x + self.width, self.y + self.height),
        ]
        pygame.draw.polygon(surface, OBSTACLE_COLOR, points)

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.obstacle_timer = 0
        self.obstacle_interval = 1500  # milliseconds
        self.speed = 7
        self.score = 0
        self.running = True
        self.game_over = False
        self.last_time = pygame.time.get_ticks()

    def reset(self):
        self.player = Player()
        self.obstacles.clear()
        self.score = 0
        self.game_over = False
        self.last_time = pygame.time.get_ticks()

    def spawn_obstacle(self):
        x = WIDTH + 50
        obstacle = Obstacle(x)
        self.obstacles.append(obstacle)

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.game_over:
            self.player.update()

            # Spawn obstacles
            if current_time - self.obstacle_timer > self.obstacle_interval:
                self.spawn_obstacle()
                self.obstacle_timer = current_time

            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update(self.speed)
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)

                # Collision check
                if self.player.rect.colliderect(obstacle.rect):
                    self.game_over = True

            # Update score
            self.score += (current_time - self.last_time) / 1000
            self.last_time = current_time

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)

        # Draw ground
        pygame.draw.rect(surface, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT), border_radius=10)

        # Draw player
        self.player.draw(surface)

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface)

        # Draw score
        score_surface = font.render(f"Score: {int(self.score)}", True, TEXT_COLOR)
        surface.blit(score_surface, (10, 10))

        if self.game_over:
            text_surface = font.render("Game Over! Press SPACE to restart", True, (255, 100, 100))
            surface.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - text_surface.get_height()//2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.player.jump()

def main():
    game = Game()

    while game.running:
        game.handle_events()
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

 