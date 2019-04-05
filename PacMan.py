import pygame
import Ghost


class PacMan:
    def __init__(self, x, y, display, maze, main):
        # Objects
        self.display = display
        self.maze = maze
        self.main = main

        # Constants
        self.size = 26
        self.step_len = main.block_size / 15
        self.block_size = self.main.block_size
        self.offset = self.main.offset

        # Movement directions
        self.DIR = {"RIGHT": 0, "DOWN": 1, "LEFT": 2, "UP": 3}
        self.COORD_DIR = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
        self.look_dir = None
        self.move_dir = None

        # Location in pixels
        self.array_coord = [x, y]
        self.x = x * main.block_size + main.block_size / 2
        self.y = y * main.block_size + main.block_size / 2

        # Setup vars
        self.powered_up = False
        self.previously_powered = False
        self.timer = 0
        self.power_time = 10

    def power_up(self, time):
        Ghost.turn_blue()
        self.previously_powered = False
        self.powered_up = True
        self.power_time = time
        self.timer = 0

    def move(self):
        step = self.step_len
        self.array_coord = [int((self.x + self.block_size / 2) / self.block_size),
                            int((self.y + self.block_size / 2) / self.block_size)]

        if self.powered_up:
            # end powerup at end of timer
            if self.timer >= self.power_time * self.main.fps:
                self.powered_up = False
                Ghost.end_blue()
            elif self.timer >= 1:
                self.previously_powered = True
            else:
                self.timer += 1

        # Can only change direction within the bounds of the maze
        if self.block_size < self.x < self.main.display_width - self.block_size:
            # Change movement direction to match look direction if possible
            if self.look_dir != self.move_dir:
                if self.maze.can_move(self, self.look_dir):
                    self.move_dir = self.look_dir

            # Do movement
            if self.maze.can_move(self, self.move_dir):
                self.x += step * self.COORD_DIR[self.move_dir][0]
                self.y += step * self.COORD_DIR[self.move_dir][1]

        # If outside maze, keep moving forwards until wrapped to the other side of the screen
        else:
            if self.move_dir == self.DIR["LEFT"]:
                self.x -= step
                self.maze.center(self, "y", self.y)
            if self.move_dir == self.DIR["RIGHT"]:
                self.x += step
                self.maze.center(self, "y", self.y)
            # Screen wrap
            if self.x < -self.size:
                self.x = self.main.display_width
            if self.x > self.size + self.main.display_width:
                self.x = -self.size

    def draw(self):
        pygame.draw.ellipse(self.display, (255, 255, 0),
                            (self.x - self.size / 2, self.y - self.size / 2 + self.offset, self.size, self.size))
