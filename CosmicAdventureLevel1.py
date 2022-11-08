from lib2to3.pytree import Base
from re import S, T, X
from this import d
import pygame

class BasicEnemy:
    def __init__(self):
        self.enemySurface = pygame.image.load("Enemy.png").convert_alpha()
        self.enemySurface = pygame.transform.scale(self.enemySurface, (100, 100))
        self.framesBetweenStep = 2
        self.health = 1

class Level1:
    def __init__(self):
        self.gameFont = pygame.font.Font("Game Font.ttf", 50)
        self.levelStart1Surface = self.gameFont.render("Level 1", False, "White")
        self.levelStart1Rect = self.levelStart1Surface.get_rect(center = (500, 350))
        self.levelStart2Surface = self.gameFont.render("Start!", False, "White")
        self.levelStart2Rect = self.levelStart2Surface.get_rect(center = (500, 350))
        self.levelPassedSurface = self.gameFont.render("Level 1 Complete", False, "White")
        self.levelPassedRect = self.levelPassedSurface.get_rect(center = (500, 350))
        self.enemy = BasicEnemy()
        self.numOfEnemies = 20
        self.enemys = [self.enemy] * self.numOfEnemies
        self.enemys_surface = [self.enemy.enemySurface] * self.numOfEnemies
        self.enemys_rect = []
        for i in range(self.numOfEnemies // 2):
            for j in range(2):
                self.enemys_rect.append(self.enemys_surface[i].get_rect(topleft = (i * 100, j * 100)))
