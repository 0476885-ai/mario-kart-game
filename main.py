import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TRACK_COLOR = (100, 100, 100)
CAR_COLOR = (255, 0, 0)

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Kart Game")

# Load player image
player_image = pygame.Surface((50, 30))
player_image.fill(CAR_COLOR)

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
    
    def draw(self):
        screen.blit(player_image, (self.x, self.y))
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

# Main game function
def game_loop():
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Drawing
        screen.fill(TRACK_COLOR)
        player.draw()
        pygame.display.flip()  
        
        clock.tick(60)  # Frame rate
    
    pygame.quit()

if __name__ == "__main__":
    game_loop()