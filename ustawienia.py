class Settings():
    """Ustawienia Gry"""

    def __init__(self):
        #Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #Ustawienia statku
        self.ship_limit = 3

        #Ustawienia pocisków
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #Ustawienia przeciwnika
        self.fleet_drop_speed = 10

        #Zmiana szybkości gry
        self.speedup_scale = 1.1
        #Zwiększenie punktacji od trudności
        self.score_scale = 1.5

        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        """Ustawienia zmieniające się podzas gry"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #Punktacja
        self.alien_points = 50

        #fleet_direction = 1 oznacza prawo -1 lewo
        self.fleet_direction = 1

    def increase_speed(self):
        """Zmiany szybkości i liczby punktów"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)