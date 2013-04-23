import pygame, sys, os
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Enemy(pygame.sprite.Sprite):
    """Enemy who shoots at you if they get too close"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('enemy.bmp', -1)
        self.growthRate = 5
        self.shooting = False

    def update(self):
        "Grow until a certain size, then destroy"""
        self.image = pygame.transform.scale(self.image, (self.rect.width + self.growthRate, self.rect.height + self.growthRate))
        if self.rect.width >= 100:
            self.shooting = True

class Reticle(pygame.sprite.Sprite):
    """Aiming reticle that shows the mouse's position.
        Use it for hit detection too"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('target_reticle.bmp', -1)
        self.shooting = False

    def update(self):
        "update reticle with mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

    def shoot(self, target):
        "returns true shooting at an enemy"
        if not self.shooting:
            self.shooting = True
            hitbox = self.rect
            return hitbox.colliderect(target.rect)

def main():
    
    #Initialize
    pygame.init()
    screen = pygame.display.set_mode((700, 400))
    pygame.display.set_caption('Shoot Out!')
    pygame.mouse.set_visible(0)
    
    #create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    
    #Display Background
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    bronemy = Enemy()
    bronemy.rect = bronemy.rect.move((300,300))
    enemies = pygame.sprite.Group()
    #Create enemies
    for i in range(4):
        enemies.add(Enemy())
    enemyList = enemies.sprites()
    enemyList[0].rect = enemyList[0].rect.move((300,300))
    enemyList[1].rect = enemyList[1].rect.move((100,50))
    enemyList[2].rect = enemyList[2].rect.move((400,40))
    enemyList[3].rect = enemyList[3].rect.move((50,50))
    reticle = Reticle()
    allsprites = pygame.sprite.RenderPlain((reticle, bronemy))
    
    going = True
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                print bronemy
                if reticle.shoot(bronemy):
                    bronemy.kill()
                for i in enemies.sprites():
                    print i
                    if reticle.shoot(i):
                        i.kill()
        allsprites.update()
        enemies.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()
