from pygame import *
from random import randint
from time import time as true_time
# вынесем размер окна в константы для удобства
# W - width, ширина
# H - height, высота
WIN_W = 700
WIN_H = 500
FPS = 60
RED = (250,0,0)
WHITE = (250,250,250)
YELLOW = (255,245,22)
ROCKET_W = 35
ROCKET_H = 65
UFO_W = 50
UFO_H = 30
ROCK_W = 50

WIN_COUNT = 10
UFO = 5
HP = 3
ROCK = 3
RECHARGE_TIME = 2
SHOTS = 6
class GameSprite(sprite.Sprite):
    def __init__(self,img,x,y,width,height):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            # здесь - размеры картинки
            (width,height)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self,window):
        window.blit(self.image,(self.rect.x,self.rect.y))
# создание окна размером 700 на 500


class Player(GameSprite):
    def __init__(self,img,x,y,width,height,speed = 3, hp = HP):
        super().__init__(img,x,y,width,height,)
        self.speed = speed
        self.count = 0
        self.missed = 0
        self.bullets = sprite.Group()
        self.hp = hp
        self.is_recharge = False
        self.shots = 0
        
    def update(self):
        keys = key.get_pressed()
        if self.rect.x > 0 and keys[K_a]:
            self.rect.x -= self.speed
        if self.rect.x < WIN_W - self.rect.width and keys[K_d]:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)
        self.shots += 1


class Enemy(GameSprite):
    def __init__(self,img,x,y,width,height,):
        super().__init__(img,x,y,width,height,)
        self.speed = randint(1,2)
        self.rect.y = randint(10,50)
        self.rect.x = randint(0,WIN_W-self.rect.width)
        
    def update(self, player, skippable = False):
        if self.rect.y > WIN_H:
            self.rect.y = randint(10,50)
            self.rect.x = randint(0,WIN_W-self.rect.width)
            if not skippable:
                player.missed += 1
        self.rect.y += self.speed


class Bullet(GameSprite):
    def __init__(self,x,y,width = 5,height = 10,speed = 3,img = 'bullet.png'):
        super().__init__(img,x,y,width,height,)
        self.speed = speed
        
    def update(self):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed

window = display.set_mode((WIN_W, WIN_H))
display.set_caption("Лабиринт")

clock = time.Clock()
mixer.init()
#mixer.music.load('MY FIRST STORY×HYDE — 夢幻 (www.lightaudio.ru).mp3')
#mixer.music.play()

font.init()

my_font = font.SysFont('arial',30)
count_txt = my_font.render('счёт', True,WHITE)
count = my_font.render('0',True,WHITE)
missed_txt = my_font.render('пропущено',True,WHITE)
missed = my_font.render('0',True,WHITE)
hp_txt = my_font.render('жизни', True,WHITE)
hp = my_font.render('0',True,WHITE)
recharge_txt = my_font.render('перезарядка', True,YELLOW)

title_font = font.SysFont('arial',70)
win = title_font.render('вы выиграли', True, RED)
lost = title_font.render('вы проиграли', True, WHITE)

# задать картинку фона такого же размера, как размер окна
background = GameSprite('galaxy.jpg', 0,0,WIN_W,WIN_H)
rocket = Player('rocket.png',(WIN_W - ROCKET_W)// 2,WIN_H - ROCKET_H, ROCKET_W,ROCKET_H)

ufos = sprite.Group()
for i in range(UFO):
    enemy = Enemy('ufo.png',0,0,UFO_W,UFO_H)
    ufos.add(enemy)

rocks = sprite.Group()
for i in range(ROCK):
    enemy = Enemy('asteroid.png',0,0,ROCK_W,ROCK_W)
    rocks.add(enemy)

start_time = None
game = True
finish = False
while game:
    for e in event.get():
        # выйти, если нажат "крестик"
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if rocket.shots < SHOTS:
                    rocket.fire()
                else:
                    rocket.is_recharge = True
                    start_time = true_time()
    if not finish:
        if rocket.is_recharge:
            cur_time = true_time()
            if cur_time - start_time < RECHARGE_TIME:
                window.blit(recharge_txt,(WIN_W//2,WIN_H-50))
                display.update()
            else:
                rocket.shots = 0
                rocket.is_recharge = False
        # отобразить картинку фона
        background.draw(window)
        window.blit(count_txt,(10,0))
        window.blit(missed_txt,(10,40))
        window.blit(hp_txt,(10,80))

        count = my_font.render(str(rocket.count),True,WHITE)
        window.blit(count,(70,0))
        missed = my_font.render(str(rocket.missed),True,WHITE)
        window.blit(missed,(150,40))
        hp = my_font.render(str(rocket.hp),True,WHITE)
        window.blit(hp,(90,80))

        rocket.draw(window)
        rocket.update()
        ufos.draw(window)
        ufos.update(rocket)
        rocket.bullets.draw(window)
        rocket.bullets.update()
        rocks.draw(window)
        rocks.update(rocket,True)
        
        ufo_vs_bullet  = sprite.groupcollide(
            ufos,rocket.bullets,True,True
        )
        for collide in ufo_vs_bullet:
            rocket.count += 1
            enemy = Enemy('ufo.png',0,0,UFO_W,UFO_H)
            ufos.add(enemy)

        ufos_collide = sprite.spritecollide(
            rocket,ufos,True
        )
        rocks_collide = sprite.spritecollide(
            rocket,rocks,True
        )

        if ufos_collide or rocks_collide:
            if rocket.hp > 0 :
                rocket.hp -= 1
            else:
                window.blit(lost,(200,200))
                finish = True
                display.update()

        if rocket.count > WIN_COUNT:
            window.blit(win,(200,200))
            finish = True
            display.update()

        if rocket.missed > UFO:
            window.blit(lost,(200,200))
            finish = True
            display.update()
    else:
        for b in rocket.bullets:
            b.kill()
        for u in ufos:
            u.kill()
        for r in rocks:
            r.kill()
        time.delay(3000)
        rocket = Player('rocket.png',(WIN_W - ROCKET_W)// 2,WIN_H - ROCKET_H, ROCKET_W,ROCKET_H)

        ufos = sprite.Group()
        for i in range(UFO):
            enemy = Enemy('ufo.png',0,0,UFO_W,UFO_H)
            ufos.add(enemy)

        rocks = sprite.Group()
        for i in range(ROCK):
            enemy = Enemy('asteroid.png',0,0,ROCK_W,ROCK_W)
            rocks.add(enemy)
        finish = False
    # обновить экран, чтобы отобрзить все изменения

    display.update()
    clock.tick(FPS)