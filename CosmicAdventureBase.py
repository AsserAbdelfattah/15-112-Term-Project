from re import S, T, X
from sys import exit
import sys
from telnetlib import GA
from this import d
from time import time
from tkinter import Y, font
import pygame
import CosmicAdventureLevel1
import CosmicAdventureLevel2
import CosmicAdventureLevel3
import CosmicAdventureLevelBoss
import random

class Laser:
        def __init__(self, rect):
            self.rect = rect

class Button():
    def __init__(self, screen, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.buttonFont = pygame.font.Font("Game Font.ttf", 30)

        self.fillColors = {'normal': '#7d0549', 'hover': '#aa09db', 'pressed': '#7d0549'}
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = self.buttonFont.render(buttonText, True, "Blue")

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)

class Game:
    def __init__(self):
        gameMusic = pygame.mixer.Sound("C:\\Users\\asser\F-777 - Sonic Blaster.mp3")
        gameMusic.set_volume(0)
        gameMusic.play(loops=-1)
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Cosmic Adventure")
        self.clock = pygame.time.Clock()
        self.gameFont = pygame.font.Font("Game Font.ttf", 50)
        self.scoreFont = pygame.font.Font("Game Font.ttf", 20)
        self.DefaultImageSize = (100, 100)
        self.spaceSurface = pygame.image.load("Space Background.jpg").convert()
        self.spaceSurface = pygame.transform.scale(self.spaceSurface, (1000, 700))
        self.gameOverSurface = self.gameFont.render("Game over", False, "Red")
        self.gameOverRect = self.gameOverSurface.get_rect(center = (500, 250))
        self.shipSurface = pygame.image.load("Ship.png").convert_alpha()
        self.shipSurface = pygame.transform.scale(self.shipSurface, (80, 80))
        self.shipRect = self.shipSurface.get_rect(midbottom = (500, 700))
        self.scoreSurface = self.scoreFont.render("Time: "+str(pygame.time.get_ticks()/1000), False, "Green")
        self.scoreRect = self.scoreSurface.get_rect(topleft = (0, 0))
        self.nameSurface = self.gameFont.render("Cosmic Adventure", False, (111, 219, 9))
        self.nameRect = self.nameSurface.get_rect(center = (500, 350))
        self.damagePowerUpSurface = pygame.image.load("Damage PowerUp.png").convert_alpha()
        self.damagePowerUpSurface = pygame.transform.scale(self.damagePowerUpSurface, (50, 50))
        self.damagePowerUpRect = self.damagePowerUpSurface.get_rect(center = (500, -25))
        self.buttons = []
        self.buttons.append(Button(self.screen, 375, 600, 250, 50, 'Exit', self.exit))
        self.buttons.append(Button(self.screen, 375, 450, 250, 50, 'Play', self.start))
        

        self.laserRects = []
        self.level1var = CosmicAdventureLevel1.Level1()
        self.level1Done = False
        self.level2var = CosmicAdventureLevel2.Level2()
        self.level2Done = False
        self.level3var = CosmicAdventureLevel3.Level3()
        self.level3Done = False
        self.levelBossvar = CosmicAdventureLevelBoss.LevelBoss()
        self.levelBossDone = False
        self.powerUpActive = False
        self.firstGame = True
        self.gameActive = False
        self.defualtCooldown = 0.25
        self.cooldownTimer = self.defualtCooldown
        self.animationDone = False
        self.damage = 1

        self.gameLoop()

    def start(self):
        self.firstGame = False
        self.gameActive = True

    def menu(self):
        pygame.quit()
        pygame.init()
        self.nextGame = Game()
        

    def exit(self):
        exit()
    
    def gameLoop(self):    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if self.gameActive:
                self.screen.blit(self.spaceSurface, (0, 0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.shipRect.left += 3
                    elif event.key == pygame.K_LEFT:
                        self.shipRect.left -= 3
                    elif event.key == pygame.K_LCTRL and self.cooldownTimer >= self.defualtCooldown:
                        self.laserRects.append(Laser(pygame.Rect(self.shipRect.centerx - 1.5, self.shipRect.top - 20, 5, 20)))
                        pygame.draw.rect(self.screen, "Red", self.laserRects[-1])
                        self.cooldownTimer = 0
                if self.shipRect.left <= 0:
                    self.shipRect.left += 3
                elif self.shipRect.right >= 1000:
                    self.shipRect.left -= 3
                self.screen.blit(self.shipSurface, self.shipRect)
                for laser in self.laserRects:
                    laser.rect.y -= 20
                    pygame.draw.rect(self.screen, "Red", laser)
                
                self.scoreSurface = self.scoreFont.render("Time: "+str((pygame.time.get_ticks() - self.startTime)/1000), False, "Green")
                self.screen.blit(self.scoreSurface, self.scoreRect)
                if self.levelBossDone:
                    self.endTime = (pygame.time.get_ticks() - self.startTime) / 1000
                    self.gameActive = False
                    #self.screen.blit(self.gameWinSurface, self.gameWinRect)
                elif self.level3Done:
                    self.levelBoss()
                elif self.level2Done:
                    self.level3()
                elif self.level1Done:
                    self.level2()
                else:
                    self.level1()
            else:
                if self.levelBossDone:
                    self.gameWinSurface = self.gameFont.render("You took " + str(self.endTime) + " seconds", False, (66, 135, 245))
                    self.gameWinRect = self.scoreSurface.get_rect(center = (200, 350))
                    self.screen.blit(self.gameWinSurface, self.gameWinRect)
                    self.buttons.pop()
                    self.buttons.append(Button(self.screen, 375, 450, 250, 50, 'Home Screen', self.menu))
                    for button in self.buttons:
                        button.process()

                elif self.firstGame:
                    self.startTime = pygame.time.get_ticks()
                    self.animationTickNum = pygame.time.get_ticks()
                    self.nextLevelTickNum = pygame.time.get_ticks()
                    self.screen.blit(self.spaceSurface, (0, 0))
                    for button in self.buttons:
                        button.process()
                    self.screen.blit(self.nameSurface, self.nameRect)

                else:
                    self.screen.blit(self.gameOverSurface, self.gameOverRect)
                    self.buttons.pop()
                    self.buttons.append(Button(self.screen, 375, 450, 250, 50, 'Home Screen', self.menu))
                    for button in self.buttons:
                        button.process()

                        

            pygame.display.update()
            self.cooldownTimer += 1/60
            self.clock.tick(60)

    def level1(self):
        if not self.animationDone:
            self.startAnimation(self.level1var.levelStart1Surface, self.level1var.levelStart1Rect, 
                            self.level1var.levelStart2Surface, self.level1var.levelStart2Rect)
            self.powerUpTimer = pygame.time.get_ticks()
            self.powerUpDuration = 1000000
        if self.animationDone:
            self.powerUp()
            if not self.level1Done:
                for k in range(self.level1var.numOfEnemies):
                    if self.level1var.enemys_rect[k].bottom == self.shipRect.top:
                        self.gameActive = False
                if pygame.time.get_ticks() % (self.level1var.enemy.framesBetweenStep + 1) == 1:
                    for i in range(self.level1var.numOfEnemies):
                        if self.level1var.enemys_rect[i].y != 2000:
                            self.level1var.enemys_rect[i].y += 1
                for i in range(self.level1var.numOfEnemies):
                    self.screen.blit(self.level1var.enemys_surface[i], self.level1var.enemys_rect[i])

                for j in range(self.level1var.numOfEnemies):
                    for i in self.laserRects:
                        if i.rect.colliderect(self.level1var.enemys_rect[j]):
                            if self.level1var.enemys[j].health <= 0:
                                i.rect.x = 2000
                                i.rect.y = 2000
                                self.level1var.enemys_rect[j].x = 2000
                                self.level1var.enemys_rect[j].y = 2000
                                self.laserRects.remove(i)
                            else:
                                self.level1var.enemys[j].health -= self.damage
            if self.level1Done:
                 for k in range(self.level1var.numOfEnemies):
                    if self.level1var.enemys_rect[k].y != 2000:
                        self.bossMinionsKilled = True
            else:
                for k in range(self.level1var.numOfEnemies):
                        if self.level1var.enemys_rect[k].y != 2000:
                            break
                else:
                    if not self.level1Done:
                        self.screen.blit(self.level1var.levelPassedSurface, self.level1var.levelPassedRect)
                        if self.nextLevelTickNum == self.animationTickNum:
                            self.nextLevelTickNum = pygame.time.get_ticks()
                        if self.nextLevelTickNum + 480 * 9 <= pygame.time.get_ticks():
                            self.nextLevelTickNum = pygame.time.get_ticks()
                            self.animationTickNum = pygame.time.get_ticks()
                            self.level1Done = True
                            self.animationDone = False
            
    def level2(self):
        if not self.animationDone:
            self.startAnimation(self.level2var.levelStart1Surface, self.level2var.levelStart1Rect, 
                            self.level2var.levelStart2Surface, self.level2var.levelStart2Rect)
            self.powerUpTimer = pygame.time.get_ticks()
            self.powerUpDuration = 1000000
        if self.animationDone:
            self.powerUp()
            if not self.level2Done:
                for k in range(self.level2var.numOfEnemies):
                    if self.level2var.enemys_rect[k].bottom == self.shipRect.top:
                        self.gameActive = False
                if pygame.time.get_ticks() % (self.level2var.enemy.framesBetweenStep + 1) == 1:
                    for i in range(self.level2var.numOfEnemies):
                        if self.level2var.enemys_rect[i].y != 2000:
                            self.level2var.enemys_rect[i].y += 1
                for i in range(self.level2var.numOfEnemies):
                    self.screen.blit(self.level2var.enemys_surface[i], self.level2var.enemys_rect[i])

                for j in range(self.level2var.numOfEnemies):
                    for i in self.laserRects:
                        if i.rect.colliderect(self.level2var.enemys_rect[j]):
                            if self.level2var.enemys[j].health <= 0:
                                i.rect.x = 2000
                                i.rect.y = 2000
                                self.level2var.enemys_rect[j].x = 2000
                                self.level2var.enemys_rect[j].y = 2000
                                self.laserRects.remove(i)
                            else:
                                self.level2var.enemys[j].health -= self.damage
                if self.level2Done:
                    for k in range(self.level2var.numOfEnemies):
                        if self.level2var.enemys_rect[k].y != 2000:
                            self.bossMinionsKilled = True
                else:
                    for k in range(self.level2var.numOfEnemies):
                            if self.level2var.enemys_rect[k].y != 2000:
                                break
                    else:
                        if not self.level2Done:
                            self.screen.blit(self.level2var.levelPassedSurface, self.level2var.levelPassedRect)
                            if self.nextLevelTickNum == self.animationTickNum:
                                self.nextLevelTickNum = pygame.time.get_ticks()
                            if self.nextLevelTickNum + 480 * 9 <= pygame.time.get_ticks():
                                self.nextLevelTickNum = pygame.time.get_ticks()
                                self.animationTickNum = pygame.time.get_ticks()
                                self.level2Done = True
                                self.animationDone = False

    def level3(self):
        if not self.animationDone:
            self.startAnimation(self.level3var.levelStart1Surface, self.level3var.levelStart1Rect, 
                            self.level3var.levelStart2Surface, self.level3var.levelStart2Rect)
            self.powerUpTimer = pygame.time.get_ticks()
            self.powerUpDuration = 1000000
        if self.animationDone:
            self.powerUp()
            if not self.level3Done:
                for k in range(self.level3var.numOfEnemies):
                    if self.level3var.enemys_rect[k].bottom == self.shipRect.top:
                        self.gameActive = False
                if pygame.time.get_ticks() % (self.level3var.enemys[0].framesBetweenStep + 1) == 1:
                    for i in range(self.level3var.numOfEnemies):
                        if self.level3var.enemys_rect[i].y != 2000:
                            self.level3var.enemys_rect[i].y += 1
                for i in range(self.level3var.numOfEnemies):
                    self.screen.blit(self.level3var.enemys_surface[i], self.level3var.enemys_rect[i])

                for j in range(self.level3var.numOfEnemies):
                    for i in self.laserRects:
                        if i.rect.colliderect(self.level3var.enemys_rect[j]):
                            self.level3var.enemys[j].health -= self.damage
                            i.rect.x = 2000
                            i.rect.y = 2000
                            self.laserRects.remove(i)
                            if self.level3var.enemys[j].health <= 0:
                                self.level3var.enemys_rect[j].x = 2000
                                self.level3var.enemys_rect[j].y = 2000
                if self.level3Done:
                    for k in range(self.level3var.numOfEnemies):
                        if self.level3var.enemys_rect[k].y != 2000:
                            self.bossMinionsKilled = True
                else:
                    for k in range(self.level3var.numOfEnemies):
                            if self.level3var.enemys_rect[k].y != 2000:
                                break
                    else:
                        if not self.level3Done:
                            self.screen.blit(self.level3var.levelPassedSurface, self.level3var.levelPassedRect)
                            if self.nextLevelTickNum == self.animationTickNum:
                                self.nextLevelTickNum = pygame.time.get_ticks()
                            if self.nextLevelTickNum + 480 * 9 <= pygame.time.get_ticks():
                                self.nextLevelTickNum = pygame.time.get_ticks()
                                self.animationTickNum = pygame.time.get_ticks()
                                self.level3Done = True
                                self.animationDone = False

    def levelBoss(self):
        if not self.animationDone:
            self.startAnimation(self.levelBossvar.levelBossStart1Surface, self.levelBossvar.levelBossStart1Rect, 
                                self.levelBossvar.levelBossStart2Surface, self.levelBossvar.levelBossStart2Rect)
            self.powerUpTimer = pygame.time.get_ticks()
            self.powerUpDuration = 1000000
            self.timeStuck = 0
            self.attackCooldown = pygame.time.get_ticks()
            self.attemptToKill = False
            self.moveUp = False
        if self.animationDone:
            self.powerUp()
            self.screen.blit(self.levelBossvar.boss_surface, self.levelBossvar.boss_rect)
            if not self.attemptToKill:
                if abs(self.shipRect.centerx - self.levelBossvar.boss_rect.centerx) <= 160:
                    if self.shipRect.centerx - self.levelBossvar.boss_rect.centerx < 160 and self.shipRect.centerx - self.levelBossvar.boss_rect.centerx > 0:
                        self.levelBossvar.boss_rect.x -= 2
                        if self.levelBossvar.boss_rect.x <= 0:
                            self.levelBossvar.boss_rect.x += 2
                            if self.timeStuck == 0:
                                self.timeStuck = pygame.time.get_ticks()
                            elif self.timeStuck + 1000 <= pygame.time.get_ticks():
                                self.levelBossvar.boss_rect.center = (500, 0)
                                self.timeStuck = 0
                    elif self.shipRect.centerx - self.levelBossvar.boss_rect.centerx >= -160:
                            self.levelBossvar.boss_rect.x += 2
                            if self.levelBossvar.boss_rect.x >= 700:
                                self.levelBossvar.boss_rect.x -= 2
                                if self.timeStuck == 0:
                                    self.timeStuck = pygame.time.get_ticks()
                                elif self.timeStuck + 1000 <= pygame.time.get_ticks():
                                    self.levelBossvar.boss_rect.center = (500, 0)
                                    self.timeStuck = 0
            else:
                if self.moveUp or self.levelBossvar.boss_rect.y >= 550:
                    self.levelBossvar.boss_rect.x += self.movePerFrame[0]
                    self.levelBossvar.boss_rect.y += self.movePerFrame[1]
                    if self.levelBossvar.boss_rect.y <= -150:
                        self.moveUp = False
                        self.attemptToKill = False
                        self.attackCooldown = pygame.time.get_ticks()
                else:
                    self.levelBossvar.boss_rect.x -= self.movePerFrame[0]
                    self.levelBossvar.boss_rect.y -= self.movePerFrame[1]
                    if self.levelBossvar.boss_rect.y >= 550:
                        self.moveUp = True
                    

            
            if self.shipRect.colliderect(self.levelBossvar.boss_rect):
                self.gameActive = False


            for i in self.laserRects:
                if i.rect.colliderect(self.levelBossvar.boss_rect):
                    self.levelBossvar.boss.health -= self.damage
                    i.rect.x = 2000
                    i.rect.y = 2000
                    self.laserRects.remove(i)
            if self.levelBossvar.boss.health <= 0:
                self.levelBossvar.boss_rect.x = 3000
                self.levelBossvar.boss_rect.y = 3000
                self.screen.blit(self.levelBossvar.levelBossPassedSurface, self.levelBossvar.levelBossPassedRect)
                if self.nextLevelTickNum == self.animationTickNum:
                    self.nextLevelTickNum = pygame.time.get_ticks()
                if self.nextLevelTickNum + 480 * 9 <= pygame.time.get_ticks():
                    self.nextLevelTickNum = pygame.time.get_ticks()
                    self.animationTickNum = pygame.time.get_ticks()
                    self.levelBossDone = True
                    self.endTime = pygame.time.get_ticks()

            if self.attackCooldown + 7000 <= pygame.time.get_ticks():
                self.differenceToMovex = self.levelBossvar.boss_rect.center[0] - self.shipRect.center[0]
                self.differenceToMovey = self.levelBossvar.boss_rect.center[1] - self.shipRect.bottom
                self.movePerFrame = (self.differenceToMovex / 90, self.differenceToMovey / 90)
                self.attackCooldown = pygame.time.get_ticks()
                self.attemptToKill = True
            
    def powerUp(self):
        if self.powerUpTimer + 7000 <= pygame.time.get_ticks():
            self.damagePowerUpRect.y += 2
            if self.shipRect.colliderect(self.damagePowerUpRect):
                self.powerUpActive = True
                self.damage = 2
                self.damagePowerUpRect.centery = -25
                if self.powerUpDuration == 1000000:
                    self.powerUpDuration = pygame.time.get_ticks()
            elif self.powerUpDuration + 3000 <= pygame.time.get_ticks():
                self.powerUpActive = False
                self.damagePowerUpRect.y -= 2
                self.damage = 1
                self.powerUpDuration = 1000000
                self.powerUpTimer = pygame.time.get_ticks()
            elif self.damagePowerUpRect.centery == 725:
                self.damagePowerUpRect.centery = -25
                self.powerUpNum = random.randint(1, 2)
                self.powerUpTimer = pygame.time.get_ticks()
            elif self.powerUpActive:
                self.damagePowerUpRect.y -= 2
                self.damage = 2
                self.damagePowerUpRect.centery = -25

        self.screen.blit(self.damagePowerUpSurface, self.damagePowerUpRect)

    def startAnimation(self, start1Surface, start1Rect, start2Surface, start2Rect):
        if pygame.time.get_ticks() <= self.animationTickNum + 480 * 3:
            self.screen.blit(start1Surface, start1Rect)
        elif pygame.time.get_ticks() < self.animationTickNum + 960 * 3:
            self.screen.blit(start2Surface, start2Rect)
        elif pygame.time.get_ticks() >= self.animationTickNum + 960 * 3:
            self.animationDone = True

pygame.init()
game = Game()
