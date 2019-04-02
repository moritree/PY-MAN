import pygame
import random


def draw_ghosts():
    for ghost in Ghost.instances:
        ghost.draw()


def check_collisions():
    for ghost in Ghost.instances:
        ghost.collide()


def move_all():
    for ghost in Ghost.instances:
        ghost.move()


class Ghost:
    instances = []

    def __init__(self, maze, block_size, display, player, main, x, y, color):
        self.array = maze.maze_array
        self.block_size = block_size
        self.offset = block_size * 2

        self.display = display
        self.player = player
        self.main = main
        self.maze = maze

        self.look_dir = "UP"
        self.move_dir = "UP"

        self.step_len = block_size / 24
        self.slow_step = block_size / 30

        self.size = 18
        self.x = x * block_size - block_size / 2
        self.y = y * block_size - block_size / 2

        self.base_color = color
        self.here = True

        self.timer = 0
        Ghost.instances.append(self)

    def move(self):
        if self.here:
            step = self.step_len
            if self.player.powered_up:
                step = self.slow_step

            # only try changing direction within bounds of maze array
            if self.block_size < self.x < self.main.display_width - self.block_size:
                # Check if this ghost can 'see' the player.
                # If the player is in the same row or column as the ghost and there are no walls between them,
                # the ghost will chase the player. Otherwise it will move randomly.

                my_row = int(self.y / self.block_size)
                my_col = int(self.x / self.block_size)
                player_row = int(self.player.y / self.block_size)
                player_col = int(self.player.x / self.block_size)

                # Check whether the player is visible from this ghost's perspective
                # If they are on the same row or column, check all tiles in between
                # If there are no walls, the ghost can see the player
                see_player = False
                if my_row == player_row or my_col == player_col:
                    flag = False
                    if my_row == player_row:
                        if my_col > player_col:
                            for i in range(0, my_col - player_col):
                                if self.array[my_row][i + player_col] == 1:
                                    flag = True
                        elif player_col == my_col:
                            flag = True
                        else:
                            for i in range(0, player_col - my_col):
                                if self.array[my_row][i + my_col] == 1:
                                    flag = True
                    if my_col == player_col:
                        if my_row > player_row:
                            for i in range(0, my_row - player_row):
                                if self.array[i + player_row][my_col] == 1:
                                    flag = True
                        elif player_row == my_row:
                            flag = True
                        else:
                            for i in range(0, player_row - my_row):
                                if self.array[i + my_row][my_col] == 1:
                                    flag = True
                    if not flag:
                        see_player = True

                # If the player is visible, either chase or run away
                if see_player:
                    # Run away from the player if player is powered up
                    # If it is able to continue in the direction it is facing it will
                    # do so, so long as it does not go towards the player
                    if self.player.powered_up:
                        if my_row == player_row:
                            if my_col > player_col:
                                direction = random.choice(["UP", "DOWN", "RIGHT"])
                                if self.look_dir == "LEFT" or not self.maze.can_move(self, self.look_dir):
                                    self.look_dir = direction
                            else:
                                direction = random.choice(["UP", "DOWN", "LEFT"])
                                if self.look_dir == "RIGHT" or not self.maze.can_move(self, self.look_dir):
                                    self.look_dir = direction
                        elif my_col == player_col:
                            if my_row > player_row:
                                direction = random.choice(["LEFT", "RIGHT", "DOWN"])
                                if self.look_dir == "UP" or not self.maze.can_move(self, self.look_dir):
                                    self.look_dir = direction
                            else:
                                direction = random.choice(["LEFT", "RIGHT", "UP"])
                                if self.look_dir == "DOWN" or not self.maze.can_move(self, self.look_dir):
                                    self.look_dir = direction
                    # Otherwise, chase the player
                    else:
                        if my_row == player_row:
                            if my_col > player_col and self.maze.can_move(self, "LEFT"):
                                self.look_dir = "LEFT"
                            elif abs(self.x - self.player.x) < self.step_len:
                                self.look_dir = None
                            elif self.maze.can_move(self, "RIGHT"):
                                self.look_dir = "RIGHT"
                        if my_col == player_col:
                            if my_row > player_row and self.maze.can_move(self, "UP"):
                                self.look_dir = "UP"
                            elif abs(self.y - self.player.y) < self.step_len:
                                self.look_dir = None
                            elif self.maze.can_move(self, "DOWN"):
                                self.look_dir = "DOWN"
                # if player not visible, pick a random movement direction
                else:
                    if self.move_dir == "UP":
                        self.look_dir = random.choice(["LEFT", "RIGHT", "UP"])
                    if self.move_dir == "DOWN":
                        self.look_dir = random.choice(["LEFT", "RIGHT", "DOWN"])
                    if self.move_dir == "LEFT":
                        self.look_dir = random.choice(["DOWN", "LEFT", "UP"])
                    if self.move_dir == "RIGHT":
                        self.look_dir = random.choice(["UP", "RIGHT", "DOWN"])

                # change move dir if possible
                if self.look_dir != self.move_dir:
                    if self.look_dir == "UP" and self.maze.can_move(self, "UP"):
                        self.move_dir = "UP"
                    elif self.look_dir == "DOWN" and self.maze.can_move(self, "DOWN"):
                        self.move_dir = "DOWN"
                    elif self.look_dir == "LEFT" and self.maze.can_move(self, "LEFT"):
                        self.move_dir = "LEFT"
                    elif self.look_dir == "RIGHT" and self.maze.can_move(self, "RIGHT"):
                        self.move_dir = "RIGHT"
                    # if in a dead end, flip direction
                    else:
                        if self.move_dir == "UP" and not self.maze.can_move(self, "UP") and not \
                                self.maze.can_move(self, "LEFT") and not self.maze.can_move(self, "RIGHT"):
                            self.move_dir = "DOWN"
                        elif self.move_dir == "DOWN" and not self.maze.can_move(self, "DOWN") and not \
                                self.maze.can_move(self, "LEFT") and not self.maze.can_move(self, "RIGHT"):
                            self.move_dir = "UP"
                        elif self.move_dir == "LEFT" and not self.maze.can_move(self, "LEFT") and not \
                                self.maze.can_move(self, "UP") and not self.maze.can_move(self, "DOWN"):
                            self.move_dir = "RIGHT"
                        elif self.move_dir == "RIGHT" and not self.maze.can_move(self, "RIGHT") and not \
                                self.maze.can_move(self, "UP") and not self.maze.can_move(self, "DOWN"):
                            self.move_dir = "LEFT"

                # do movement
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

            # if outside maze, keep moving until wrapped to the other side of the screen
            else:
                if self.move_dir == "LEFT":
                    self.x -= self.step_len
                    self.maze.center(self, "y", self.y)
                if self.move_dir == "RIGHT":
                    self.x += self.step_len
                    self.maze.center(self, "y", self.y)

                # screen wrap
                if self.x < -self.size:
                    self.x = self.main.display_width
                if self.x > self.size + self.main.display_width:
                    self.x = -self.size

        # respawn
        elif self.timer >= 60*10:
            self.x = 10 * self.block_size - self.block_size / 2
            self.y = 10 * self.block_size - self.block_size / 2
            self.here = True
        else:
            self.timer += 1

    def draw(self):
        if self.here:
            if self.player.powered_up:
                # blink in the last 2 seconds of player's power up time
                if 0 < self.player.timer % 40 < 20 \
                        and self.player.timer + 2 * self.main.fps >= self.player.power_time * self.main.fps:
                    color = (200, 200, 255)
                else:
                    color = (50, 50, 200)
            else:
                color = self.base_color

            pygame.draw.rect(self.display, color, (self.x - self.size / 2, self.y - self.size / 2 + self.offset,
                                                   self.size, self.size))

    def collide(self):
        dist_x = abs(self.x - self.player.x)
        dist_y = abs(self.y - self.player.y)

        touch_distance = self.size/2 + self.player.size/2

        if dist_x < touch_distance and dist_y < touch_distance and self.here:
            if self.player.powered_up:
                self.here = False
                self.main.coins += 10
            else:
                self.main.running = False
