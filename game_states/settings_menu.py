# game_states/settings_menu.py
"""Модуль для меню настроек."""

import pygame
from ui.button import Button
from data.localization import get_text

class SettingsMenu:
    def __init__(self, screen, settings, on_back):
        self.screen = screen
        self.settings = settings
        self.on_back = on_back

        self.font_title = pygame.font.SysFont(None, 60)
        self.font_normal = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 24)

        # Флаг для main.py, сигнализирующий об изменении.
        # Возможные значения: None, "language", "music_volume", "sfx_volume"
        self.pending_change = None
        # Флаги для отслеживания, нужно ли обновлять конкретные индикаторы
        self.music_display_dirty = True
        self.sfx_display_dirty = True

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        """Создает кнопки меню настроек."""
        # Очищаем старые кнопки
        self.buttons = []
        settings_width = 400
        settings_height = 40
        settings_start_x = self.screen.get_width() // 2 - settings_width // 2
        settings_start_y = 150
        settings_spacing = 70 # Увеличиваем интервал из-за дополнительных элементов

        # Кнопка языка
        lang_text = f"{get_text(self.settings, 'language')}: {self.settings['language'].upper()}"
        lang_button = Button(settings_start_x, settings_start_y, settings_width, settings_height,
                             lang_text, (100, 100, 100), (200, 200, 200), self.font_normal, is_toggle=True)
        lang_button.is_toggled = self.settings["language"] == "en"
        lang_button.action = self._toggle_language
        self.buttons.append(("language", lang_button))

        # --- Громкость музыки ---
        # Перед созданием кнопки обновим её текст, если он "грязный"
        if self.music_display_dirty:
            self._update_music_display_text(settings_start_x, settings_start_y + settings_spacing, settings_width, settings_height)
        music_indicator = Button(settings_start_x, settings_start_y + settings_spacing, settings_width, settings_height,
                                  self._get_music_text(), (100, 100, 100), (100, 100, 100), self.font_normal, text_color=(255, 255, 255), is_toggle=False)
        self.buttons.append(("music_display", music_indicator))

        music_up_button = Button(settings_start_x + settings_width - 50, settings_start_y + settings_spacing, 40, settings_height,
                               "+", (50, 205, 50), (200, 200, 200), self.font_normal)
        music_up_button.action = self._increase_music_volume
        self.buttons.append(("music_up", music_up_button))
        
        music_down_button = Button(settings_start_x + 10, settings_start_y + settings_spacing, 40, settings_height,
                                 "-", (178, 34, 34), (200, 200, 200), self.font_normal)
        music_down_button.action = self._decrease_music_volume
        self.buttons.append(("music_down", music_down_button))

        # --- Громкость звуковых эффектов ---
        # Перед созданием кнопки обновим её текст, если он "грязный"
        if self.sfx_display_dirty:
            self._update_sfx_display_text(settings_start_x, settings_start_y + 2*settings_spacing, settings_width, settings_height)
        sfx_indicator = Button(settings_start_x, settings_start_y + 2*settings_spacing, settings_width, settings_height,
                                  self._get_sfx_text(), (100, 100, 100), (100, 100, 100), self.font_normal, text_color=(255, 255, 255), is_toggle=False)
        self.buttons.append(("sfx_display", sfx_indicator))

        sfx_up_button = Button(settings_start_x + settings_width - 50, settings_start_y + 2*settings_spacing, 40, settings_height,
                               "+", (50, 205, 50), (200, 200, 200), self.font_normal)
        sfx_up_button.action = self._increase_sfx_volume
        self.buttons.append(("sfx_up", sfx_up_button))
        
        sfx_down_button = Button(settings_start_x + 10, settings_start_y + 2*settings_spacing, 40, settings_height,
                                 "-", (178, 34, 34), (200, 200, 200), self.font_normal)
        sfx_down_button.action = self._decrease_sfx_volume
        self.buttons.append(("sfx_down", sfx_down_button))

        # Кнопка "Назад"
        back_button = Button(50, self.screen.get_height() - 80, 150, 50,
                             get_text(self.settings, "back"), (100, 100, 100), (200, 200, 200), self.font_normal)
        back_button.action = self.on_back
        self.buttons.append(("back", back_button))
        
        # Сбрасываем флаги "грязности"
        self.music_display_dirty = False
        self.sfx_display_dirty = False

    def _get_music_text(self):
        """Получает текст для индикатора громкости музыки."""
        return f"{get_text(self.settings, 'music_volume')}: {int(self.settings['music_volume'] * 100)}%"

    def _get_sfx_text(self):
        """Получает текст для индикатора громкости звуковых эффектов."""
        return f"{get_text(self.settings, 'sfx_volume')}: {int(self.settings['sfx_volume'] * 100)}%"
        
    def _update_music_display_text(self, x, y, width, height):
        """Обновляет текст кнопки-индикатора громкости музыки."""
        for i, (key, button) in enumerate(self.buttons):
            if key == "music_display":
                button.text = self._get_music_text()
                button.text_surf = button.font.render(button.text, True, button.text_color)
                button.text_rect = button.text_surf.get_rect(center=button.rect.center)
                return

    def _update_sfx_display_text(self, x, y, width, height):
        """Обновляет текст кнопки-индикатора громкости звуковых эффектов."""
        for i, (key, button) in enumerate(self.buttons):
            if key == "sfx_display":
                button.text = self._get_sfx_text()
                button.text_surf = button.font.render(button.text, True, button.text_color)
                button.text_rect = button.text_surf.get_rect(center=button.rect.center)
                return

    def handle_event(self, event, mouse_pos):
        """Обрабатывает события."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, button in self.buttons:
                # Проверяем, есть ли действие у кнопки, и вызываем его
                if button.rect.collidepoint(mouse_pos) and hasattr(button, 'action') and button.action:
                    # Выполняем действие
                    button.action()
                    # ВАЖНО: Не пересоздаем кнопки здесь. main.py будет решать, что делать.
                    # Просто выходим после первого совпадения, чтобы не обрабатывать другие кнопки
                    return 

    def update(self, mouse_pos):
        """Обновляет состояние кнопок."""
        for _, button in self.buttons:
            button.check_hover(mouse_pos)

    def draw(self):
        """Отрисовывает меню настроек."""
        # НЕ заполняем экран черным, фон рисуется в main.py
        # self.screen.fill((0, 0, 0))

        screen_width, screen_height = self.screen.get_size()
        
        title_text = get_text(self.settings, "settings_title")
        title_surface = self.font_title.render(title_text, True, (255, 215, 0))
        title_rect = title_surface.get_rect(center=(screen_width//2, 100))
        self.screen.blit(title_surface, title_rect)

        for _, button in self.buttons:
            button.draw(self.screen)

    # --- Методы для действий кнопок ---
    def _toggle_language(self):
        """Переключает язык."""
        self.settings["language"] = "en" if self.settings["language"] == "ru" else "ru"
        self.pending_change = "language"

    def _increase_music_volume(self):
        """Увеличивает громкость музыки."""
        self.settings["music_volume"] = min(1.0, round(self.settings["music_volume"] + 0.1, 1))
        print(f"Громкость музыки увеличена до: {self.settings['music_volume']}")
        # Помечаем индикатор как "грязный" для обновления
        self.music_display_dirty = True
        self.pending_change = "music_volume"

    def _decrease_music_volume(self):
        """Уменьшает громкость музыки."""
        self.settings["music_volume"] = max(0.0, round(self.settings["music_volume"] - 0.1, 1))
        print(f"Громкость музыки уменьшена до: {self.settings['music_volume']}")
        # Помечаем индикатор как "грязный" для обновления
        self.music_display_dirty = True
        self.pending_change = "music_volume"

    def _increase_sfx_volume(self):
        """Увеличивает громкость звуковых эффектов."""
        self.settings["sfx_volume"] = min(1.0, round(self.settings["sfx_volume"] + 0.1, 1))
        print(f"Громкость звуков увеличена до: {self.settings['sfx_volume']}")
        # Помечаем индикатор как "грязный" для обновления
        self.sfx_display_dirty = True
        self.pending_change = "sfx_volume"

    def _decrease_sfx_volume(self):
        """Уменьшает громкость звуковых эффектов."""
        self.settings["sfx_volume"] = max(0.0, round(self.settings["sfx_volume"] - 0.1, 1))
        print(f"Громкость звуков уменьшена до: {self.settings['sfx_volume']}")
        # Помечаем индикатор как "грязный" для обновления
        self.sfx_display_dirty = True
        self.pending_change = "sfx_volume"
