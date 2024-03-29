import pygame, sys, os, random
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
        self.timer = 0

    def update(self):
        "Grow until a certain size, then destroy"""
        self.timer += 1
        if self.timer > 120:
            print "Bang!"
            self.timer = 0
            self.shooting = True

class Reticle(pygame.sprite.Sprite):
    """Aiming reticle that shows the mouse's position.
        Use it for hit detection too"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image, self.rect = load_image('target_reticle.bmp', -1)
        self.image, self.rect = load_image('banana.gif', -1)

    def update(self):
        "update reticle with mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midleft = pos

    def shoot(self, target):
        "returns true shooting at an enemy"
        hitbox = self.rect
        return hitbox.colliderect(target.rect)

class Heart(pygame.sprite.Sprite):
    """Basic class for lifebar hearts"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('heart.bmp', -1)
    
def main():
    
    #Initialize
    pygame.init()
    screen = pygame.display.set_mode((700, 400))
    pygame.display.set_caption('Shoot Out!')
    pygame.mouse.set_visible(0)
    
    #create the background
    #background = pygame.Surface(screen.get_size())
    #background = background.convert()
    #background.fill((250, 250, 250))
    background = pygame.image.load(os.path.join(data_dir, "forest.bmp")).convert()
    redBackground = pygame.Surface(screen.get_size())
    redBackground = redBackground.convert()
    redBackground.fill((250,0,0))
    
    #Display Background
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    clock = pygame.time.Clock()
    enemySpawn = 0
    spawnTime = 50
    flashTime = -1
    #Create enemies
    enemies = pygame.sprite.Group()
    tempEnemy = Enemy()
    tempEnemy.rect = tempEnemy.rect.move(200,200)
    enemies.add(tempEnemy)
    
    #Create reticle
    reticle = Reticle()
    
    #Create hearts
    heart1 = Heart()
    heart2 = Heart()
    heart3 = Heart()
    
    #Score
    score = 0
    
    #Move hearts into position
    heart1.rect = heart1.rect.move((540, 340))
    heart2.rect = heart2.rect.move((590, 340))
    heart3.rect = heart3.rect.move((640, 340))
    hearts = [heart1, heart2, heart3]
    allsprites = pygame.sprite.RenderPlain((reticle, hearts))
    
    going = True
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                for i in enemies.sprites():
                    if reticle.shoot(i):
                        i.kill()
                        score += 1
                        if (score % 10) == 0:
                            spawnTime -= 5
        enemySpawn += 1
        if enemySpawn >= spawnTime:
            tempEnemy = Enemy()
            tempEnemy.rect = tempEnemy.rect.move((70 + random.randrange(0, 500), 70 + random.randrange(0,200)))
            enemies.add(tempEnemy)
            enemySpawn = 0
        allsprites.update()
        enemies.update()

        for i in enemies.sprites():
            if i.shooting:
                removing = hearts.pop(0)
                removing.kill()
                i.kill()
                flashTime = 5
                if len(hearts) == 0:
                    pygame.quit()

        if flashTime >= 0:
            screen.blit(redBackground,(0,0))
            flashTime -= 1
        else:
            screen.blit(background, (0,0))
        allsprites.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()
