import pygame

# import os, sys
import math

# import pickle
import vision

start = (0, 10)
finish = (600, 590)
pygame.font.init()  # Initialize font
clock = pygame.time.Clock()
# Window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 600
surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Pygame window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Maze Solver")
maze_path = "maze.png"
# Load images
bg_img = pygame.transform.scale(
    pygame.image.load(maze_path).convert_alpha(), (600, 600)
)

# Blit the image onto the main surface
surface.blit(bg_img, (0, 0))


class RectObject:
    """
    Rectangular object representing the moving entity in the maze
    """

    def __init__(self, x, y):
        self.width = 10
        self.height = 10
        self.angle = 0
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, win):
        """
        Draw the rectangular object on the window
        """
        pygame.draw.rect(surface, (255, 0, 0), (50, 20, 100, 60))

    def get_position(self):
        """
        Return the position of the rectangular object
        """
        return self.x, self.y


def draw_window(win, vehicle, score):
    """
    Draw the game window
    """
    win.blit(bg_img, (0, 0))
    vehicle.draw(win)
    score_label = STAT_FONT.render("Score: " + str(int(score)), 1, (0, 255, 0))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    pygame.display.update()


def solve_maze(start, finish, vehicle):
    """
    Solve the maze using a depth-first search algorithm
    """
    stack = [start]
    visited = set()
    while stack:
        current = stack.pop()
        if current == finish:
            return True
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        motion = vision.main(x, y)  # Adjust based on grid size
        vehicle.move(5 * motion[0], 5 * motion[1])
    return False


def main():
    """
    Main function to run the maze solver
    """
    vehicle = RectObject(0, 109)  # Initialize rectangular object
    start_distance = vehicle.get_position()[0]  # Distance from start position
    score = 0
    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Solve maze
        solved = solve_maze(start, finish, vehicle)
        if solved:
            print("Maze solved!")
            break

        # Move the rectangular object
        vehicle.move(10)

        # Update score based on distance traveled
        score = vehicle.get_position()[0] - start_distance

        # Draw window
        draw_window(WIN, vehicle, score)


if __name__ == "__main__":
    main()
