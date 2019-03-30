import pygame


class ItemFactory:
    def __init__(self, maze_array, block_size, display, player, main):
        self.array = maze_array
        self.block_size = block_size

        self.display = display
        self.player = player
        self.main = main

    def make_coins(self):
        for i in range(0, len(self.array)):
            for j in range(0, len(self.array[i])):
                if self.array[j][i] == 0:
                    coin = Coin(i, j, self.block_size, self.display)

    def draw_all(self):
        for coin in Coin.instances:
            coin.draw()

    def check_collisions(self):
        for coin in Coin.instances:
            coin.collide(self.player, self.main)


class Coin:
    instances = []
    coin_size = 10

    def __init__(self, x, y, block_size, display):
        Coin.instances.append(self)

        self.display = display
        self.x = x * block_size + block_size / 2
        self.y = y * block_size + block_size / 2

        self.here = True
        self.timer = 0

    def draw(self):
        if self.here:
            half = self.coin_size/2
            pygame.draw.rect(self.display, (255, 255, 255), (self.x - half, self.y - half,
                                                             self.coin_size, self.coin_size))

    def collide(self, player, main):
        dist_x = abs(self.x - player.x)
        dist_y = abs(self.y - player.y)

        if dist_x < self.coin_size and dist_y < self.coin_size and self.here:
            self.here = False
            main.coins += 1
            self.timer = 0
            print(main.coins)
        elif not self.here and self.timer >= 30 * 60:
            self.here = True
        else:
            self.timer += 1
