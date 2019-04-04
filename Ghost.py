import pygame
import random
import math


def draw_ghosts():
    for ghost in Ghost.instances:
        ghost.draw()


def check_collisions():
    for ghost in Ghost.instances:
        ghost.collide()


def move_all():
    for ghost in Ghost.instances:
        ghost.move()


def turn_blue():
    for ghost in Ghost.instances:
        if ghost.here:
            ghost.blue = True
            ghost.timer = 0


def end_blue():
    for ghost in Ghost.instances:
        ghost.blue = False


def right_turn(facing):
    return abs((facing + 1) % 4)


def left_turn(facing):
    return abs((facing - 1) % 4)


class Ghost:
    instances = []

    def __init__(self, maze, display, player, main, x, y, color, scatter_coord, personality):
        # Objects
        self.display = display
        self.player = player
        self.main = main
        self.maze = maze

        # Constants
        self.block_size = main.block_size
        self.offset = main.offset
        self.size = 24
        self.base_color = color
        self.step_len = self.block_size / 17  # normal movement speed
        self.slow_step = self.block_size / 20  # movement speed when turned blue
        self.personality = personality
        self.scatter_time = 7
        self.chase_time = 20
        self.mode = "house"

        # Movement
        self.scatter_coord = scatter_coord
        self.DIR = {"RIGHT": 0, "DOWN": 1, "LEFT": 2, "UP": 3}
        self.COORD_DIR = {0: [1, 0], 1: [0, 1], 2: [-1, 0], 3: [0, -1]}
        self.look_dir = 3
        self.move_dir = 3

        # Location
        self.array_coord = [x, y]
        self.x = x * self.block_size + self.block_size / 2  # px
        self.y = y * self.block_size + self.block_size / 2  # px

        # Setup vars
        self.here = True
        self.blue = False
        self.timer = 0
        self.respawn_time = 3
        self.turn_timer = 0

        Ghost.instances.append(self)

    def move(self):
        def find_distance(a_pos, b_pos):
            a = pow(abs(a_pos[0] - b_pos[0]), 2)
            b = pow(abs(a_pos[1] - b_pos[1]), 2)
            return math.sqrt(a + b)

        def find_closest(facing, target_pos):
            return_dir = facing
            next_pos = [self.array_coord[0] + self.COORD_DIR[facing][0],
                        self.array_coord[1] + self.COORD_DIR[facing][1]]
            dir_min = find_distance(next_pos, target_pos)
            # check left turn
            if self.maze.can_move(self, left_turn(facing)):
                next_pos = [self.array_coord[0] + self.COORD_DIR[left_turn(facing)][0],
                            self.array_coord[1] + self.COORD_DIR[left_turn(facing)][1]]
                next_dir = find_distance(next_pos, target_pos)
                if next_dir < dir_min:
                    return_dir = left_turn(facing)
            # check right turn
            if self.maze.can_move(self, right_turn(facing)):
                next_pos = [self.array_coord[0] + self.COORD_DIR[right_turn(facing)][0],
                            self.array_coord[1] + self.COORD_DIR[right_turn(facing)][1]]
                next_dir = find_distance(next_pos, target_pos)
                if next_dir < dir_min:
                    return_dir = right_turn(facing)
            return return_dir

        step = self.step_len
        if self.timer >= self.player.power_time * self.main.fps:
            self.blue = False
        elif self.blue:
            self.timer += 1
            step = self.slow_step

        # normal play - scatter, chase, and frightened behaviours
        if self.mode == "normal":
            self.array_coord = [int((self.x + self.block_size / 2) / self.block_size),
                                int((self.y + self.block_size / 2) / self.block_size)]

            # only try changing direction if within bounds of maze array
            if self.block_size < self.x < self.main.display_width - self.block_size:
                my_row = int(self.y / self.block_size)
                my_col = int(self.x / self.block_size)
                player_row = int(self.player.y / self.block_size)
                player_col = int(self.player.x / self.block_size)
                player_dir = 0

                # FRIGHTENED MODE
                if self.blue:
                    # Check whether the player is visible from this ghost's perspective
                    # If they are on the same row or column, check all tiles in between
                    # If there are no walls, the ghost can see the player
                    see_player = False
                    if my_row == player_row or my_col == player_col:
                        wall = False  # flag for whether there is an obstruction between ghost and player
                        if my_col == player_col and my_row == player_row:
                            wall = True
                        elif my_row == player_row:
                            if my_col > player_col:
                                player_dir = self.DIR["LEFT"]
                                for i in range(0, my_col - player_col):
                                    if self.maze.maze_array[my_row][i + player_col] == 1:
                                        wall = True
                            elif player_col == my_col:
                                wall = True
                            else:
                                player_dir = self.DIR["RIGHT"]
                                for i in range(0, player_col - my_col):
                                    if self.maze.maze_array[my_row][i + my_col] == 1:
                                        wall = True
                        elif my_col == player_col:
                            if my_row > player_row:
                                player_dir = self.DIR["UP"]
                                for i in range(0, my_row - player_row):
                                    if self.maze.maze_array[i + player_row][my_col] == 1:
                                        wall = True
                            elif player_row == my_row:
                                wall = True
                            else:
                                player_dir = self.DIR["DOWN"]
                                for i in range(0, player_row - my_row):
                                    if self.maze.maze_array[i + my_row][my_col] == 1:
                                        wall = True
                        if not wall:
                            see_player = True

                    # Run away from the player
                    # If it is able to continue in the direction it is facing it will
                    # do so, so long as it does not go towards the player
                    if self.turn_timer > 1:
                        if see_player:
                            if self.look_dir == player_dir or not self.maze.can_move(self, self.look_dir):
                                self.look_dir = random.choice([left_turn(left_turn(player_dir)),
                                                               left_turn(player_dir), right_turn(player_dir)])
                                self.turn_timer = 0
                        # if player not visible, pick a random movement direction
                        else:
                            self.look_dir = random.choice([self.move_dir,
                                                           left_turn(self.move_dir), right_turn(self.move_dir)])
                            self.turn_timer = 0

                if (self.main.tick_counter / 60) / 7 < 1:
                    # scatter mode
                    target_coord = self.scatter_coord
                else:
                    # chase mode
                    target_coord = self.player.array_coord

                # move towards target
                # only try movement at intersection
                if step < self.x % self.block_size < self.block_size - step \
                        and step < self.y % self.block_size < self.block_size - step and self.turn_timer > 1:
                    if self.maze.can_move(self, left_turn(self.look_dir)) \
                            or self.maze.can_move(self, right_turn(self.look_dir)):
                        self.look_dir = find_closest(self.look_dir, target_coord)
                        self.turn_timer = 0
                    if not self.maze.can_move(self, self.look_dir):
                        self.look_dir = random.choice([left_turn(self.move_dir), right_turn(self.move_dir)])
                        self.turn_timer = 0

                # change move direction to match look direction if possible
                if self.look_dir != self.move_dir:
                    if self.maze.can_move(self, self.look_dir):
                        self.move_dir = self.look_dir
                    # if in a dead end, flip direction
                    if not (self.maze.can_move(self, self.move_dir)) \
                            and not (self.maze.can_move(self, left_turn(self.move_dir))) \
                            and not (self.maze.can_move(self, right_turn(self.move_dir))):
                        self.look_dir = left_turn(left_turn(self.move_dir))
                        self.move_dir = self.look_dir

                # do movement
                if self.maze.can_move(self, self.move_dir):
                    self.x += step * self.COORD_DIR[self.move_dir][0]
                    self.y += step * self.COORD_DIR[self.move_dir][1]

            # if outside maze, keep moving forwards until wrapped to the other side of the screen
            else:
                if self.move_dir == 2:  # moving left
                    self.x -= self.step_len
                    self.maze.center(self, "y", self.y)
                if self.move_dir == 0:  # moving right
                    self.x += self.step_len
                    self.maze.center(self, "y", self.y)
                # screen wrap
                if self.x < -self.size:
                    self.x = self.main.display_width
                if self.x > self.size + self.main.display_width:
                    self.x = -self.size

            self.turn_timer += 1

        # ghost stays inside the house
        elif self.mode == "house":
            if self.look_dir == self.DIR["DOWN"] or self.look_dir == self.DIR["UP"]:
                self.look_dir = random.choice([self.DIR["LEFT"], self.DIR["RIGHT"]])
                self.move_dir = self.look_dir
            if not (self.maze.can_move(self, self.move_dir)):
                self.look_dir = left_turn(left_turn(self.move_dir))
                self.move_dir = self.look_dir
            self.x += step * self.COORD_DIR[self.move_dir][0]

        # re-spawn if time has passed
        elif self.mode == "dead":
            if self.timer >= self.main.fps * self.respawn_time:
                self.x = 10 * self.block_size - self.block_size / 2
                self.y = 10 * self.block_size - self.block_size / 2
                self.mode = "normal"
            else:
                self.timer += 1

    def draw(self):
        def draw_body(col):
            pygame.draw.ellipse(self.display, col, (self.x - self.size / 2, self.y + self.offset - self.size / 2,
                                                    self.size, self.size * 0.95))
            pygame.draw.rect(self.display, col, (self.x - self.size / 2, self.y + self.offset,
                                                 self.size, self.size / 4))

            # alternate wobble shape
            if 0 < self.main.tick_counter % 20 < 10:
                pygame.draw.ellipse(self.display, col, (
                    self.x - self.size / 2, self.y + self.size / 6 + self.offset - 1, self.size / 3, self.size / 3))
                pygame.draw.ellipse(self.display, col, (
                    self.x - self.size / 6, self.y + self.size / 6 + self.offset - 1, self.size / 3, self.size / 3))
                pygame.draw.ellipse(self.display, col, (
                self.x + self.size / 6, self.y + self.size / 6 + self.offset - 1, self.size / 3, self.size / 3))
            else:
                pygame.draw.ellipse(self.display, col, (
                    self.x - self.size / 6 * 2, self.y + self.size / 6 + self.offset - 1, self.size / 3, self.size / 3))
                pygame.draw.ellipse(self.display, col, (
                    self.x, self.y + self.size / 6 + self.offset - 1, self.size / 3, self.size / 3))

        def draw_eyes(move_dir):
            eye_width = self.size / 3
            eye_height = eye_width * 3 / 2
            pupil_diam = eye_width * 3 / 4
            eye_separation = self.size * 0.1
            y_pos = self.y - eye_height / 2 + self.offset

            x_off = 0
            y_off = 0
            if move_dir == self.DIR["RIGHT"]:
                x_off = 1
            elif move_dir == self.DIR["LEFT"]:
                x_off = -1
            elif move_dir == self.DIR["UP"]:
                y_off = -1
            elif move_dir == self.DIR["DOWN"]:
                y_off = 1

            # eye whites
            pygame.draw.ellipse(self.display, (255, 255, 255),
                                (self.x - eye_width - (eye_separation / 2) + x_off, y_pos + y_off,
                                 eye_width, eye_height))
            pygame.draw.ellipse(self.display, (255, 255, 255),
                                (self.x + (eye_separation / 2) + x_off, y_pos + y_off,
                                 eye_width, eye_height))

            # eye pupils
            pygame.draw.circle(self.display, (0, 0, 0), (round(self.x - eye_width / 2 - eye_separation / 2 + x_off * 2),
                               round(y_pos + eye_height / 2 + y_off * 2)), round(pupil_diam / 2))
            pygame.draw.circle(self.display, (0, 0, 0), (round(self.x + eye_width / 2 + eye_separation / 2 + x_off * 2),
                               round(y_pos + eye_height / 2 + y_off * 2)), round(pupil_diam / 2))

        if self.mode != "dead":
            if self.blue and self.player.powered_up:
                # blink blue and white in the last 2 seconds of power up time
                if 0 < self.timer % 40 < 20 \
                        and self.timer + (2 * self.main.fps) >= self.player.power_time * self.main.fps:
                    color = (200, 200, 255)  # very light blue
                else:
                    color = (50, 50, 200)  # dark blue
            else:
                color = self.base_color
            draw_body(color)
            draw_eyes(self.move_dir)

    def collide(self):
        dist_x = abs(self.x - self.player.x)
        dist_y = abs(self.y - self.player.y)

        touch_distance = self.size / 2

        if dist_x < touch_distance and dist_y < touch_distance and self.mode != "dead":
            if self.blue and self.player.powered_up:
                self.timer = 0
                self.main.score += 10
                self.blue = False
                self.mode = "dead"
            else:
                self.main.game_state = "lose"
