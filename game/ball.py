import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, sound_manager=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.max_speed = 15
        self.sound_manager = sound_manager

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top and bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            
            # Position correction for walls
            if self.y <= 0:
                self.y = 0
            else:
                self.y = self.screen_height - self.height
            
            # Play wall bounce sound
            if self.sound_manager:
                self.sound_manager.play_wall_bounce()

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        
        # Check LEFT paddle (player) collision
        if ball_rect.colliderect(player.rect()):
            # Only reverse if ball is moving towards the paddle (prevent double-hit)
            if self.velocity_x < 0:
                self.velocity_x = abs(self.velocity_x)  # Bounce right
                # Position correction: push ball out of paddle
                self.x = player.x + player.width
                # Optional: slight speed increase for difficulty
                self.velocity_x *= 1.05
                # Add angle variation based on where ball hits paddle
                self._add_spin(player)
                
                # Play paddle hit sound
                if self.sound_manager:
                    self.sound_manager.play_paddle_hit()
        
        # Check RIGHT paddle (AI) collision
        elif ball_rect.colliderect(ai.rect()):
            # Only reverse if ball is moving towards the paddle
            if self.velocity_x > 0:
                self.velocity_x = -abs(self.velocity_x)  # Bounce left
                # Position correction: push ball out of paddle
                self.x = ai.x - self.width
                # Optional: slight speed increase
                self.velocity_x *= 1.05
                # Add angle variation
                self._add_spin(ai)
                
                # Play paddle hit sound
                if self.sound_manager:
                    self.sound_manager.play_paddle_hit()
        
        # Cap velocity to prevent tunneling
        self._clamp_velocity()

    def _add_spin(self, paddle):
        """Add angle variation based on where ball hits paddle"""
        # Calculate where on paddle the ball hit (0 = top, 1 = bottom)
        relative_intersect = (self.y + self.height/2) - (paddle.y + paddle.height/2)
        normalized_intersect = relative_intersect / (paddle.height/2)
        
        # Adjust vertical velocity based on hit position (max ±5)
        self.velocity_y += normalized_intersect * 2

    def _clamp_velocity(self):
        """Prevent velocity from exceeding max_speed"""
        if abs(self.velocity_x) > self.max_speed:
            self.velocity_x = self.max_speed if self.velocity_x > 0 else -self.max_speed
        if abs(self.velocity_y) > self.max_speed:
            self.velocity_y = self.max_speed if self.velocity_y > 0 else -self.max_speed

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)