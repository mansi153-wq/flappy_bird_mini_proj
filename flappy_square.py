import pygame
import sys
import random
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
clock = pygame.time.Clock()
FPS = 60
gravity = 0.5
jump_strength = -10
pipe_gap = 200
pipe_width = 95
pipe_velocity = 3
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)
THEMES = {
    "Night": {
        "background": "n.png",
        "pipe": "pipe.png",
        "bird": "birdie.png"
    },
    "Day": {
        "background": "day_back.png",
        "pipe": "pipe.png",
        "bird": "bird.png"
    }
}
theme_names = list(THEMES.keys())
current_theme_index = 0
def load_theme(theme_name):
    theme = THEMES[theme_name]
    bg_img = pygame.image.load(theme["background"]).convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    p_img = pygame.image.load(theme["pipe"]).convert_alpha()
    p_img = pygame.transform.scale(p_img, (pipe_width, 450))
    b_img = pygame.image.load(theme["bird"]).convert_alpha()
    b_img = pygame.transform.scale(b_img, (50, 50))
    return bg_img, p_img, b_img
jump_sound = pygame.mixer.Sound("sound.wav")
point_sound = pygame.mixer.Sound("point.mp3")
die_sound= pygame.mixer.Sound("die.mp3")

def draw_background():
    screen.blit(background_img, (0, 0))

def draw_text(text, x, y, font=font, color=(0, 0, 0)):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x, y))
    screen.blit(rendered, rect)

def draw_scoreboard(score):
    box_width, box_height = 100, 60
    scoreboard_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    scoreboard_surface.fill((WHITE))
    screen.blit(scoreboard_surface, (10, 10))
    border_rect = pygame.Rect(10, 10, box_width, box_height)
    pygame.draw.rect(screen, (0, 0, 0), border_rect, 3)
    rendered = font.render(f"Score: {score}", True, (BLACK))
    screen.blit(rendered, (20, 25))

class Bird:
    def __init__(self):
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += gravity
        self.rect.y += int(self.velocity)

    def jump(self):
        self.velocity = jump_strength

    def draw(self):
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - pipe_gap - 100)
        self.top_rect = pygame.Rect(x, 0, pipe_width, self.height)
        self.bottom_rect = pygame.Rect(x, self.height + pipe_gap, pipe_width, HEIGHT - self.height - pipe_gap)
        self.scored = False

    def update(self):
        self.x -= pipe_velocity
        self.top_rect.x = self.bottom_rect.x = int(self.x)

    def draw(self):
        # Draw top pipe (flipped)
        top_pipe_img = pygame.transform.flip(pipe_img, False, True)
        top_pipe_y = self.height - pipe_img.get_height()
        screen.blit(top_pipe_img, (self.x, top_pipe_y))
        # Draw bottom pipe
        screen.blit(pipe_img, (self.x, self.height + pipe_gap))

    def off_screen(self):
        return self.x + pipe_width < 0

    def collide(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

def theme_menu():
    selected = 0
    while True:
        screen.fill(BLACK)
        draw_text("Choose Theme", WIDTH // 2, 100, big_font, BLACK)
        for i, name in enumerate(theme_names):
            color = GREEN if i == selected else WHITE
            draw_text(name, WIDTH // 2, 200 + i * 60, big_font, color)
        draw_text("Use UP/DOWN to select, ENTER to start", WIDTH // 2, HEIGHT - 80, font, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(theme_names)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(theme_names)
                if event.key == pygame.K_RETURN:
                    return theme_names[selected]

def main():
    global background_img, pipe_img, bird_img
  
    chosen_theme = theme_menu()
    background_img, pipe_img, bird_img = load_theme(chosen_theme)
    
 
    draw_background()
    draw_text("Get Ready!", WIDTH // 2, HEIGHT // 2, big_font, GREEN)
    pygame.display.flip()
    pygame.time.wait(5000)  # Wait for 5000 milliseconds (5 seconds)

    bird = Bird()
    pipes = []
    score = 0
    frame_count = 0
    game_over = False

    while True:
        clock.tick(FPS)
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                    jump_sound.play()
                if event.key == pygame.K_r and game_over:
                    return main()
                

        if not game_over:
            bird.update()
            frame_count += 1

            if frame_count % 90 == 0:
                pipes.append(Pipe(WIDTH))

            for pipe in pipes[:]:
                pipe.update()
                pipe.draw()
                if pipe.collide(bird):
                    game_over = True
                    die_sound.play()
                if pipe.x + pipe_width < bird.rect.x and not pipe.scored:
                    score += 1
                    pipe.scored = True
                    point_sound.play()
                if pipe.off_screen():
                    pipes.remove(pipe)

            if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
                game_over = True

            bird.draw()
            draw_scoreboard(score)
        else:
            draw_text("opps", WIDTH // 2, HEIGHT // 2 - 100, big_font)
            draw_text("Game Over", WIDTH // 2, HEIGHT // 2 - 50, big_font)
            draw_text(f"Final Score: {score}", WIDTH // 2, HEIGHT // 2, big_font)
            draw_text("Press R to Restart", WIDTH // 2, HEIGHT // 2 + 50, font)

        pygame.display.flip()

if __name__ == "__main__":
    main()
