import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TRACK_COLOR = (34, 139, 34)
GRASS_COLOR = (0, 100, 0)
ROAD_COLOR = (100, 100, 100)
CAR_WIDTH = 30
CAR_HEIGHT = 20
FPS = 60

# Track waypoints for AI to follow
TRACK_WAYPOINTS = [
    (600, 100), (900, 150), (1000, 400), (900, 700),
    (600, 750), (300, 700), (200, 400), (300, 150)
]

class PowerUp:
    """Power-up items for the player"""
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type  # 'speed', 'shield', 'boost'
        self.active = True
        self.rect = pygame.Rect(x, y, 20, 20)
    
def draw(self, screen):
        if self.type == 'speed':
            pygame.draw.rect(screen, (255, 255, 0), self.rect)
        elif self.type == 'shield':
            pygame.draw.circle(screen, (0, 255, 255), (self.x + 10, self.y + 10), 10)
        elif self.type == 'boost':
            pygame.draw.circle(screen, (255, 165, 0), (self.x + 10, self.y + 10), 10)
    
def collect(self):
        self.active = False
        return self.type

class Obstacle:
    """Obstacles on the track"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
    
def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.rect)

class AIOpponent:
    """Computer-controlled racer"""
    def __init__(self, name, start_x, start_y, color):
        self.name = name
        self.x = start_x
        self.y = start_y
        self.color = color
        self.speed = 2
        self.waypoint_index = 0
        self.laps = 0
        self.finished = False
        self.rect = pygame.Rect(start_x, start_y, CAR_WIDTH, CAR_HEIGHT)
        self.angle = 0
    
def move(self):
        """Move towards next waypoint"""
        if not self.finished:
            waypoint = TRACK_WAYPOINTS[self.waypoint_index]
            dx = waypoint[0] - self.x
            dy = waypoint[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < 30:
                self.waypoint_index = (self.waypoint_index + 1) % len(TRACK_WAYPOINTS)
                if self.waypoint_index == 0:
                    self.laps += 1
                    if self.laps >= 3:
                        self.finished = True
            
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                self.angle = math.atan2(dy, dx)
            
            self.rect.x = self.x
            self.rect.y = self.y
    
def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw direction indicator
        end_x = self.x + 15 * math.cos(self.angle)
        end_y = self.y + 15 * math.sin(self.angle)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (end_x, end_y), 2)

class Player:
    """Player-controlled kart"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.friction = 0.05
        self.angle = 0
        self.laps = 0
        self.position = 0
        self.shield_active = False
        self.shield_time = 0
        self.boost_active = False
        self.boost_time = 0
        self.speed_boost = 1.0
        self.rect = pygame.Rect(x, y, CAR_WIDTH, CAR_HEIGHT)
    
def move(self, keys):
        """Handle player input and movement"""
        # Acceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        # Braking
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration * 2, -2)
        else:
            # Friction
            if self.speed > 0:
                self.speed -= self.friction
            elif self.speed < 0:
                self.speed += self.friction
            if abs(self.speed) < 0.1:
                self.speed = 0
        
        # Steering
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= 0.1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += 0.1
        
        # Movement
        self.x += self.speed * self.speed_boost * math.cos(self.angle)
        self.y += self.speed * self.speed_boost * math.sin(self.angle)
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Update power-up timers
        if self.shield_active:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.shield_active = False
        
        if self.boost_active:
            self.boost_time -= 1
            if self.boost_time <= 0:
                self.boost_active = False
                self.speed_boost = 1.0
    
def apply_powerup(self, power_type):
        """Apply power-up effects"""
        if power_type == 'speed':
            self.max_speed = 7
        elif power_type == 'shield':
            self.shield_active = True
            self.shield_time = 300  # 5 seconds at 60 FPS
        elif power_type == 'boost':
            self.boost_active = True
            self.boost_time = 120  # 2 seconds at 60 FPS
            self.speed_boost = 1.5
    
def draw(self, screen):
        """Draw player kart"""
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        # Draw direction indicator
        end_x = self.x + 15 * math.cos(self.angle)
        end_y = self.y + 15 * math.sin(self.angle)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (end_x, end_y), 2)
        
        # Draw shield if active
        if self.shield_active:
            pygame.draw.circle(screen, (0, 255, 255), (int(self.x), int(self.y)), 35, 2)
        
        # Draw boost indicator
        if self.boost_active:
            pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), 40, 1)

class RaceTrack:
    """Track with boundaries and lap counter"""
    def __init__(self):
        self.lap_line = 100  # X position where lap is counted
        self.player_crossed = False
    
def draw_track(self, screen):
        """Draw the track"""
        # Background
        screen.fill(GRASS_COLOR)
        
        # Outer track boundary
        pygame.draw.ellipse(screen, ROAD_COLOR, (150, 100, 900, 600))
        # Inner track boundary
        pygame.draw.ellipse(screen, GRASS_COLOR, (350, 250, 500, 300))
        
        # Lap line
        pygame.draw.line(screen, (255, 255, 255), (600, 100), (600, 200), 3)
    
def check_lap(self, player):
        """Check if player completed a lap"""
        if player.y > 100 and player.y < 200:
            if not self.player_crossed:
                player.laps += 1
                self.player_crossed = True
                return True
        else:
            self.player_crossed = False
        return False

class MarioKartGame:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mario Kart Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game objects
        self.track = RaceTrack()
        self.player = Player(600, 150)
        self.ai_opponents = [
            AIOpponent('AI-Luigi', 550, 150, (0, 255, 0)),
            AIOpponent('AI-Yoshi', 650, 150, (255, 165, 0)),
        ]
        
        self.power_ups = [
            PowerUp(400, 400, 'speed'),
            PowerUp(800, 300, 'shield'),
            PowerUp(500, 500, 'boost'),
        ]
        
        self.obstacles = [
            Obstacle(300, 350),
            Obstacle(900, 450),
        ]
        
        self.race_finished = False
        self.finish_time = 0
    
def handle_collisions(self):
        """Handle collisions with obstacles and power-ups"""
        # Check power-up collisions
        for power_up in self.power_ups:
            if power_up.active and self.player.rect.colliderect(power_up.rect):
                power_type = power_up.collect()
                self.player.apply_powerup(power_type)
        
        # Check obstacle collisions
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                if not self.player.shield_active:
                    self.player.speed = 0
                    self.player.x -= 5
                    self.player.y -= 5
    
def draw_ui(self):
        """Draw UI elements"""
        # Player lap counter
        lap_text = self.font.render(f"Laps: {self.player.laps}/3", True, (255, 255, 255))
        self.screen.blit(lap_text, (20, 20))
        
        # Speed display
        speed_text = self.small_font.render(f"Speed: {self.player.speed:.1f}", True, (255, 255, 255))
        self.screen.blit(speed_text, (20, 60))
        
        # AI opponent positions
        y_offset = 20
        ai_label = self.small_font.render("Opponents:", True, (255, 255, 255))
        self.screen.blit(ai_label, (SCREEN_WIDTH - 200, y_offset))
        y_offset += 30
        
        for opponent in self.ai_opponents:
            opponent_text = self.small_font.render(f"{opponent.name}: {opponent.laps}/3", True, opponent.color)
            self.screen.blit(opponent_text, (SCREEN_WIDTH - 200, y_offset))
            y_offset += 25
        
        # Power-up status
        status_text = ""
        if self.player.shield_active:
            status_text += "Shield "
        if self.player.boost_active:
            status_text += "Boost "
        
        if status_text:
            status_display = self.small_font.render(status_text, True, (255, 255, 0))
            self.screen.blit(status_display, (20, 100))
        
        # Race finished message
        if self.race_finished:
            finished_text = self.font.render("RACE FINISHED!", True, (255, 215, 0))
            self.screen.blit(finished_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    
def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            keys = pygame.key.get_pressed()
            
            # Update game state
            if not self.race_finished:
                self.player.move(keys)
                self.track.check_lap(self.player)
                
                # Update AI opponents
                for opponent in self.ai_opponents:
                    opponent.move()
                
                # Check collisions
                self.handle_collisions()
                
                # Check if race is finished
                if self.player.laps >= 3:
                    self.race_finished = True
                    self.finish_time = pygame.time.get_ticks()
            
            # Draw everything
            self.track.draw_track(self.screen)
            
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            # Draw power-ups
            for power_up in self.power_ups:
                if power_up.active:
                    power_up.draw(self.screen)
            
            # Draw AI opponents
            for opponent in self.ai_opponents:
                opponent.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = MarioKartGame()
    game.run()