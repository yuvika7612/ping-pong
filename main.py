import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle game over menu input
            if engine.is_game_over():
                action = engine.handle_game_over_input(event)
                if action == "exit":
                    running = False
                elif action == "continue":
                    # Game will restart automatically via start_new_game()
                    pass
            
            # Handle ESC during gameplay to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not engine.is_game_over():
                    running = False

        # Only handle gameplay input if game is not over
        if not engine.is_game_over():
            engine.handle_input()
            engine.update()
        
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()