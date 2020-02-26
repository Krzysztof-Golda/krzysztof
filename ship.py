import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Inicjalizacja statku i jego położenia"""

        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # Obraz statku
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # satek pojawia się u dołu ekranu
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Punkt środkowy jest zachowany jako liczba zmiennoprzecinkowa
        self.center = float(self.rect.centerx)

        #opcje poruszania statkiem
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Uaktualnienie położenia statku z opcji wskazującej na jego ruch"""
        #Uaktualnienie punktu środkowego statku
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #Uaktualnienie obiektu rect na podstawie wartości self.center
        self.rect.centerx = self.center #5

    def blitme(self):
        """Wyświetlanie statku w akutalnym położeniu"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Umieszczenie statku na środku przy dolnej krawędzi"""
        self.center = self.screen_rect.centerx
