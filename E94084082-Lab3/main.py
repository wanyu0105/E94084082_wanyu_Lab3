import pygame
from enemy import EnemyGroup
import os
from settings import WIN_WIDTH, WIN_HEIGHT, FPS

# initialization
pygame.init()
# load image
BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "Map.png"))
HP_IMAGE = pygame.image.load(os.path.join("images", "hp.png"))
HP_GRAY_IMAGE = pygame.image.load(os.path.join("images", "hp_gray.png"))
# set the title and icon
pygame.display.set_caption("My TD game")


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
        self.hp_images = [pygame.transform.scale(HP_IMAGE, (40, 40)),
                          pygame.transform.scale(HP_GRAY_IMAGE, (40, 40))]
        self.enemies = EnemyGroup()
        self.base = pygame.Rect(430, 90, 195, 130)

    def collide_base(self, enemy):
        """
        Return True if the enemy collide with base.
        :param enemy: object (Enemy())
        :return: Bool
        """
        x, y = self.base.center
        width, height = self.base.w, self.base.h
        if x - width // 2 < enemy.x < x + width // 2 and y - height // 2 < enemy.y < y + height // 2:
            return True
        return False

    def draw(self):
        """
        Draw everything in this method.
        :return: None
        """
        # draw background
        self.win.blit(self.bg_image, (0, 0))
        # draw enemy
        for en in self.enemies.get():
            en.draw(self.win)

    def game_run(self):
        # game loop
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            # event loop
            for event in pygame.event.get():
                # quit the game
                if event.type == pygame.QUIT:
                    run = False
                # generate enemy of the next wave
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n and self.enemies.is_empty():
                        self.enemies.generate(3)

            # enemy loop
            self.enemies.campaign()
            for en in self.enemies.get():
                en.move()
                # delete the object when it reach the base
                if self.collide_base(en):
                    self.enemies.retreat(en)

            # draw everything
            self.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    covid_game = Game()
    covid_game.game_run()