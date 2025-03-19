from pygame import *

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