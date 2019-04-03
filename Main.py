import pygame
import pygame.freetype
import Maze
import Pacman
import Items
import Ghost


class Main:
    def __init__(self):
        self.block_size = 30
        self.display_width = 19 * self.block_size
        self.display_height = self.display_width + 2*self.block_size

        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        self.tick_counter = 1

        self.coins = 0
        self.running = True

        self.game_state = "run"

    def events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    setattr(player, "look_dir", "UP")
                if event.key == pygame.K_DOWN:
                    setattr(player, "look_dir", "DOWN")
                if event.key == pygame.K_LEFT:
                    setattr(player, "look_dir", "LEFT")
                if event.key == pygame.K_RIGHT:
                    setattr(player, "look_dir", "RIGHT")
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return

    def loop(self, maze, player, factory):
        if self.game_state == "run":
            player.move()
            factory.check_collisions()
            Ghost.move_all()
            Ghost.check_collisions()

    def draw(self, display, maze, player, factory):
        pygame.draw.rect(display, (0, 0, 0), (0, 0, self.display_width, self.display_height))

        maze.draw()
        factory.draw_all()
        player.draw()
        Ghost.draw_ghosts()

        game_font = pygame.freetype.SysFont("Helvetica.ttf", 40)
        game_font.render_to(display, (15, 15), "SCORE: " + str(self.coins), (255, 255, 255))

    def win_condition(self):
        flag = False
        for coin in Items.Coin.instances:
            if coin.here:
                flag = True
        if not flag:
            self.game_state = "win"

    def run(self):
        pygame.init()
        pygame.display.set_caption("PY-MAN")
        display_surf = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.font.init()

        # initialize maze and player
        maze = Maze.Maze(display_surf, self.block_size)
        player = Pacman.Pacman(9, 11, self.block_size, display_surf, maze, self)

        # generate all coins and power ups
        factory = Items.ItemFactory(maze, self.block_size, display_surf, player, self)
        factory.setup()

        # spawn ghosts
        ghost1 = Ghost.Ghost(maze, self.block_size, display_surf, player, self, 9, 10, (255, 80, 80))
        ghost2 = Ghost.Ghost(maze, self.block_size, display_surf, player, self, 10, 10, (255, 100, 150))
        ghost3 = Ghost.Ghost(maze, self.block_size, display_surf, player, self, 11, 10, (100, 255, 255))
        ghost4 = Ghost.Ghost(maze, self.block_size, display_surf, player, self, 10, 8, (255, 200, 000))

        while self.running:
            if self.game_state == "run":
                self.events(player)
                self.loop(maze, player, factory)
                self.draw(display_surf, maze, player, factory)

                pygame.display.update()
                self.fps_clock.tick(self.fps)
                self.tick_counter += 1

            elif self.game_state == "win":
                self.running = False
            elif self.game_state == "lose":
                self.running = False


if __name__ == "__main__":
    main = Main()
    main.run()
