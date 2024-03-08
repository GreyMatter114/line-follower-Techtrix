import pygame
import os, sys
import neat
import math
import pickle

start = (0, 10)
finish = (600, 590)
pygame.font.init()  # Initialize font
clock = pygame.time.Clock()
# Window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 600
surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

# Pygame window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Maze Solver")

# Load images
bg_img = pygame.transform.scale(
    pygame.image.load("maze.png").convert_alpha(), (600, 600)
)

gen = 0

image = pygame.transform.scale(pygame.image.load("car.png"), (20, 20))
image_rect = image.get_rect()
# Load an image onto a separate surface  # Path to your image file

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

    def distance_to_start(self):
        return math.sqrt((self.x - start[0]) ** 2 + (self.y - start[1]) ** 2)

    def distance_to_finish(self):
        return math.sqrt((self.x - finish[0]) ** 2 + (self.y - finish[1]) ** 2)

    def check_color_at_side(self, angle_offset):
        """
        Check the color at the side of the rectangular object
        Returns 1 for black, 0 for white, and -1 for out of bounds
        """
        side_x = self.x + int(20 * math.cos(math.radians(self.angle + angle_offset)))
        side_y = self.y + int(20 * math.sin(math.radians(self.angle + angle_offset)))
        try:
            color = surface.get_at((int(side_x), int(side_y)))
            if color == (0, 0, 0):  # Check if color is black
                return 0
            else:
                return 1
        except:  # Handle out of bounds
            return -1


def draw_window(win, vehicle, score, gen):
    """
    Draw the game window
    """
    win.blit(bg_img, (0, 0))
    vehicle.draw(win)
    score_label = STAT_FONT.render("Score: " + str(int(score)), 1, (0, 255, 0))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    score_label = STAT_FONT.render("Gens: " + str(gen - 1), 1, (0, 255, 0))
    win.blit(score_label, (10, 10))
    vehicle.draw(win)
    pygame.display.update()


def eval_genomes(genomes, config):
    """
    Evaluate genomes in the current population
    """
    global WIN, gen
    win = WIN
    gen += 1
    vehicles = []
    nets = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # Initialize fitness to 0
        vehicle = RectObject(0, 15)  # Initialize rectangular object
        vehicle.rotate(90)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        vehicles.append(vehicle)
        ge.append(genome)
        start_distance = vehicle.distance_to_start()  # Distance from start position
        finish_distance = vehicle.distance_to_finish()  # Distance from finish position

        # Game loop
        run = True
        while run and len(vehicles) > 0:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            # Input data for neural network

            # Feed input to the neural network

            # Interpret output to decide movement

            # Move the rectangular object
            for x, vehicle in enumerate(
                vehicles
            ):  # give each vehicle a fitness of 0.1 for each frame it stays alive
                ge[x].fitness += 0.1
                vehicle.move(10)
                left_data = vehicle.check_color_at_side(-90)
                right_data = vehicle.check_color_at_side(90)
                vehicle.get_position()
                if left_data == -1 and right_data == -1:
                    genome.fitness = 0
                # send vehicle location, top pipe location and bottom pipe location and determine from network whether to move or not in which direction
                output = nets[vehicles.index(vehicle)].activate((left_data, right_data))

                if output[0] > 0.5 and output[1] < -0.5:
                    vehicle.rotate(90)
                    vehicle.move(10)
                elif output[1] > 0.5 and output[0] < -0.5:
                    vehicle.rotate(-90)
                    vehicle.move(10)
                elif output[1] > 0.5 and output[0] > 0.5:
                    vehicle.move(10)
                elif output[1] < -0.5 and output[0] < -0.5:
                    vehicle.rotate(180)
                    vehicle.move(10)

                # Update fitness based on distance traveled
                new_start_distance = vehicle.distance_to_start()
                new_finish_distance = vehicle.distance_to_finish()

                # Penalize fitness if the robot moves away from the line

                # Penalize fitness if the robot is near the edges of the screen

                # Increase fitness if distance from start decreases and from finish increases
                if (new_start_distance - start_distance) < -100:
                    genome.fitness -= 1
                elif (new_start_distance - start_distance) > 100:
                    genome.fitness += 1
                if (new_finish_distance - finish_distance) < -100:
                    genome.fitness += 1
                elif (new_finish_distance - finish_distance) > 100:
                    genome.fitness -= 1

                # Draw window
                draw_window(win, vehicle, vehicle.distance_to_start() // 10, gen)
                if vehicle.distance_to_start() // 10 > 84:
                    pickle.dump(nets[0], open("line_follower_model.pickle", "wb+"))
                    pygame.quit()
                    sys.exit()
                if genome.fitness <= 0:
                    ind = vehicles.index(vehicle)
                    vehicles.pop(ind)
                    ge.pop(ind)
                    nets.pop(ind)
                start_distance = new_start_distance
                finish_distance = new_finish_distance


# Main function to run NEAT
def run(config_file):
    """
    Run NEAT algorithm to train a neural network to solve the maze
    """
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Create the population
    p = neat.Population(config)

    # Add reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for a specified number of generations
    winner = p.run(eval_genomes, 50)

    # Show final stats
    print("\nBest genome:\n{!s}".format(winner))


if __name__ == "__main__":
    # Determine path to configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    run(config_path)
