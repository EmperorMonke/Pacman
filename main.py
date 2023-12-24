import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PACMAN_RADIUS = 20
GHOST_RADIUS = 15
NORMAL_SPEED = 3
INVINCIBLE_SPEED = 6
NUM_GHOSTS = 3
NUM_LIVES = 3
PELLET_RADIUS = 5
LARGE_PELLET_RADIUS = 10
LARGE_PELLET_DURATION = 500  # in milliseconds
NUM_LARGE_PELLETS = 5

# Initialize game variables
score = 0
lives = NUM_LIVES
level = 1

# Initialize Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game")

# Load images with adjusted dimensions
pacman_img = pygame.transform.scale(pygame.image.load("pacman.jpg"), (2 * PACMAN_RADIUS, 2 * PACMAN_RADIUS))
ghost_img = pygame.transform.scale(pygame.image.load("ghost.jpg"), (2 * GHOST_RADIUS, 2 * GHOST_RADIUS))

# Define Obstacle class
class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(window, BLUE, self.rect)

obstacles = [
    Obstacle(50, 50, 100, 400),
    Obstacle(150, 250, 300, 100),
    Obstacle(450, 50, 100, 400),
    Obstacle(150, 50, 300, 50),
    Obstacle(150, 500, 300, 50)
] 

# Define Pacman class
class Pacman:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = "RIGHT"
        self.speed = NORMAL_SPEED
        self.large_pellet_timer = 0
        self.rect = pygame.Rect(0, 0, 2 * PACMAN_RADIUS, 2 * PACMAN_RADIUS)
        self.spawn()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y - self.speed > 0 and not self.check_collision((0, -self.speed)):
            self.y -= self.speed
            self.direction = "UP"
        elif keys[pygame.K_DOWN] and self.y + self.speed < HEIGHT and not self.check_collision((0, self.speed)):
            self.y += self.speed
            self.direction = "DOWN"
        elif keys[pygame.K_LEFT] and self.x - self.speed > 0 and not self.check_collision((-self.speed, 0)):
            self.x -= self.speed
            self.direction = "LEFT"
        elif keys[pygame.K_RIGHT] and self.x + self.speed < WIDTH and not self.check_collision((self.speed, 0)):
            self.x += self.speed
            self.direction = "RIGHT"

    def draw(self):
        angle = 0
        if self.direction == "UP":
            angle = 90
        elif self.direction == "DOWN":
            angle = 270
        elif self.direction == "LEFT":
            angle = 180
        rotated_pacman = pygame.transform.rotate(pacman_img, angle)
        window.blit(rotated_pacman, (self.x - PACMAN_RADIUS, self.y - PACMAN_RADIUS))

    def check_collision(self, delta):
        rect = pygame.Rect(self.x + delta[0] - PACMAN_RADIUS, self.y + delta[1] - PACMAN_RADIUS, 2 * PACMAN_RADIUS, 2 * PACMAN_RADIUS)
        for obstacle in obstacles:
            if obstacle.rect.colliderect(rect):
                return True
        return False

    def spawn(self):
        while True:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.rect.topleft = (self.x - PACMAN_RADIUS, self.y - PACMAN_RADIUS)
            if not any(obstacle.rect.colliderect(self.rect) for obstacle in obstacles):
                break

# Define Ghost class
class Ghost:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = NORMAL_SPEED
        self.large_pellet_timer = 0
        self.rect = pygame.Rect(0, 0, 2 * GHOST_RADIUS, 2 * GHOST_RADIUS)
        self.move()  # Move Ghost to a valid position

    def move(self):
        while True:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.rect.topleft = (self.x - GHOST_RADIUS, self.y - GHOST_RADIUS)
            if not any(obstacle.rect.colliderect(self.rect) for obstacle in obstacles):
                break

    def draw(self):
        window.blit(ghost_img, (self.x - GHOST_RADIUS, self.y - GHOST_RADIUS))

# Define Pellet class
class Pellet:
    def __init__(self, x, y, is_large=False):
        self.x = x
        self.y = y
        self.radius = LARGE_PELLET_RADIUS if is_large else PELLET_RADIUS
        self.is_large = is_large

    def draw(self):
        color = YELLOW if self.is_large else YELLOW
        pygame.draw.circle(window, color, (self.x, self.y), self.radius)

# Create Pacman, Ghosts, Obstacles, and Pellets
pacman = Pacman()
ghosts = [Ghost() for _ in range(NUM_GHOSTS)]

# Create pellets with large pellets
pellets = [Pellet(70, 70), Pellet(130, 130), Pellet(300, 300, is_large=True), Pellet(470, 470), Pellet(530, 530)]
pellets += [
    Pellet(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    for _ in range(50 - NUM_LARGE_PELLETS)
]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(BLACK)

    # Handle Pacman movement
    pacman.move()

    # Draw Pellets
    for pellet in pellets:
        pellet.draw()

    # Check for collisions with pellets
    for pellet in pellets:
        if pygame.Rect(pellet.x - pellet.radius, pellet.y - pellet.radius, 2 * pellet.radius, 2 * pellet.radius).colliderect(
            pygame.Rect(pacman.x - PACMAN_RADIUS, pacman.y - PACMAN_RADIUS, 2 * PACMAN_RADIUS, 2 * PACMAN_RADIUS)
        ):
            score += 1
            pellets.remove(pellet)

            # Check if the pellet is a large pellet
            if pellet.is_large:
                pacman.large_pellet_timer = LARGE_PELLET_DURATION
                pacman.speed = INVINCIBLE_SPEED

    # Update Ghosts based on large pellet timer
    for ghost in ghosts:
        ghost.move()

    # Check for collisions with ghosts
    for ghost in ghosts:
        if not ghost.large_pellet_timer and pygame.Rect(ghost.x - GHOST_RADIUS, ghost.y - GHOST_RADIUS, 2 * GHOST_RADIUS, 2 * GHOST_RADIUS).colliderect(
            pygame.Rect(pacman.x - PACMAN_RADIUS, pacman.y - PACMAN_RADIUS, 2 * PACMAN_RADIUS, 2 * PACMAN_RADIUS)
        ):
            if pacman.large_pellet_timer > 0:
                # Pacman can eat the ghost during the large pellet time
                ghosts.remove(ghost)
            else:
                # Collision with ghost, Pacman loses a life
                lives -= 1
                if lives == 0:
                    print("Game Over!")
                    running = False
                    break
                else:
                    # Reset Pacman position
                    pacman.spawn()
                    pacman.speed = NORMAL_SPEED

    # Draw Obstacles
    for obstacle in obstacles:
        obstacle.draw()

    # Draw Ghosts
    for ghost in ghosts:
        ghost.draw()

    # Draw Pacman
    pacman.draw()

    # Check for winning condition
    if not pellets:
        level += 1
        print(f"Congratulations! You've completed Level {level}")
        # Reset variables for the next level
        score = 0
        pacman.large_pellet_timer = 0
        pacman.speed = NORMAL_SPEED
        pacman.spawn()
        pellets = [Pellet(70, 70), Pellet(130, 130), Pellet(300, 300, is_large=True), Pellet(470, 470), Pellet(530, 530)]
        pellets += [
            Pellet(random.randint(0, WIDTH), random.randint(0, HEIGHT))
            for _ in range(50 - NUM_LARGE_PELLETS)
        ]

    # Display score, lives, and level
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    level_text = font.render(f"Level: {level}", True, YELLOW)
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, 50))
    window.blit(level_text, (10, 90))

    # Display large pellet timer
    if pacman.large_pellet_timer > 0:
        timer_text = font.render(f"Invincible: {pacman.large_pellet_timer / 1000} s", True, YELLOW)
        window.blit(timer_text, (10, 130))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()