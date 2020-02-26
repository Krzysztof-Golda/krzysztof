import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Klasa zarządzająca pociskami statku"""
    def __init__(self, ai_settings, screen, ship):
        """Utworzenie obiektu w aktualnym położeniu statku"""
        super(Bullet, self).__init__()
        self.screen = screen

        #Tworzenie pocisku w (0,0) i zdefiniowanie dla niego odpowiedniego położenia
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Położenie pocisku jest zdefiniowane jako wartość zmiennoprzecinkowa
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Poruszanie pocisku na ekranie"""
        #Uaktualnione położenie pocisku
        self.y -= self.speed_factor

        #Uaktualnienie prostokąta pocisku
        self.rect.y = self.y

    def draw_bullet(self):
        """Wyświetlanie pocisku na ekranie"""
        pygame.draw.rect(self.screen, self.color, self.rect)