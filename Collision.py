import pygame
import random
import math
import numpy as np

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25



class Ball:
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self, x, y, change_x, change_y, color):
        self.x = x
        self.y = y
        self.change_x = change_x
        self.change_y = change_y
        self.collider = pygame.Rect(x - BALL_SIZE, y - BALL_SIZE, BALL_SIZE * 2, BALL_SIZE * 2)
        self.color = color

    def update_collider(self):
        # Update the collider position
        self.collider.centerx = int(self.x)
        self.collider.centery = int(self.y)
        self.collider.left = max(self.collider.left, 0)
        self.collider.right = min(self.collider.right, SCREEN_WIDTH)
        self.collider.top = max(self.collider.top, 0)
        self.collider.bottom = min(self.collider.bottom, SCREEN_HEIGHT)


def make_ball():
    """
    Function to make a new, random ball.
    """
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ball = Ball(random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE),
                random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE),
                random.randrange(-2, 3),
                random.randrange(-2, 3),
                color)

    return ball


def check_collision(ball1, ball2):
    # Calculate the distance between the two balls
    dist = math.sqrt((ball2.x - ball1.x) ** 2 + (ball2.y - ball1.y) ** 2)
    # Calculate the sum of the radii of the two balls
    sum_radii = BALL_SIZE * 2
    # If the distance is less than the sum of the radii, then the balls are colliding
    if dist < sum_radii:
        # Calculate the angle between the two balls
        angle = math.atan2(ball2.y - ball1.y, ball2.x - ball1.x)
        # Calculate the new velocities of the balls
        v1, v2 = calculate_new_velocities(ball1, ball2, angle)
        # Update the velocities of the balls
        ball1.change_x, ball1.change_y = v1
        ball2.change_x, ball2.change_y = v2
        return True
    return False


def calculate_new_velocities(ball1, ball2, angle):
    # Calculate the initial velocities of the balls
    v1_i = math.sqrt(ball1.change_x ** 2 + ball1.change_y ** 2) / 2
    v2_i = math.sqrt(ball2.change_x ** 2 + ball2.change_y ** 2) / 2
    m1 = (4/3) * math.pi * (BALL_SIZE ** 3) # Mass of ball 1
    m2 = (4/3) * math.pi * (BALL_SIZE ** 3) # Mass of ball 2
    # Calculate the direction of motion of the balls
    u1 = np.array([ball1.change_x, ball1.change_y])
    u2 = np.array([ball2.change_x, ball2.change_y])
    e = np.array([math.cos(angle), math.sin(angle)])
    # Calculate the new velocities of the balls using the elastic collision equations
    v1_f = ((m1 - m2) * v1_i + 2 * m2 * v2_i * np.dot(u2 - u1, e)) / (m1 + m2)
    v2_f = ((m2 - m1) * v2_i + 2 * m1 * v1_i * np.dot(u1 - u2, e)) / (m1 + m2)
    # Calculate the final velocities of the balls
    v1_f = v1_f * e + u1
    v2_f = v2_f * e + u2
    # Reduce the velocities slightly to prevent the balls from bouncing too far away from each other
    v1_f *= 0.95
    v2_f *= 0.95
    return v1_f.tolist(), v2_f.tolist()

def main():

    pygame.init()

    # Set the height and width of the screen
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Ender EROL Midterm Exam")

    # Create a list to hold the balls
    ball_list = []

    # Create the first ball
    ball = make_ball()
    ball_list.append(ball)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    score = 0

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a new ball and add it to the list
                    ball = make_ball()
                    ball_list.append(ball)

        # --- Game logic should go here
        # Move the balls
        for ball in ball_list:
            ball.x += ball.change_x
            ball.y += ball.change_y
            ball.update_collider()

            # Check for collisions with other balls
            for other_ball in ball_list:
                if ball != other_ball:
                    if check_collision(ball, other_ball):
                        score += 1


            # Check for collisions with the walls
            if ball.x < BALL_SIZE or ball.x > SCREEN_WIDTH - BALL_SIZE:
                ball.change_x *= -1
            if ball.y < BALL_SIZE or ball.y > SCREEN_HEIGHT - BALL_SIZE:
                ball.change_y *= -1

        # --- Drawing code should go here
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)

        # Draw the balls
        for ball in ball_list:
            pygame.draw.circle(screen, ball.color, (ball.x, ball.y), BALL_SIZE)

        # --- Go ahead and update the screen
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == "__main__":
    main()