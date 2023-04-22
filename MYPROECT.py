from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),
                                     (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    '''Керування клавішами'''

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x < w - 70:
            self.rect.x = self.rect.x + self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y = self.rect.y - self.speed
        if keys[K_DOWN] and self.rect.y < h - 70:
            self.rect.y = self.rect.y + self.speed


class Enemy(GameSprite):
    def update(self):
        if self.rect.x >= w-100:
            self.side = "left"
            print("left")
        if self.rect.x <= w-250:
            self.side = "right"
            print("right")
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_y, wall_w, wall_h):
        super().__init__()
        self.color = color
        self.width = wall_w
        self.height = wall_h
        self.image = Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

mixer.init()
mixer.music.load("osnova.ogg")
mixer.music.play()
eating_sound = mixer.Sound("eat.ogg")
kick_sound = mixer.Sound("kick.ogg")






font.init()
text1 = font.SysFont("Arial", 80)
win = text1.render("YOU WIN!", True, (255, 255, 0))
try_nex = text1.render("YOU LOOSE", True, (255, 255, 0))





w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption("Tom and Jerry")
background = transform.scale(image.load("room.png"), (w, h))

# TODO Дописати екземпляри класу
player = Player("Jerry.png", 20, h-100, 5)
enemy = Enemy("Tom.png", w-100, h-200, 2)
final = GameSprite("chees.png", w-80, h-100, 0)

w1 = Wall((70, 250, 50), 10, 350, 200, 5)
w2 = Wall((250, 0, 50), 10, 480, 280, 5)
w3 = Wall((250, 250, 0),100, 200, 190, 5)
w4 = Wall((40, 200, 20), 290, 150, 10, 380)
w5 = Wall((250, 100, 0),300, 150, 260, 10)
w6 = Wall((150, 200, 100), 450, 90, 10, 390)


clock = time.Clock()
FPS = 60
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:  # ? if finish != True
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        enemy.update()
        enemy.reset()
        final.update()
        final.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
      

        if (sprite.collide_rect(player, enemy) or
                    sprite.collide_rect(player, w1) or
                    sprite.collide_rect(player, w2) or
                    sprite.collide_rect(player, w3) or
                    sprite.collide_rect(player, w4) or
                    sprite.collide_rect(player, w5) or
                    sprite.collide_rect(player, w6)
                ):
            window.blit(try_nex, (200, 200))
            finish = True
            kick_sound.play()
            display.update()
            time.delay(3000)

        if sprite.collide_rect(player, final):
            window.blit(win, (200, 200))
            finish = True
            eating_sound.play()
            display.update()
            time.delay(3000)
    else:
        player.rect.x = 20
        player.rect.y = h-100
        finish = False

    display.update()
    clock.tick(FPS)
