import pygame
import time
import random

from pygame.locals import*
from time import sleep

xSpeed = 15

class Mario(pygame.sprite.Sprite):
	def __init__(self, Model):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.model = Model
		self.image = pygame.image.load("mario1.png")
		self.rect = self.image.get_rect()
		self.type = "mario"
		self.rect.x = 100
		self.rect.y = 100
		self.rect.w = 60
		self.rect.h = 95
		self.previousX = 0
		self.previousY = 0
		self.verticalVelocity = 0
		self.solidCount = 0
		self.spriteValue = 0
		self.imageArray = [pygame.image.load("mario1.png"), pygame.image.load("mario2.png"), pygame.image.load("mario3.png"), pygame.image.load("mario4.png"), pygame.image.load("mario5.png")]

	def update(self):
		# "Adds gravity to mario"
		self.verticalVelocity += 5
		self.rect.y += self.verticalVelocity
		self.solidCount += 1

		if self.rect.y > 375:
			self.verticalVelocity = 0
			self.rect.y = 375
			self.solidCount = 0
		
		# Unable to use pygame collision because x, y values are never updated
		for sprite in self.model.sprites:
			if (sprite.type == "brick" or sprite.type == "coinBlock") and self.checkCollision(self, sprite):
				self.setBarrier(sprite)

	def setBarrier(self, sprite):
		# Left of Brick Barrier
		if ((self.rect.x + self.model.cameraPosition + self.rect.w >= sprite.rect.x) and (self.model.previousCameraPostion + self.previousX + self.rect.w < sprite.rect.x)):
			self.model.cameraPosition -= xSpeed
		
		# Right of Brick Barrier
		if ((self.model.cameraPosition + self.rect.x <= sprite.rect.x + sprite.rect.w) and (self.previousX + self.model.previousCameraPostion > sprite.rect.x + sprite.rect.w)):
			self.model.cameraPosition += xSpeed
		
		# Top of Brick Barrier
		if ((self.rect.y + self.rect.h >= sprite.rect.y) and (self.previousY + self.rect.h <= sprite.rect.y)):
			self.verticalVelocity = 0
			self.rect.y = sprite.rect.y - self.rect.h - 3
			self.solidCount = 0
		
		# Bottom of Brick Barrier
		if ((self.rect.y <= sprite.rect.y + sprite.rect.h) and (self.previousY > sprite.rect.y + sprite.rect.h)):
			self.rect.y = sprite.rect.y + sprite.rect.h + 1
			self.verticalVelocity = 0
			if (sprite.type == "coinBlock"):
				sprite.generate_coin()
			
		

	def checkCollision(self, sprite1, sprite2):
		# Check left of brick
		if (sprite1.rect.x + self.model.cameraPosition + sprite1.rect.w < sprite2.rect.x):
			print("left")
			return False
		# Check right of brick
		elif (sprite1.rect.x + self.model.cameraPosition > sprite2.rect.x + sprite2.rect.w):
			print("right")
			return False
		# Check top of the brick
		elif (sprite1.rect.y + sprite1.rect.h < sprite2.rect.y):
			print("top")
			return False
		# Check bottom of brick
		elif (sprite1.rect.y > sprite2.rect.y + sprite2.rect.h):
			return False
		else:
			print("Inside")
			return True


	def jump(self):
		if self.solidCount < 4:
			self.verticalVelocity -= 15

	def draw(self, screen):
		screen.blit(self.imageArray[self.spriteValue], (self.rect.x, self.rect.y))

	def updateImage(self):
		self.spriteValue += 1
		if self.spriteValue == 5:
			self.spriteValue = 0

	def setPrevious(self):
		self.previousX = self.rect.x
		self.previousY = self.rect.y
		self.model.previousCameraPos = self.model.cameraPosition

class Brick(pygame.sprite.Sprite):
	def __init__(self, xx, yy, ww, hh, Model):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.model = Model
		self.image = pygame.image.load("brick.png")
		self.image = pygame.transform.scale(self.image,(ww, hh))
		self.rect = self.image.get_rect()
		self.rect.x = xx
		self.rect.y = yy
		self.rect.w = ww
		self.rect.h = hh
		self.type = "brick"

	def draw(self, screen):
		screen.blit(self.image, (self.rect.x - self.model.cameraPosition, self.rect.y))

class CoinBlock(pygame.sprite.Sprite):
	def __init__(self, xx, yy, ww, hh, Model):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.model = Model
		self.image = pygame.image.load("coinBlockFull.png")
		self.image = pygame.transform.scale(self.image,(ww, hh))
		self.rect = self.image.get_rect()
		self.rect.x = xx
		self.rect.y = yy
		self.rect.w = ww
		self.rect.h = hh
		self.type = "coinBlock"
		self.coinBlockValue = 0
		self.coinBlockImageValue = 0
		self.coinTimer = 0
		self.coinHit = False

	def draw(self, screen):
		screen.blit(self.image, (self.rect.x - self.model.cameraPosition, self.rect.y))

	def update(self):
		if self.coinBlockValue == 5:
			self.image = load("coinBlockFull.png")
			self.image = pygame.transform.scale(self.image, (self.rect.x , self.rect.y))

	def generateCoin(self):
		if (not self.coinHit and self.coinTimer < 1 and self.coinBlockValue < 5):
			self.coinHit = not self.coinHit
			self.coinBlockValue += 1
			coin = Coin()
			self.model.sprites.add(coin)

class Coin(pygame.sprite.Sprite):
	def __init__(self, xx, yy, ww, hh, Model):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.model = Model
		self.image = pygame.image.load("coin.png")
		self.image = pygame.transform.scale(self.image,(ww, hh))
		self.rect = self.image.get_rect()
		self.rect.x = xx
		self.rect.y = yy
		self.rect.w = ww
		self.rect.h = hh
		self.vVel = -20
		self.hVel = random.randint(0, 18)
		self.type = "coin"

		self.multiplyer = random.randint(0,1)
		if(self.multiplyer < .5):
			self.multiplyer = -1
		else:
			self.multiplyer = 1
		self.hVel *= self.multiplyer

	def draw(self, screen):
		screen.blit(self.image, (self.rect.x - self.model.cameraPosition, self.rect.y))

	def update(self):
		self.vVel += 3.14159
		self.rect.y += self.vVel
		self.rect.x += self.hVel

		if (self.rect.y > 700):
			self.model.sprites.remove(self)



class Model():
	def __init__(self):
		self.sprites = pygame.sprite.Group()
		self.mario = Mario(self)
		self.sprites.add(self.mario)

		self.cameraPosition = 0
		self.previousCameraPostion = 0
		
		self.destX1 = 0
		self.destX2 = 0
		self.destY1 = 0
		self.destY2 = 0

	def update(self):
		self.sprites.update()

	def setDestination1(self, pos):
		self.destX1 = pos[0]
		self.destY1 = pos[1]

	def setDestination2(self, pos):
		self.destX2 = pos[0]
		self.destY2 = pos[1]
		self.determineBoundries()

	def determineBoundries(self):
		xx = min(self.destX1, self.destX2) + self.cameraPosition
		yy = min(self.destY1, self.destY2)
		ww = abs(self.destX1 - self.destX2)
		hh = abs(self.destY1 - self.destY2)
		brick = Brick(xx, yy, ww, hh, self)
		self.sprites.add(brick)

	def addCoinBlock(self, pos):
		coinBlock = CoinBlock(pos[0], pos[1], 50, 50, self)
		self.sprites.add(coinBlock)

class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.background = pygame.image.load("background.png")
		self.background = pygame.transform.scale(self.background,(800, 600))
		self.model = model

	def update(self):    
		self.screen.fill([0,200,100])

		for x in range(-10, 10):
			self.screen.blit(self.background, (800 * x - self.model.cameraPosition/2, 0))

		spritesList = self.model.sprites.sprites()
		for sprite in spritesList:
			sprite.draw(self.screen)
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		self.model.mario.setPrevious()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				self.model.setDestination1(pygame.mouse.get_pos())
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				self.model.setDestination2(pygame.mouse.get_pos())
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				self.model.addCoinBlock(pygame.mouse.get_pos())
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.cameraPosition -= xSpeed
			self.model.mario.updateImage()
		if keys[K_RIGHT]:
			self.model.cameraPosition += xSpeed
			self.model.mario.updateImage()
		if keys[K_SPACE]:
			self.model.mario.jump()

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")