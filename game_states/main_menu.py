# game_states/main_menu.py
"""Модуль для главного меню."""

import pygame
from ui.button import Button
from data.localization import get_text

class MainMenu:
    def __init__(self, screen, settings, on_new_game, on_load_game, on_settings, on_exit):
        self.screen = screen
        self.settings = settings
        self.on_new_game = on_new_game
        self.on_load_game = on_load_game
        self.on_settings = on_settings
        self.on_exit = on_exit

        self.font_title = pygame.font.SysFont(None, 60)
        self.font_button = pygame.font.SysFont(None, 36)

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        self.buttons = []
        main_menu_width = 400
        main_menu_height = 50
        main_menu_start_x = (self.screen.get_width() - main_menu_width) // 2
        main_menu_start_y = 250
        main_menu_spacing = 70

        main_menu_items = [
            {"text_key": "new_game", "color": (25, 25, 112), "hover_color": (70, 130, 180), "action": self.on_new_game},
            {"text_key": "load_game", "color": (70, 130, 180), "hover_color": (100, 170, 220), "action": self.on_load_game},
            {"text_key": "settings", "color": (180, 180, 180), "hover_color": (220, 220, 220), "action": self.on_settings},
            {"text_key": "exit", "color": (178, 34, 34), "hover_color": (220, 20, 60), "action": self.on_exit}
        ]

        for i, item in enumerate(main_menu_items):
            button_y = main_menu_start_y + i * main_menu_spacing
            button_text = get_text(self.settings, item["text_key"])
            button = Button(main_menu_start_x, button_y, main_menu_width, main_menu_height,
                            button_text, item["color"], item["hover_color"], self.font_button)
            button.action = item["action"] # Сохраняем действие в кнопке
            self.buttons.append(button)

    def handle_event(self, event, mouse_pos):
        """Обрабатывает события, используя button.is_clicked для звука."""
        # Используем button.is_clicked() для обработки кликов и воспроизведения звука
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                # is_clicked проверит попадание и воспроизведет звук
                if button.is_clicked(mouse_pos, event):
                    # Если клик был обработан, вызываем action
                    if hasattr(button, 'action') and button.action:
                        button.action()
                    # Обработали клик, выходим из цикла
                    break

    def update(self, mouse_pos):
        for button in self.buttons:
            button.check_hover(mouse_pos)

    def draw(self):
        # self.screen.fill((0, 0, 0)) # Убрано, фон рисуется в main.py

        title_text = get_text(self.settings, "title")
        title_surface = self.font_title.render(title_text, True, (255, 215, 0))
        title_rect = title_surface.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        subtitle_text = get_text(self.settings, "main_menu")
        subtitle_surface = self.font_button.render(subtitle_text, True, (200, 200, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen.get_width()//2, 160))
        self.screen.blit(subtitle_surface, subtitle_rect)

        for button in self.buttons:
            button.draw(self.screen)
