from const import WIN_W, WIN_H
from game_sprite import  GameSprite
from random import randint

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