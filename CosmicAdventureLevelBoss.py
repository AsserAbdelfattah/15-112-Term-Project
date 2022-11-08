from lib2to3.pytree import Base
from re import S, T, X
from this import d
import pygame

class BossEnemy:
    def __init__(self):
        self.enemySurface = pygame.image.load("EnemyBoss.png").convert_alpha()
        self.enemySurface = pygame.transform.scale(self.enemySurface, (300, 300))
        self.health = 100
        self.haveExtraLife = True
        self.dodgeCooldown = 0
        self.enemySpawnCooldown = 30
        self.invincibiltyCooldown = 60
        self.invincible = False
        self.invincibiltyTime = 0
        self.nextStage = False

class LevelBoss:
    def __init__(self):
        self.gameFont = pygame.font.Font("Game Font.ttf", 50)
        self.levelBossStart1Surface = self.gameFont.render("Boss Level", False, "White")
        self.levelBossStart1Rect = self.levelBossStart1Surface.get_rect(center = (500, 350))
        self.levelBossStart2Surface = self.gameFont.render("Start!", False, "White")
        self.levelBossStart2Rect = self.levelBossStart2Surface.get_rect(center = (500, 350))
        self.levelBossPassedSurface = self.gameFont.render("Boss Level Complete!", False, "White")
        self.levelBossPassedRect = self.levelBossPassedSurface.get_rect(center = (500, 350))
        self.boss = BossEnemy()
        self.boss_surface = self.boss.enemySurface
        self.boss_rect = self.boss_surface.get_rect(midtop = (500, -150))