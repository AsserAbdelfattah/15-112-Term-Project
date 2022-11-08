from lib2to3.pytree import Base
from re import S, T, X
from this import d
import pygame

class ArmoredEnemy:
    def __init__(self):
        self.enemySurface = pygame.image.load("Enemy3.png").convert_alpha()
        self.enemySurface = pygame.transform.scale(self.enemySurface, (100, 100))
        self.framesBetweenStep = 2
        self.health = 2

class Level3:
    def __init__(self):
        self.gameFont = pygame.font.Font("Game Font.ttf", 50)
        self.levelStart1Surface = self.gameFont.render("Level 3", False, "White")
        self.levelStart1Rect = self.levelStart1Surface.get_rect(center = (500, 350))
        self.levelStart2Surface = self.gameFont.render("Start!", False, "White")
        self.levelStart2Rect = self.levelStart2Surface.get_rect(center = (500, 350))
        self.levelPassedSurface = self.gameFont.render("Level 3 Complete", False, "White")
        self.levelPassedRect = self.levelPassedSurface.get_rect(center = (500, 350))
        self.numOfEnemies = 20
        self.enemys = []
        for i in range(self.numOfEnemies):
            self.enemys.append(ArmoredEnemy())
            self.enemys_surface = [self.enemys[i].enemySurface] * self.numOfEnemies
        self.enemys_rect = []
        for i in range(self.numOfEnemies // 2):
            for j in range(2):
                self.enemys_rect.append(self.enemys_surface[i].get_rect(topleft = (i * 100, j * 100)))
