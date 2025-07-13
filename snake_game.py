import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
        
        # Check self collision
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def change_direction(self, new_direction):
        # Prevent moving in opposite direction
        if (self.direction[0] * -1, self.direction[1] * -1) != new_direction:
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self, screen):
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            # Draw head differently
            if i == 0:
                pygame.draw.rect(screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, WHITE, (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4), 2)
            else:
                pygame.draw.rect(screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, WHITE, (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2), 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def respawn(self, snake_body):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
    
    def draw(self, screen):
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        pygame.draw.rect(screen, RED, (x, y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, WHITE, (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.reset_game()
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        return True
    
    def update(self):
        if not self.game_over and not self.paused:
            if not self.snake.move():
                self.game_over = True
                return
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow_snake()
                self.score += 10
                self.food.respawn(self.snake.body)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        if not self.game_over:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # Draw pause screen
        if self.paused and not self.game_over:
            pause_text = self.big_font.render("PAUSED", True, BLUE)
            continue_text = self.font.render("Press SPACE to continue", True, WHITE)
            
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(pause_text, pause_rect)
            self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for smooth gameplay
        
        pygame.quit()
        sys.exit()

# Instructions
def show_instructions():
    print("Snake Game Instructions:")
    print("- Use arrow keys to control the snake")
    print("- Eat red food to grow and increase score")
    print("- Avoid hitting walls or yourself")
    print("- Press SPACE to pause/unpause")
    print("- Press ESC to quit")
    print("- When game over, press SPACE to restart")
    print("\nStarting game...")

if __name__ == "__main__":
    show_instructions()
    game = Game()
    game.run()