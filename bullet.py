from game_sprite import  GameSprite

class Bullet(GameSprite):
    def __init__(self,x,y,width = 5,height = 10,speed = 3,img = 'src/bullet.png'):
        super().__init__(img,x,y,width,height,)
        self.speed = speed
        
    def update(self):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.speed