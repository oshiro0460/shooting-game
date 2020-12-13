import pygame
import random
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
bg_x = 0

def main():
    global bg_x

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("shooting_game")

    all = pygame.sprite.RenderUpdates()
    background = pygame.image.load("data/background.png")
    enemy = pygame.sprite.Group()
    bullet = pygame.sprite.Group()
    enemy_bullet = pygame.sprite.Group()

    Player.containers = all
    Bullet.containers = all, bullet
    Enemy.containers = all, enemy
    EnemyBullet.containers = all, enemy_bullet

    player = Player()
    Enemy((SCREEN_WIDTH, SCREEN_HEIGHT/2))

    clock = pygame.time.Clock()

    while True:
        clock.tick(120)
        all.update()
        collision_detection(player, enemy, bullet, enemy_bullet)
        bg_x = (bg_x-1)%1600
        screen.blit(background, [bg_x-1600, 0])
        screen.blit(background, [bg_x, 0])
        all.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.create_bullet()


def collision_detection(player, enemys, bullets, enemy_bullets):
    enemy_collided = pygame.sprite.groupcollide(enemys, bullets, False, True)
    for enemy in list(enemy_collided.keys()):
        enemy.hp -= 1
    enemy_bullet_collided = pygame.sprite.spritecollide(player, enemy_bullets, True)
    if enemy_bullet_collided:
        player.kill()
    player_collided = pygame.sprite.spritecollide(player, enemys, False)
    if player_collided:
        player.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("data/player.png")
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def create_bullet(self):
        return Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


class Bullet(pygame.sprite.Sprite):
    speed = 10
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((50,2))
        self.image.fill((50, 200, 200))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.x >= SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    speed = 1
    move_range = 200
    prob_shooting = 0.05
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.hp = 25
        self.status = 0
        self.image = pygame.image.load("data/enemy_0.png")
        self.rect = self.image.get_rect(center = pos)
        self.rect.center = pos
        self.top = pos[1]
        self.bottom = self.top + self.move_range
    def update(self):
        if self.status == 0:
            self.rect.move_ip(-self.speed, 0)
            if self.rect.center[1] < 0 or self.rect.center[1] > self.bottom:
                self.speed = -self.speed
            if self.rect.center == (SCREEN_WIDTH - 200, SCREEN_HEIGHT/2):
                self.status += 1
        elif self.status == 1:
            self.rect.move_ip(0, -self.speed)
            if self.rect.center[1] < 0 or self.rect.center[1] > self.bottom:
                self.speed = -self.speed
            if random.random() < self.prob_shooting:
                EnemyBullet((self.rect.center[0] - 75, self.rect.center[1] + 35), -5, (50, 200, 200))
            if random.random() < self.prob_shooting:
                EnemyBullet((self.rect.center[0] - 80, self.rect.center[1] - 30), -2, (150, 0, 0))
        if self.hp == 15:
            self.image = pygame.image.load("data/enemy_1.png")
        elif self.hp <= 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, color):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.speed = speed
        self.image = pygame.Surface((50,5))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    main()
