import pygame

# import os, sys
import math

# import pickle
from utility.vision import compute

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
maze_path = "./utility/assets/maze.png"
# Load images
bg_img = pygame.transform.scale(
    pygame.image.load(maze_path).convert_alpha(), (600, 600)
)

image = pygame.transform.scale(pygame.image.load("./utility/assets/car.png"), (20, 20))

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
        self.image = image
        self.rect = self.image.get_rect()
        self.center = self.rect.center
        self.x = x
        self.y = y
        self.rect_center = (x, y)
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, distance):
        dx = distance * math.cos(math.radians(self.angle))
        dy = distance * math.sin(math.radians(self.angle))
        self.x += dx
        self.y += dy

    def draw(self, win):
        """
        Draw the rectangular object on the window
        """
        win.blit(self.image, self.rect_center)

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


def solve_maze(start, finish, surface):
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
        neighbored = compute(x, y)  # Adjust based on grid size
        for neighbors in neighbored:
            for neighbor in neighbors:
                print(neighbor)
                nx, ny = neighbor
                if (
                    0 <= nx < WIN_WIDTH
                    and 0 <= ny < WIN_HEIGHT
                    and surface.get_at((nx, ny)) != (255, 255, 255)
                ):  # Check if the neighbor is within bounds and not a white wall
                    stack.append(neighbor)
    return False


def main():
    """
    Main function to run the maze solver
    """
    vehicle = RectObject(0, 109)  # Initialize rectangular object
    vehicle.rotate(90)
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
        solved = solve_maze(start, finish, surface)
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
