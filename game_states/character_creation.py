# game_states/character_creation.py
"""Модуль для экрана создания персонажа."""

import pygame
from ui.button import Button
from ui.text_renderer import wrap_text, draw_wrapped_text
from data.paths import PATHS_DATA, get_localized_path_name, get_localized_path_description, get_path_color
from data.localization import get_text

class CharacterCreation:
    def __init__(self, screen, settings, on_character_created, on_back):
        self.screen = screen
        self.settings = settings
        self.on_character_created = on_character_created
        self.on_back = on_back

        self.font_title = pygame.font.SysFont(None, 50)
        self.font_normal = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 28)
        self.font_path_title = pygame.font.SysFont(None, 40) # Для заголовка пути

        self.state = "enter_name" # "enter_name", "choose_path"
        self.player_name = ""
        self.selected_path = None
        self.viewing_path = None # Путь, информация о котором сейчас отображается

        # --- Стили для UI ---
        self.ui_colors = {
            "input_border_default": (100, 100, 100),     # Серый
            "input_border_active": (255, 215, 0),        # Золотой (GOLD)
            "input_background": (50, 50, 50, 200),       # Темно-серый, почти черный, полупрозрачный
            "text_default": (255, 255, 255),             # Белый
            "text_placeholder": (150, 150, 150),         # Светло-серый
            "path_info_bg": (30, 30, 30, 220),           # Очень темный полупрозрачный фон для инфо
            "path_info_border": (100, 100, 100),         # Серая рамка для инфо
        }
        self.input_active = False # Флаг для отслеживания фокуса на поле ввода
        self.placeholder_text = "Введите имя героя..." # Плейсхолдер

        # --- UI Элементы ---
        # Они будут инициализированы в _create_ui_elements
        self.back_button = None
        self.name_input_box = None
        self.name_confirm_button = None
        self.path_buttons = []
        self.select_path_button = None
        self.path_info_area = None # Область для отображения информации о пути

        self._create_ui_elements()

    def _create_ui_elements(self):
        """Создает или пересоздает все UI элементы."""
        # Очищаем старые элементы
        self.path_buttons = []

        # Общие параметры
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Кнопка "Назад" (универсальная)
        self.back_button = Button(50, screen_height - 80, 150, 50,
                                  get_text(self.settings, "back"), (100, 100, 100), (200, 200, 200), self.font_normal)

        if self.state == "enter_name":
            self.name_input_box = pygame.Rect(screen_width // 2 - 200, 250, 400, 50)
            self.name_confirm_button = Button(screen_width // 2 - 75, 350, 150, 50,
                                              get_text(self.settings, "confirm"), (50, 150, 50), (100, 255, 100), self.font_normal)

        elif self.state == "choose_path":
            # Определяем области экрана
            left_panel_width = screen_width * 0.4 # 40% экрана для кнопок
            right_panel_x = left_panel_width + 20 # Начало правой панели
            panel_width = screen_width - right_panel_x - 20 # Ширина правой панели
            
            # Область для информации о пути (правая панель)
            self.path_info_area = pygame.Rect(right_panel_x, 100, panel_width, screen_height - 200)

            # Кнопки путей (левая панель)
            button_width = int(left_panel_width - 40) # Учитываем отступы
            button_height = 50
            start_x = (left_panel_width - button_width) // 2
            start_y = 100
            spacing = 65

            for i, path_data in enumerate(PATHS_DATA):
                button_y = start_y + i * spacing
                path_name = get_localized_path_name(self.settings, path_data)
                color = get_path_color(path_data)
                # Осветляем цвет для hover и выделения
                hover_color = tuple(min(255, c + 30) for c in color)
                selected_color = tuple(min(255, c + 50) for c in color) # Ещё светлее для выбранного
                
                button = Button(start_x, button_y, button_width, button_height,
                                path_name, color, hover_color, self.font_normal)
                # Добавляем выбранный цвет как атрибут кнопки
                button.selected_color = selected_color
                # action будет установлено позже в handle_event
                self.path_buttons.append((path_data, button))

            # Кнопка "Выбрать" внизу левой панели
            self.select_path_button = Button(start_x, screen_height - 150, button_width, 50,
                                             get_text(self.settings, "select"), (50, 150, 50), (100, 255, 100), self.font_normal)

    def handle_event(self, event, mouse_pos):
        """Обрабатывает события."""
        # --- Обработка событий в зависимости от текущего состояния экрана ---
        if self.state == "enter_name":
            if event.type == pygame.KEYDOWN:
                # Проверяем, активно ли поле ввода
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            self.state = "choose_path"
                            self._create_ui_elements() # Пересоздаем UI для нового состояния
                            self.input_active = False # Сбрасываем фокус
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        # Ограничиваем длину и разрешаем только определенные символы
                        if event.unicode.isprintable() and len(self.player_name) < 20:
                            # Можно добавить больше проверок, например, запрет на пробелы в начале
                            if not (event.unicode == ' ' and len(self.player_name) == 0):
                                self.player_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверяем клик по полю ввода для установки фокуса
                if self.name_input_box and self.name_input_box.collidepoint(mouse_pos):
                    self.input_active = True
                else:
                    self.input_active = False
                    
                # Используем is_clicked для корректной обработки и звука
                if self.name_confirm_button and self.name_confirm_button.is_clicked(mouse_pos, event):
                     if self.player_name.strip():
                         self.state = "choose_path"
                         self._create_ui_elements()
                         self.input_active = False # Сбрасываем фокус
                elif self.back_button and self.back_button.is_clicked(mouse_pos, event):
                     self.on_back()
                     self.input_active = False # Сбрасываем фокус

        elif self.state == "choose_path":
            if self.back_button and self.back_button.is_clicked(mouse_pos, event):
                self.state = "enter_name"
                self.selected_path = None
                self.viewing_path = None
                self._create_ui_elements()
            elif self.select_path_button and self.select_path_button.is_clicked(mouse_pos, event):
                 if self.selected_path and self.player_name:
                     # Создание персонажа завершено
                     character_data = {
                         "name": self.player_name.strip(),
                         "path_id": self.selected_path["id"]
                         # Позже добавим сюда атрибуты, навыки и т.д.
                     }
                     self.on_character_created(character_data)
            else:
                # Проверяем клики по кнопкам путей
                for path_data, button in self.path_buttons:
                    if button.is_clicked(mouse_pos, event):
                        # Устанавливаем выбранный путь для отображения информации и для возможного выбора
                        self.selected_path = path_data
                        self.viewing_path = path_data # Также устанавливаем как просматриваемый
                        print(f"Выбран путь: {get_localized_path_name(self.settings, path_data)}") # Отладка
                        break # Найден, выходим

    def update(self, mouse_pos):
        """Обновляет состояние UI элементов."""
        # Проверяем наведение для всех кнопок, которые существуют в текущем состоянии
        if self.state == "enter_name":
            if self.name_confirm_button:
                self.name_confirm_button.check_hover(mouse_pos)
            if self.back_button:
                self.back_button.check_hover(mouse_pos)
                
        elif self.state == "choose_path":
            if self.back_button:
                self.back_button.check_hover(mouse_pos)
            if self.select_path_button:
                self.select_path_button.check_hover(mouse_pos)
            
            # Проверяем наведение на кнопки путей и обновляем просматриваемый путь
            for path_data, button in self.path_buttons:
                button.check_hover(mouse_pos)
                # Если мышь наведена на кнопку, обновляем информацию (не обязательно, можно оставить только клик)
                # if button.is_hovered and self.viewing_path != path_data:
                #     self.viewing_path = path_data
                #     print(f"Просмотр пути при наведении: {get_localized_path_name(self.settings, path_data)}") # Отладка

    def draw(self):
        """Отрисовывает экран создания персонажа."""
        # НЕ заполняем экран черным, фон рисуется в main.py
        # self.screen.fill((0, 0, 0)) 

        if self.state == "enter_name":
            # --- Отрисовка экрана ввода имени ---
            title = self.font_title.render(get_text(self.settings, "enter_name_title"), True, (255, 215, 0)) # GOLD
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(title, title_rect)

            # --- Улучшенное поле ввода имени ---
            if self.name_input_box:
                # Создаем полупрозрачную поверхность для поля ввода
                input_surf = pygame.Surface((self.name_input_box.width, self.name_input_box.height), pygame.SRCALPHA)
                
                # Рисуем фон поля ввода
                pygame.draw.rect(input_surf, self.ui_colors["input_background"], 
                                (0, 0, self.name_input_box.width, self.name_input_box.height), 
                                border_radius=5)
                
                # Определяем цвет рамки в зависимости от фокуса
                border_color = self.ui_colors["input_border_active"] if self.input_active else self.ui_colors["input_border_default"]
                
                # Рисуем рамку поля ввода
                pygame.draw.rect(input_surf, border_color, 
                                (0, 0, self.name_input_box.width, self.name_input_box.height), 
                                2, border_radius=5)
                
                # Определяем текст для отображения
                display_text = self.player_name
                text_color = self.ui_colors["text_default"]
                
                # Если текст пустой и поле не активно, показываем плейсхолдер
                if not display_text and not self.input_active:
                    display_text = self.placeholder_text
                    text_color = self.ui_colors["text_placeholder"]
                
                # Рендерим текст
                text_surface = self.font_normal.render(display_text, True, text_color)
                
                # Ограничиваем ширину текста, чтобы он помещался в поле ввода
                max_text_width = self.name_input_box.width - 20 # Отступы
                if text_surface.get_width() > max_text_width:
                    # Можно добавить прокрутку текста, если он длинный
                    # Пока просто обрезаем
                    text_surface = text_surface.subsurface((0, 0, max_text_width, text_surface.get_height()))
                
                text_rect = text_surface.get_rect(midleft=(10, self.name_input_box.height // 2))
                
                # Отображаем текст на поверхности поля ввода
                input_surf.blit(text_surface, text_rect)
                
                # Отображаем поверхность поля ввода на основном экране
                self.screen.blit(input_surf, self.name_input_box.topleft)
            # --- Конец улучшенного поля ввода ---

            if self.name_confirm_button:
                self.name_confirm_button.draw(self.screen)
            if self.back_button:
                self.back_button.draw(self.screen)

        elif self.state == "choose_path":
            # --- Отрисовка экрана выбора пути ---
            title_text = get_text(self.settings, "choose_path_title").format(name=self.player_name.strip())
            title = self.font_title.render(title_text, True, (255, 215, 0))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(title, title_rect)

            # --- Отрисовка кнопок путей (левая панель) ---
            for path_data, button in self.path_buttons:
                # Если этот путь выбран, рисуем его с особым цветом
                if path_data == self.selected_path:
                    # Сохраняем оригинальные цвета
                    original_color = button.color
                    original_hover_color = button.hover_color
                    # Устанавливаем цвет выбранного
                    button.color = button.selected_color
                    # Рисуем
                    button.draw(self.screen)
                    # Восстанавливаем оригинальные цвета
                    button.color = original_color
                    button.hover_color = original_hover_color
                else:
                    button.draw(self.screen)

            # --- Отрисовка кнопки "Выбрать" ---
            if self.select_path_button:
                # Кнопка "Выбрать" активна только если путь выбран
                if self.selected_path:
                    self.select_path_button.draw(self.screen)
                else:
                    # Рисуем неактивную кнопку
                    inactive_surf = pygame.Surface((self.select_path_button.rect.width, self.select_path_button.rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(inactive_surf, (100, 100, 100, 150), (0, 0, self.select_path_button.rect.width, self.select_path_button.rect.height), border_radius=10)
                    pygame.draw.rect(inactive_surf, (150, 150, 150, 150), (0, 0, self.select_path_button.rect.width, self.select_path_button.rect.height), 2, border_radius=10)
                    text_surf = self.select_path_button.font.render(self.select_path_button.text, True, (150, 150, 150))
                    text_rect = text_surf.get_rect(center=(self.select_path_button.rect.width // 2, self.select_path_button.rect.height // 2))
                    inactive_surf.blit(text_surf, text_rect)
                    self.screen.blit(inactive_surf, self.select_path_button.rect)

            # --- Отрисовка кнопки "Назад" ---
            if self.back_button:
                self.back_button.draw(self.screen)

            # --- Отрисовка информации о выбранном/просматриваемом пути (правая панель) ---
            if self.path_info_area and self.viewing_path:
                # Рисуем фон для информации
                info_bg_surf = pygame.Surface((self.path_info_area.width, self.path_info_area.height), pygame.SRCALPHA)
                pygame.draw.rect(info_bg_surf, self.ui_colors["path_info_bg"], 
                                (0, 0, self.path_info_area.width, self.path_info_area.height), 
                                border_radius=10)
                pygame.draw.rect(info_bg_surf, self.ui_colors["path_info_border"], 
                                (0, 0, self.path_info_area.width, self.path_info_area.height), 
                                2, border_radius=10)
                self.screen.blit(info_bg_surf, self.path_info_area.topleft)
                
                # Отступы внутри области информации
                info_padding = 20
                info_start_x = self.path_info_area.x + info_padding
                info_start_y = self.path_info_area.y + info_padding
                info_width = self.path_info_area.width - 2 * info_padding
                
                # Заголовок - имя пути
                path_name = get_localized_path_name(self.settings, self.viewing_path)
                path_color = get_path_color(self.viewing_path)
                title_surface = self.font_path_title.render(path_name, True, path_color)
                self.screen.blit(title_surface, (info_start_x, info_start_y))
                
                # Описание
                description_y = info_start_y + title_surface.get_height() + 20
                description = get_localized_path_description(self.settings, self.viewing_path)
                desc_surfaces = wrap_text(description, self.font_small, info_width)
                draw_wrapped_text(self.screen, desc_surfaces, info_start_x, description_y)
                
                # Навыки
                skills_start_y = description_y + len(desc_surfaces) * (self.font_small.get_height() + 5) + 20
                skills_title = self.font_normal.render(get_text(self.settings, "path_skills") + ":", True, (200, 200, 200))
                self.screen.blit(skills_title, (info_start_x, skills_start_y))
                
                skills_list_start_y = skills_start_y + skills_title.get_height() + 10
                for i, skill in enumerate(self.viewing_path.get("skills", [])):
                    skill_name = self.font_small.render(f"• {skill['name']}", True, (255, 255, 255))
                    # Можно добавить описание навыка
                    # skill_desc = wrap_text(skill['description'], self.font_small, info_width)
                    self.screen.blit(skill_name, (info_start_x + 10, skills_list_start_y + i * (skill_name.get_height() + 5)))
