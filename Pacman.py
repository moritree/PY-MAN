import pygame
import Ghost


class Pacman:
    def __init__(self, x, y, block_size, display, maze, main):
        self.block_size = block_size
        self.offset = block_size*2
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2

        self.size = 22
        self.step_len = block_size / 15
        self.powered_step = block_size / 13

        self.display = display
        self.maze = maze
        self.main = main

        self.look_dir = None
        self.move_dir = None

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

        if self.powered_up:
            step = self.powered_step
            if self.timer >= self.power_time * self.main.fps:
                self.powered_up = False
                Ghost.end_blue()
            elif self.timer >= 1:
                self.previously_powered = True
            else:
                self.timer += 1

        # change movement direction if possible
        if self.block_size < self.x < self.main.display_width - self.block_size:
            if self.look_dir != self.move_dir:
                if self.look_dir == "UP" and self.maze.can_move(self, "UP"):
                    self.move_dir = "UP"
                if self.look_dir == "DOWN" and self.maze.can_move(self, "DOWN"):
                    self.move_dir = "DOWN"
                if self.look_dir == "LEFT" and self.maze.can_move(self, "LEFT"):
                    self.move_dir = "LEFT"
                if self.look_dir == "RIGHT" and self.maze.can_move(self, "RIGHT"):
                    self.move_dir = "RIGHT"

            # move
            if self.move_dir == "UP" and self.maze.can_move(self, "UP"):
                self.y -= step
                self.maze.center(self, "x", self.x)
            if self.move_dir == "DOWN" and self.maze.can_move(self, "DOWN"):
                self.y += step
                self.maze.center(self, "x", self.x)
            if self.move_dir == "LEFT" and self.maze.can_move(self, "LEFT"):
                self.x -= step
                self.maze.center(self, "y", self.y)
            if self.move_dir == "RIGHT" and self.maze.can_move(self, "RIGHT"):
                self.x += step
                self.maze.center(self, "y", self.y)
        else:
            if self.move_dir == "LEFT":
                self.x -= step
                self.maze.center(self, "y", self.y)
            if self.move_dir == "RIGHT":
                self.x += step
                self.maze.center(self, "y", self.y)

            # screen wrap
            if self.x < -self.size:
                self.x = self.main.display_width
            if self.x > self.size + self.main.display_width:
                self.x = -self.size

    def draw(self):
        pygame.draw.ellipse(self.display, (255, 255, 0),
                            (self.x - self.size / 2, self.y - self.size / 2 + self.offset, self.size, self.size))
