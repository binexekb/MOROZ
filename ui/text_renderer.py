# ui/text_renderer.py
"""Модуль для вспомогательных функций отрисовки текста."""

import pygame

def wrap_text(text, font, max_width, color=(255, 255, 255)):
    """
    Разбивает текст на строки, чтобы они помещались в заданную ширину.
    Возвращает список строк Surface указанного цвета.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        # Получаем ширину тестовой строки
        if font.size(test_line)[0] > max_width:
            if current_line: # Если текущая строка не пуста, добавляем её
                lines.append(current_line)
                current_line = word + " "
            else: # Если слово слишком длинное, помещаем его в отдельную строку
                lines.append(word)
                current_line = ""
        else:
            current_line = test_line

    if current_line: # Добавляем последнюю строку
        lines.append(current_line.strip())

    # Преобразуем строки в Surface указанного цвета
    surfaces = [font.render(line, True, color) for line in lines]
    return surfaces

def draw_wrapped_text(surface, text_surfaces, x, y, line_height=None):
    """Отрисовывает список строк Surface на заданной позиции."""
    if not line_height and text_surfaces:
        # Получаем высоту строки из первой поверхности, если не задана
        line_height = text_surfaces[0].get_height() + 3 # +3 пикселя между строками
    elif not line_height:
        line_height = 20 # fallback

    for i, text_surf in enumerate(text_surfaces):
        surface.blit(text_surf, (x, y + i * line_height))
