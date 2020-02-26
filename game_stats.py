class GameStats():
    """Monitorowanie statystyk w grze"""

    def __init__(self, ai_settings):
        """Inicjalizacja statystyk"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #Uruchomienie gry w stanie aktywnym
        self.game_active = False

    def reset_stats(self):
        """Statystyki, które zmieniają się podczas gry"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1