import pygame
import Ghost


class Maze:
    def __init__(self, display, main):
        self.main = main
        self.display = display
        self.block_size = main.block_size
        self.offset = main.offset

        # draw maze
        self.maze_array = [[0] * main.maze_width for i in range(main.maze_height)]  # [y][x]

        if main.maze_width == 19 and main.maze_height == 19:
            self.maze_array[0]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            self.maze_array[1]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            self.maze_array[2]  = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
            self.maze_array[3]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            self.maze_array[4]  = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
            self.maze_array[5]  = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
            self.maze_array[6]  = [1, 1, 1, 1, 0, 1, 1, 1, 4, 1, 4, 1, 1, 1, 0, 1, 1, 1, 1]
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
        if main.maze_width == 19 and main.maze_height == 21:
            self.maze_array[0]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            self.maze_array[1]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            self.maze_array[2]  = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
            self.maze_array[3]  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            self.maze_array[4]  = [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
            self.maze_array[5]  = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
            self.maze_array[6]  = [1, 1, 1, 1, 0, 1, 1, 1, 4, 1, 4, 1, 1, 1, 0, 1, 1, 1, 1]
            self.maze_array[7]  = [3, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3, 3]
            self.maze_array[8]  = [1, 1, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 0, 1, 0, 1, 1, 1, 1]
            self.maze_array[9]  = [0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0]
            self.maze_array[10] = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]
            self.maze_array[11] = [3, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 3, 3]
            self.maze_array[12] = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1]
            self.maze_array[13] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            self.maze_array[14] = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]
            self.maze_array[15] = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
            self.maze_array[16] = [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1]
            self.maze_array[17] = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]
            self.maze_array[18] = [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
            self.maze_array[19] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            self.maze_array[20] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def draw(self):
        # draw maze
        for i in range(self.main.maze_width):
            for j in range(self.main.maze_height):
                if self.maze_array[j][i] == 1:
                    pygame.draw.rect(self.display, (0, 0, 210), (i * self.block_size, j * self.block_size + self.offset,
                                                                 self.block_size, self.block_size))
                elif self.maze_array[j][i] == 2:
                    pygame.draw.rect(self.display, (200, 0, 0), (i * self.block_size, j * self.block_size + self.offset,
                                                                 self.block_size, self.block_size))
                else:
                    pygame.draw.rect(self.display, (0, 0, 0), (i * self.block_size, j * self.block_size + self.offset,
                                                               self.block_size, self.block_size))

    def center(self, entity, var, coord):
        setattr(entity, var, int(coord / self.block_size) * self.block_size + self.block_size / 2)

    def can_move(self, entity, dir):
        allowed = [0, 3, 4]
        if isinstance(entity, Ghost.Ghost):
            if (entity.mode == "normal" and 9 <= entity.array_coord[0] <= 11 and 8 <= entity.array_coord[1] <= 11) \
                    or entity.mode == "dead":
                allowed = [0, 2, 3]
            elif dir == entity.DIR["UP"]:
                allowed = [0, 3]

        if dir == entity.DIR["UP"] or dir == entity.DIR["DOWN"]:
            x_plus = int((entity.x + self.block_size / 2 - entity.step) / self.block_size)
            x_minus = int((entity.x - self.block_size / 2 + entity.step) / self.block_size)
            tmp_y = int((entity.y - self.block_size / 2 - entity.step) / self.block_size)
            if dir == entity.DIR["DOWN"]:
                tmp_y = int((entity.y + self.block_size / 2 + entity.step) / self.block_size)
            if self.maze_array[tmp_y][x_plus] in allowed and self.maze_array[tmp_y][x_minus] in allowed:
                return True
        elif dir == entity.DIR["LEFT"] or dir == entity.DIR["RIGHT"]:
            y_plus = int((entity.y + self.block_size / 2 - entity.step) / self.block_size)
            y_minus = int((entity.y - self.block_size / 2 + entity.step) / self.block_size)
            tmp_x = int((entity.x - self.block_size / 2 - entity.step) / self.block_size)
            if dir == entity.DIR["RIGHT"]:
                tmp_x = int((entity.x + entity.block_size / 2 + entity.step) / self.block_size)
            if self.maze_array[y_plus][tmp_x] in allowed and self.maze_array[y_minus][tmp_x] in allowed:
                return True
        else:
            return False
