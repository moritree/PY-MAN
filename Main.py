import pygame
import pygame.freetype
import Maze
import PacMan
import Items
import Ghost


class Main:
    def __init__(self):
        self.block_size = 30
        self.offset = self.block_size * 2

        self.maze_width = 19
        self.maze_height = 21

        self.lives = 3;

        self.display_width = self.maze_width * self.block_size
        self.display_height = self.maze_height * self.block_size + self.offset

        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        self.tick_counter = 1
        self.temp_counter = 0

        self.score = 0
        self.coins = 0
        self.total_coins = 0
        self.running = True

        self.game_state = "run"

    def events(self, player):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    setattr(player, "look_dir", player.DIR["UP"])
                if event.key == pygame.K_DOWN:
                    setattr(player, "look_dir", player.DIR["DOWN"])
                if event.key == pygame.K_LEFT:
                    setattr(player, "look_dir", player.DIR["LEFT"])
                if event.key == pygame.K_RIGHT:
                    setattr(player, "look_dir", player.DIR["RIGHT"])
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        return

    def loop(self, player, item_factory, ghost_factory):
        if self.game_state == "run":
            ghost_factory.activation()
            player.move()
            item_factory.check_collisions()
            Ghost.move_all()
            Ghost.check_collisions()

    def draw(self, display, maze, player, item_factory):
        pygame.draw.rect(display, (0, 0, 0), (0, 0, self.display_width, self.display_height))

        maze.draw()
        item_factory.draw_all()
        player.draw(self.game_state)
        Ghost.draw_ghosts()

        game_font = pygame.freetype.SysFont("Helvetica.ttf", 40)
        game_font.render_to(display, (15, 15), "SCORE: " + str(self.score), (255, 255, 255))
        game_font = pygame.freetype.SysFont("Helvetica.ttf", 20)
        game_font.render_to(display, (300, 15), str(self.lives) + " LIVES", (255, 255, 255))

    def run(self):
        # initialize
        pygame.init()
        pygame.display.set_caption("PY-MAN")
        display_surf = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.font.init()

        # spawn maze and player
        maze = Maze.Maze(display_surf, self)
        player = PacMan.PacMan(9, 11, display_surf, maze, self)

        # generate all coins and power ups
        item_factory = Items.ItemFactory(maze, self.block_size, display_surf, player, self)
        item_factory.setup()

        # spawn ghosts
        ghost_factory = Ghost.GhostFactory(maze, display_surf, player, self)

        # running game loop
        while self.running:
            if self.game_state in("run", "respawn"):

                # main game loop
                self.events(player)
                self.loop(player, item_factory, ghost_factory)
                self.draw(display_surf, maze, player, item_factory)

                # check win condition
                if self.coins >= self.total_coins:
                    self.game_state = "win"

                pygame.display.update()
                self.fps_clock.tick(self.fps)
                self.tick_counter += 1

            # end game at win/lose
            elif self.game_state == "win":
                self.running = False
            elif self.game_state == "lose":
                self.running = False


if __name__ == "__main__":
    main = Main()
    main.run()
