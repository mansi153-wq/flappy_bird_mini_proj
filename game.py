import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Square")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game variables
gravity = 0.5
jump_strength = -10
pipe_gap = 150
pipe_width = 70
pipe_velocity = 3

# Font
font = pygame.font.SysFont(None, 48)

# Square (player) class
class Square:
    def __init__(self):
        self.size = 40
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.velocity += gravity
        self.y += self.velocity
        self.rect.y = int(self.y)

    def jump(self):
        self.velocity = jump_strength

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - pipe_gap - 100)
        self.top_rect = pygame.Rect(self.x, 0, pipe_width, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + pipe_gap, pipe_width, HEIGHT - self.height - pipe_gap)

    def update(self):
        self.x -= pipe_velocity
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def off_screen(self):
        return self.x + pipe_width < 0

    def collide(self, square):
        return self.top_rect.colliderect(square.rect) or self.bottom_rect.colliderect(square.rect)

# Function to display text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Main game function
def main():
    square = Square()
    pipes = []
    score = 0
    frame_count = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    square.jump()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            square.update()
            frame_count += 1

            # Generate new pipes
            if frame_count % 90 == 0:
                pipes.append(Pipe(WIDTH))

            # Update and draw pipes
            for pipe in pipes[:]:
                pipe.update()
                pipe.draw()
                if pipe.collide(square):
                    game_over = True
                if pipe.x + pipe_width < square.x and not hasattr(pipe, 'scored'):
                    score += 1
                    pipe.scored = True
                if pipe.off_screen():
                    pipes.remove(pipe)

            # Check for collision with top and bottom of the screen
            if square.y <= 0 or square.y + square.size >= HEIGHT:
                game_over = True

            square.draw()
            draw_text(f"Score: {score}", font, (0, 0, 0), screen, WIDTH // 2, 50)
        else:
            draw_text("Game Over", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Final Score: {score}", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
            draw_text("Press R to Restart", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
