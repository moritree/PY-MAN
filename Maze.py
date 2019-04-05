import pygame
from collections import defaultdict


class Maze:
    def __init__(self, display, main):
        self.display = display
        self.block_size = main.block_size
        self.offset = main.offset

        # draw maze
        self.maze_array = [[0] * 19 for i in range(19)] # [y][x]

        self.maze_array[0]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.maze_array[1]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.maze_array[2]  = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
        self.maze_array[3]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.maze_array[4]  = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
        self.maze_array[5]  = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        self.maze_array[6]  = [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
        self.maze_array[7]  = [3, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3, 3]
        self.maze_array[8]  = [1, 1, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1]
        self.maze_array[9]  = [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0]
        self.maze_array[10] = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]
        self.maze_array[11] = [3, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3, 3]
        self.maze_array[12] = [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
        self.maze_array[13] = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        self.maze_array[14] = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
        self.maze_array[15] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.maze_array[16] = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
        self.maze_array[17] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.maze_array[18] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def draw(self):
        # draw maze
        for i in range(19):
            for j in range(19):
                if self.maze_array[j][i] == 1:
                    pygame.draw.rect(self.display, (0, 0, 210), (i * self.block_size, j * self.block_size + self.offset,
                                                                 self.block_size, self.block_size))
                elif self.maze_array[j][i] == 0 or self.maze_array[j][i] == 3:
                    pygame.draw.rect(self.display, (0, 0, 0), (i * self.block_size, j * self.block_size + self.offset,
                                                               self.block_size, self.block_size))
                elif self.maze_array[j][i] == 2:
                    pygame.draw.rect(self.display, (200, 0, 0), (i * self.block_size, j * self.block_size + self.offset,
                                                                 self.block_size, self.block_size))

    def center(self, entity, var, coord):
        setattr(entity, var, int(coord / self.block_size) * self.block_size + self.block_size / 2)

    def can_move(self, entity, dir):
        if dir == "UP" or dir == 3:
            tmp_y = int((entity.y - self.block_size / 2 - entity.step_len) / self.block_size)
            if self.maze_array[tmp_y][
                int((entity.x + (self.block_size / 2) - entity.step_len) / self.block_size)] != 1 and \
                    self.maze_array[tmp_y][
                        int((entity.x - (self.block_size / 2) + entity.step_len) / self.block_size)] != 1:
                return True
        elif dir == "DOWN" or dir == 1:
            tmp_y = int((entity.y + self.block_size / 2 + entity.step_len) / self.block_size)
            if self.maze_array[tmp_y][
                int((entity.x + (self.block_size / 2) - entity.step_len) / self.block_size)] != 1 and \
                    self.maze_array[tmp_y][
                        int((entity.x - (self.block_size / 2) + entity.step_len) / self.block_size)] != 1:
                return True
        elif dir == "LEFT" or dir == 2:
            tmp_x = int((entity.x - self.block_size / 2 - entity.step_len) / self.block_size)
            if self.maze_array[int((entity.y + (self.block_size / 2) - entity.step_len) / self.block_size)][
                tmp_x] != 1 and \
                    self.maze_array[int((entity.y - (self.block_size / 2) + entity.step_len) / self.block_size)][
                        tmp_x] != 1:
                return True
        elif dir == "RIGHT" or dir == 0:
            tmp = int((entity.x + entity.block_size / 2 + entity.step_len) / self.block_size)
            if self.maze_array[int((entity.y + (self.block_size / 2) - entity.step_len) / self.block_size)][
                tmp] != 1 and \
                    self.maze_array[int((entity.y - (self.block_size / 2) + entity.step_len) / self.block_size)][
                        tmp] != 1:
                return True
        else:
            return False
