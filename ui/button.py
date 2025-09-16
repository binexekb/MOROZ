# ui/button.py
"""Модуль для создания и отрисовки кнопок."""

import pygame

class Button:
    # Статические переменные для хранения звука кнопки и настроек громкости
    click_sound = None
    sfx_volume = 1.0 # Будет установлен из main.py

    def __init__(self, x, y, width, height, text, color, hover_color, font, text_color=(255, 255, 255), is_toggle=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.text_color = text_color
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.is_hovered = False
        self.is_toggled = False
        self.is_toggle = is_toggle

    def draw(self, surface):
        # Создаем полупрозрачную поверхность для кнопки
        button_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        color = self.hover_color if self.is_hovered else self.color
        if self.is_toggle and self.is_toggled:
            # Можно использовать другой цвет для выделения выбранного переключателя
            color = tuple(min(255, c + 30) for c in color)
        
        # Рисуем прямоугольник с полупрозрачностью (например, 200 из 255)
        pygame.draw.rect(button_surf, (*color, 200), (0, 0, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(button_surf, (255, 255, 255, 200), (0, 0, self.rect.width, self.rect.height), 2, border_radius=10)
        
        # Рисуем текст
        text_rect = self.text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        button_surf.blit(self.text_surf, text_rect)
        
        # Отображаем полупрозрачную поверхность на основном экране
        surface.blit(button_surf, self.rect)

    def check_hover(self, pos):
        """Проверяет, наведена ли мышь на кнопку."""
        # ИСПРАВЛЕНО: Удалена попытка доступа к несуществующей переменной 'event'
        # Старая строка вызывала NameError:
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #    ...
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos, event):
        """Проверяет, была ли кнопка кликнута."""
        # Добавим отладочный вывод
        print(f"Button.is_clicked вызван для кнопки '{self.text}'") # <-- Отладка
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                # Воспроизводим звук, если он загружен
                # Добавим отладочный вывод
                if Button.click_sound:
                    print(f"Попытка воспроизвести звук. Громкость SFX: {Button.sfx_volume}") # <-- Отладка
                    Button.click_sound.set_volume(Button.sfx_volume)
                    play_result = Button.click_sound.play()
                    print(f"Звук воспроизведен. Результат: {play_result}") # <-- Отладка
                else:
                    print("Звук не воспроизводится, так как Button.click_sound is None") # <-- Отладка
                if self.is_toggle:
                    self.is_toggled = not self.is_toggled
                return True
        return False
