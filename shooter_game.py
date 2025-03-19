from pygame import *
from random import randint
from time import time as true_time
from const import *
from game_sprite import GameSprite
from player import Player
from enemy import Enemy
from bullet import Bullet


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
background = GameSprite('src/galaxy.jpg', 0,0,WIN_W,WIN_H)
rocket = Player('src/rocket.png',(WIN_W - ROCKET_W)// 2,WIN_H - ROCKET_H, ROCKET_W,ROCKET_H)

ufos = sprite.Group()
for i in range(UFO):
    enemy = Enemy('src/ufo.png',0,0,UFO_W,UFO_H)
    ufos.add(enemy)

rocks = sprite.Group()
for i in range(ROCK):
    enemy = Enemy('src/asteroid.png',0,0,ROCK_W,ROCK_W)
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
            enemy = Enemy('src/ufo.png',0,0,UFO_W,UFO_H)
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
        rocket = Player('src/rocket.png',(WIN_W - ROCKET_W)// 2,WIN_H - ROCKET_H, ROCKET_W,ROCKET_H)

        ufos = sprite.Group()
        for i in range(UFO):
            enemy = Enemy('src/ufo.png',0,0,UFO_W,UFO_H)
            ufos.add(enemy)

        rocks = sprite.Group()
        for i in range(ROCK):
            enemy = Enemy('src/asteroid.png',0,0,ROCK_W,ROCK_W)
            rocks.add(enemy)
        finish = False
    # обновить экран, чтобы отобрзить все изменения

    display.update()
    clock.tick(FPS)