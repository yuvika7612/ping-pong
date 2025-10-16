import pygame
from .paddle import Paddle
from .ball import Ball
from .sound_manager import SoundManager

# Game Engine

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize sound manager
        self.sound_manager = SoundManager()

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, self.sound_manager)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5
        self.game_over = False
        self.winner = None
        self.selected_option = None  # Track which option is highlighted
        
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.medium_font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 25)

    def handle_input(self):
        # Don't allow gameplay input during game over
        if self.game_over:
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def handle_game_over_input(self, event):
        """Handle input during game over screen"""
        if not self.game_over:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self.start_new_game(3)
                return "continue"
            elif event.key == pygame.K_5:
                self.start_new_game(5)
                return "continue"
            elif event.key == pygame.K_7:
                self.start_new_game(7)
                return "continue"
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        
        return None

    def start_new_game(self, winning_score):
        """Start a new game with specified winning score"""
        self.winning_score = winning_score
        self.reset_game()

    def update(self):
        # Don't update game state if game is over
        if self.game_over:
            return
            
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.check_game_over()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.check_game_over()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self):
        """Check if either player has reached the winning score"""
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Draw game over screen if game is over
        if self.game_over:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        """Render the game over overlay with replay options"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Winner text
        winner_text = self.large_font.render(f"{self.winner} Wins!", True, YELLOW)
        winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2 - 150))
        screen.blit(winner_text, winner_rect)

        # Final score
        score_text = self.medium_font.render(
            f"Final Score: {self.player_score} - {self.ai_score}", 
            True, WHITE
        )
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2 - 80))
        screen.blit(score_text, score_rect)

        # Replay options title
        replay_title = self.medium_font.render("Play Again?", True, WHITE)
        replay_rect = replay_title.get_rect(center=(self.width//2, self.height//2 - 10))
        screen.blit(replay_title, replay_rect)

        # Draw replay options
        options = [
            ("Press 3 for Best of 3", pygame.K_3, 60),
            ("Press 5 for Best of 5", pygame.K_5, 100),
            ("Press 7 for Best of 7", pygame.K_7, 140),
        ]

        for text, key, y_offset in options:
            # Highlight if this is the default/recommended option
            color = GREEN if key == pygame.K_5 else WHITE
            option_text = self.font.render(text, True, color)
            option_rect = option_text.get_rect(center=(self.width//2, self.height//2 + y_offset))
            screen.blit(option_text, option_rect)

        # Exit instruction
        exit_text = self.small_font.render("Press ESC to Exit", True, GRAY)
        exit_rect = exit_text.get_rect(center=(self.width//2, self.height//2 + 200))
        screen.blit(exit_text, exit_rect)

        # Add visual separator
        pygame.draw.line(screen, GRAY, 
                        (self.width//2 - 150, self.height//2 + 30),
                        (self.width//2 + 150, self.height//2 + 30), 2)

    def is_game_over(self):
        """Public method to check if game is over"""
        return self.game_over

    def reset_game(self):
        """Reset the game to initial state"""
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.selected_option = None
        
        # Reset ball to center
        self.ball.reset()
        
        # Reset paddle positions
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50

    def get_winning_score(self):
        """Get current winning score target"""
        return self.winning_score