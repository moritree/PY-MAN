import pygame


class ItemFactory:
    def __init__(self, maze, block_size, display, player, main):
        self.array = maze.maze_array
        self.block_size = block_size

        self.display = display
        self.player = player
        self.main = main
        self.maze = maze

    def setup(self):
        self.make_powerups()
        self.make_coins()

    def make_powerups(self):
        x = [1, 17, 1, 17]
        y = [2, 15, 15, 2]
        for i in range(len(x)):
            PowerUp(x[i], y[i], self.block_size, self.display)

    def make_coins(self):
        for i in range(0, len(self.array)):
            for j in range(0, len(self.array[i])):
                if self.array[i][j] in([0, 4]):
                    flag = False
                    for item in PowerUp.instances:
                        if item.x_coord == j and item.y_coord == i:
                            flag = True
                    if not flag:
                        Coin(j, i, self.block_size, self.display, self.main)

    def draw_all(self):
        for power_up in PowerUp.instances:
            power_up.draw()
        for coin in Coin.instances:
            coin.draw()

    def check_collisions(self):
        for power_up in PowerUp.instances:
            power_up.collide(self.player, self.main)
        for coin in Coin.instances:
            coin.collide(self.player, self.main)


class Coin:
    instances = []
    coin_size = 6

    def __init__(self, x, y, block_size, display, main):
        Coin.instances.append(self)

        self.display = display
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2
        self.offset = block_size*2

        main.total_coins += 1
        self.here = True

    def draw(self):
        if self.here:
            half = self.coin_size/2
            pygame.draw.ellipse(self.display, (255, 255, 255), (self.x - half, self.y - half + self.offset,
                                                                self.coin_size, self.coin_size))

    def collide(self, player, main):
        dist_x = abs(self.x - player.x)
        dist_y = abs(self.y - player.y)

        if dist_x < self.coin_size and dist_y < self.coin_size and self.here:
            self.here = False
            main.coins += 1
            main.score += 1


class PowerUp:
    instances = []
    size = 12

    def __init__(self, x, y, block_size, display):
        PowerUp.instances.append(self)

        self.display = display

        self.x_coord = x
        self.y_coord = y
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2
        self.offset = block_size*2

        self.here = True

    def draw(self):
        if self.here:
            half = self.size/2
            pygame.draw.ellipse(self.display, (255, 255, 255), (self.x - half, self.y - half + self.offset,
                                                                self.size, self.size))

    def collide(self, player, main):
        dist_x = abs(self.x - player.x)
        dist_y = abs(self.y - player.y)

        if dist_x < self.size and dist_y < self.size and self.here:
            self.here = False
            player.power_up(8)
