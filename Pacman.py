import pygame


class Pacman:
    def __init__(self, x, y, block_size, display, maze):
        self.block_size = block_size
        self.offset = block_size*2
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2

        self.size = 20
        self.step_len = 1

        self.display = display
        self.maze = maze

        self.look_dir = "UP"
        self.move_dir = "UP"

    def move(self):
        # check movement directions
        half_block = self.block_size/2
        can_up = False
        if (self.look_dir == "UP") or self.move_dir == "UP":
            tmp_y = int((self.y - self.block_size / 2 - self.step_len) / self.block_size)
            if self.maze.maze_array[tmp_y][int((self.x + half_block - 1)/ self.block_size)] == 0 and \
                    self.maze.maze_array[tmp_y][int((self.x - half_block + 1)/ self.block_size)] == 0:
                can_up = True
        can_down = False
        if (self.look_dir == "DOWN") or self.move_dir == "DOWN":
            tmp_y = int((self.y + self.block_size / 2 + self.step_len) / self.block_size)
            if self.maze.maze_array[tmp_y][int((self.x + half_block - 1)/ self.block_size)] == 0 and \
                    self.maze.maze_array[tmp_y][int((self.x - half_block + 1)/ self.block_size)] == 0:
                can_down = True
        can_left = False
        if (self.look_dir == "LEFT") or self.move_dir == "LEFT":
            tmp_x = int((self.x - self.block_size / 2 - self.step_len) / self.block_size)
            if self.maze.maze_array[int((self.y + half_block - 1) / self.block_size)][tmp_x] == 0 and \
                    self.maze.maze_array[int((self.y - half_block + 1) / self.block_size)][tmp_x] == 0:
                can_left = True
        can_right = False
        if (self.look_dir == "RIGHT") or self.move_dir == "RIGHT":
            tmp = int((self.x + self.block_size / 2 + self.step_len) / self.block_size)
            if self.maze.maze_array[int((self.y + half_block - 1) / self.block_size)][tmp] == 0 and \
                    self.maze.maze_array[int((self.y - half_block + 1) / self.block_size)][tmp] == 0:
                can_right = True

        # change movement direction if possible
        if self.look_dir != self.move_dir:
            if self.look_dir == "UP" and can_up: self.move_dir = "UP"
            if self.look_dir == "DOWN" and can_down: self.move_dir = "DOWN"
            if self.look_dir == "LEFT" and can_left: self.move_dir = "LEFT"
            if self.look_dir == "RIGHT" and can_right: self.move_dir = "RIGHT"

        # move
        if self.move_dir == "UP" and can_up: self.y -= self.step_len
        if self.move_dir == "DOWN" and can_down: self.y += self.step_len
        if self.move_dir == "LEFT" and can_left: self.x -= self.step_len
        if self.move_dir == "RIGHT" and can_right: self.x += self.step_len

    def draw(self):
        pygame.draw.rect(self.display, (255, 255, 0),
                         (self.x - self.size / 2, self.y - self.size / 2 + self.offset, self.size, self.size))
