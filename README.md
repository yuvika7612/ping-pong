Real-Time Ping Pong Game

This project is a terminal-based ping pong game developed using Python and Pygame.
It introduces students to interactive game design, focusing on object-oriented programming and real-time graphical rendering.# Project: Real-Time Ping Pong Game

This project is a terminal-based ping pong game using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

Project Overview

You are provided with a partially working game that includes:

Player and AI-controlled paddles

Ball movement with basic collision mechanics

Score tracking and display

Your task is to analyze, collaborate with an AI assistant (ChatGPT), and complete/fix the game to make it fully functional.

Use ChatGPT as your LLM partner for “vibecoding” throughout this lab.
 Getting Started
1. Setup

Clone this repository or download the project folder.

Ensure Python 3.10+ is installed.

Install dependencies:

pip install -r requirements.txt


Run the game:

python main.py

Initial Prompt Template (for LLM)

Use the following prompt to start your interaction with ChatGPT:

I’m working on a real-time Ping Pong game using Python and Pygame. I have a partially working project structure. Please help me understand how the logic is organized and guide me on implementing missing features. Review any code I send to ensure it aligns with the expected behavior.

Quick Prompts for Common Tasks

The prompts below will help you quickly work on each task.
Copy and paste them into ChatGPT for step-by-step assistance.

Note: While the responses will generate working code, always review and test the logic for edge cases.
This is designed to help you practice critical code review and debugging skills.

Tasks to Complete

Each task should be developed through an iterative process — test, refine, and validate.

Task 1: Refine Ball Collision

The ball occasionally passes through paddles at high speed. Improve collision accuracy.

Prompt:

Help me fix ball collision in my ping pong game. The ball passes through paddles sometimes. I need to check if the ball's rectangle overlaps with paddle rectangles and reverse velocity_x when it happens. Just add the collision check right after moving the ball, that should work perfectly for high speeds.

Task 2: Implement Game Over Condition

Add a “Game Over” screen when a player reaches the winning score (e.g., 5).
Display the winner and end the game gracefully.

Prompt:

I need a game over screen when a player reaches 5 points. Create a method that checks if either score equals 5, then display "Player Wins!" or "AI Wins!" on screen. Make sure to keep the game loop running so players can see the message. Add a small delay before closing pygame.

Task 3: Add Replay Option

Allow players to choose to replay after the game ends (Best of 3, 5, or 7).

Prompt:

Add a replay feature after game over. Show options for "Best of 3", "Best of 5", "Best of 7", or "Exit". Wait for user input (keys 3, 5, 7, or ESC). When they choose, update the winning score target and reset the ball position. That should let them play again.

Task 4: Add Sound Feedback

Include sound effects for paddle hits, wall bounces, and scoring.

Prompt:

Add sound effects to my pygame ping pong game. Load .wav files for paddle hit, wall bounce, and scoring using pygame.mixer.Sound(). Play the sounds whenever ball.velocity_x or ball.velocity_y changes. Initialize pygame.mixer at the start of the file.

Expected Final Behavior

Smooth paddle movement using W and S keys

AI responds dynamically to the ball’s movement

Realistic ball rebounds on walls and paddles

Scores update correctly on each miss

Displays “Game Over” with replay options

Optional sound feedback for all major events
