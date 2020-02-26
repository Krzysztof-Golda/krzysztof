import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Reagowanie na naciśnięcie klawisza"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
     #Utworzenie nowego pocisku
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Reagowanie na nie naciśnięcie klawisza"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Reagowanie na klawiature i mysz"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Rozpoczęcie nowej gry po kliknięciu GRAJ"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Wyzerowanie ustawień gry
        ai_settings.initialize_dynamic_settings()

        #Wyzerowanie statystyk
        stats.reset_stats()
        stats.game_active = True

        #Wyzerowanie wyników
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        #Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()

        #Utworzenie nowej floty
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Uaktualnienie obrazków na ekranie"""
    # Odświerzanie ekranu w każdej iteracji
    screen.fill(ai_settings.bg_color)
    #Wyświetlanie wszystkich pocisków pod warstwami statku kosmicznego i obcych
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #Wyświetlanie info o punktacji
    sb.show_score()

    #Wyświetlanie przycisku tylko gdy gra jest nieaktywna
    if not stats.game_active:
        play_button.draw_button()

    # Wyświetlanie ostatnio zmodyfikowanego ekranu
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Uaktualnienie położenia pocisków i usunięcie niewidocznych"""
    bullets.update()
    # usuwanie niewidocznych pocisków
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #Sprawdzenie czy pocisk trafił przeciwnika.
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Reacje na kolizje pocisku i przeciwnika"""
    #Usuwanie pocisków i obcych w których doszło do kolizji
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        for aliens in collision.values():
            stats.score += ai_settings.alien_points * len(aliens )
            sb.prep_score()

    if len(aliens) == 0:
        # Pozbycie się pocisków i stworzenie nowej floty
        bullets.empty()
        ai_settings.increase_speed()
        #Inkrementacja poziomu
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    """Ustalenie liczby obcych, którzy mieszczą sie w rzędzie"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Ustalenie ile rzędów przeciwników zmieści się na ekranie"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Stworzenie przeciwnika i dodanie go do rzędu"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Utworzenie pełnej floty obcych"""
    #Utworzenie obcego i ustalenie liczby obcych w rzędzie oraz odległości między nimi
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Utworzenie pierwszego rzędu przeciwników
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Przesunięcie całej floty w dół i zmiana kierunku poruszania"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Reakcja na uderzenie aliena w statek gracza"""
    if stats.ships_left > 0:
        #Zmniejszenie wartości ships_left
        stats.ships_left -= 1

        #Uaktualnienie tablicy wyników
        sb.prep_ships()

        #Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()

        #Utworzenie nowej floty i wyśrodkowanie statku
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pauza
        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """prawdzenie, czy wróg dotarłdo krawędzi"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #To samo co uderzenie o statek
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Sprawdzenie czy flota jest przy krawędzi ekranu, uaktualnienie położenia przeciwników w flocie"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #wykrycie kolizji statku i aliena
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    #wykrycie aliena docierającego do krawędzi ekranu
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)