import pygame
import Ghost
import math


class PacMan:
    def __init__(self, x, y, display, maze, main):
        # Objects
        self.display = display
        self.maze = maze
        self.main = main

        # Constants
        self.size = 26
        self.step_len = main.block_size / 15
        self.step = self.step_len
        self.block_size = self.main.block_size
        self.offset = self.main.offset

        # Movement directions
        self.DIR = {"RIGHT": 0, "DOWN": 1, "LEFT": 2, "UP": 3}
        self.COORD_DIR = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
        self.look_dir = 3
        self.move_dir = 3

        # Location in pixels
        self.array_coord = [x, y]
        self.x = x * main.block_size + main.block_size / 2
        self.y = y * main.block_size + main.block_size / 2
        self.spawn_x = self.x
        self.spawn_y = self.y

        # Setup vars
        self.powered_up = False
        self.timer = 0
        self.power_time = 10

    def power_up(self, time):
        Ghost.turn_blue()
        self.powered_up = True
        self.power_time = time
        self.timer = 0

    def move(self):
        step = self.step_len
        self.array_coord = [int((self.x + self.block_size / 2) / self.block_size),
                            int((self.y + self.block_size / 2) / self.block_size)]

        if self.powered_up:
            # end power up at end of timer
            if self.timer >= self.power_time * self.main.fps:
                self.powered_up = False
                Ghost.end_blue()
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
            self.maze.center(self, "y", self.y)
            if self.move_dir == self.DIR["LEFT"]:
                self.x -= step
            if self.move_dir == self.DIR["RIGHT"]:
                self.x += step
            # Screen wrap
            if self.x < -self.size:
                self.x = self.main.display_width
            if self.x > self.size + self.main.display_width:
                self.x = -self.size

    def draw(self, mode):
        def draw_wedge_pacman(wedge_angle):
            radius = self.size / 2
            n_points = 60
            point_separation = math.radians((360 - wedge_angle) / n_points)
            current_angle = math.radians(90 * self.move_dir + wedge_angle / 2)
            pointlist = [(self.x, self.y + self.offset) for i in range(n_points)]

            for i in range(1, n_points):
                pointlist[i] = (self.x + math.cos(current_angle) * radius,
                                self.y + math.sin(current_angle) * radius + self.offset)
                current_angle += point_separation

            pygame.draw.polygon(self.display, (255, 255, 0), pointlist)

        def draw_while_running():
            if (not self.block_size/2 < self.x < self.main.display_width - self.block_size/2 - self.size) \
                    or self.maze.can_move(self, self.move_dir):
                if self.main.tick_counter % 18 < 9:
                    draw_wedge_pacman((self.main.tick_counter % 9) * 15)
                else:
                    draw_wedge_pacman(120 - (self.main.tick_counter % 9) * 15)
            else:
                draw_wedge_pacman(75)

        if mode == "run":
            draw_while_running()

        elif mode == "respawn":
            if self.main.temp_counter < 36:
                draw_wedge_pacman(0 + 10 * self.main.temp_counter)
                self.main.temp_counter += 1
            else:
                self.main.game_state = "run"
                self.x = self.spawn_x
                self.y = self.spawn_y
                draw_while_running()
