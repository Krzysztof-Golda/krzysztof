import sys

import pygame

from pygame.sprite import Group
from ustawienia import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():
    # Inicjalizacja gry
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    #Wyświetlanie przycisk gra
    play_button = Button(ai_settings, screen, "GRAJ")

    #Stworzenie egemplarza przechowującego statystyki oraz wyniku
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Utworzenie statku Utworzenie grupy do przechowywania pocisków oraz grupy przeciwników
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    #Stworzenie floty obcych
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Rozpoczęcie pętli gry
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
