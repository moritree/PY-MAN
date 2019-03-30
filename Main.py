import pygame
import pygame.freetype
import Maze
import Pacman
import Items


class Main:
    def __init__(self):
        self.block_size = 30
        self.display_width = 19 * self.block_size
        self.display_height = self.display_width + 2*self.block_size

        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        self.tick_counter = 1

        self.coins = 0

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
        player.move()
        factory.check_collisions()

    def draw(self, display, maze, player, factory):
        pygame.draw.rect(display, (0, 0, 0), (0, 0, self.display_width, self.display_height))

        maze.draw()
        factory.draw_all()
        player.draw()

        game_font = pygame.freetype.SysFont("Helvetica.ttf", 40)
        game_font.render_to(display, (15, 15), "COINS: " + str(self.coins), (255, 255, 255))

    def run(self):
        pygame.init()
        pygame.display.set_caption("Pacman")
        display_surf = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.font.init()

        maze = Maze.Maze(display_surf, self.block_size)
        player = Pacman.Pacman(9, 11, self.block_size, display_surf, maze, self)
        factory = Items.ItemFactory(maze.maze_array, self.block_size,
                                    display_surf, player, self)
        factory.setup()

        running = True
        while running:
            self.events(player)
            self.loop(maze, player, factory)
            self.draw(display_surf, maze, player, factory)

            pygame.display.update()
            self.fps_clock.tick(self.fps)
            self.tick_counter += 1


if __name__ == "__main__":
    main = Main()
    main.run()
