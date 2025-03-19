from pygame import *
from const import WIN_W, HP
from bullet import Bullet
from game_sprite import  GameSprite

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