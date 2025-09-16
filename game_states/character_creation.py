# game_states/character_creation.py
"""Модуль для экрана создания персонажа."""

import pygame
import os
from ui.button import Button
from ui.text_renderer import wrap_text, draw_wrapped_text
from data.paths import PATHS_DATA, get_localized_path_name, get_localized_path_title, get_localized_path_description, get_path_color, get_path_by_id
from data.localization import get_text
from data.settings import PATH_IMAGES_FOLDER # <-- Импортируем путь к папке

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
            "path_button": (70, 70, 70),                 # Универсальный цвет для кнопок путей
            "path_button_hover": (100, 100, 100),        # Универсальный цвет hover для кнопок путей
            "path_button_selected": (120, 120, 120),     # Универсальный цвет selected для кнопок путей
        }
        self.input_active = False # Флаг для отслеживания фокуса на поле ввода
        # Плейсхолдер будет зависеть от языка

        # --- UI Элементы ---
        # Они будут инициализированы в _create_ui_elements
        self.back_button = None
        self.name_input_box = None
        self.name_confirm_button = None
        self.path_buttons = []
        self.select_path_button = None
        self.path_info_area = None # Область для отображения информации о пути

        # --- Загрузка изображений для путей ---
        self.path_images = {}
        self._load_path_images()

        self._create_ui_elements()

    def _load_path_images(self):
        """Загружает изображения для путей."""
        if not os.path.exists(PATH_IMAGES_FOLDER):
            print(f"Папка с изображениями путей '{PATH_IMAGES_FOLDER}' не найдена.")
            return
            
        for path_data in PATHS_DATA:
            path_id = path_data["id"]
            # Проверяем несколько возможных расширений
            extensions = ['.png', '.jpg', '.jpeg']
            image_loaded = False
            for ext in extensions:
                image_path = os.path.join(PATH_IMAGES_FOLDER, f"{path_id}{ext}")
                if os.path.exists(image_path):
                    try:
                        # Загружаем изображение
                        image = pygame.image.load(image_path).convert_alpha()
                        self.path_images[path_id] = image
                        print(f"Изображение для пути '{path_id}' загружено: {image_path}")
                        image_loaded = True
                        break # Нашли и загрузили, выходим из цикла расширений
                    except pygame.error as e:
                        print(f"Ошибка загрузки изображения '{image_path}': {e}")
            if not image_loaded:
                print(f"Изображение для пути '{path_id}' не найдено в '{PATH_IMAGES_FOLDER}' с расширениями {extensions}.")

    def _create_ui_elements(self):
        """Создает или пересоздает все UI элементы."""
        # Очищаем старые элементы
        self.path_buttons = []

        # Общие параметры
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Кнопка "Назад" (универсальная)
        self.back_button = Button(50, screen_height - 80, 150, 50,
                                  get_text(self.settings, "back"), 
                                  self.ui_colors["path_button"], 
                                  self.ui_colors["path_button_hover"], 
                                  self.font_normal)

        if self.state == "enter_name":
            self.name_input_box = pygame.Rect(screen_width // 2 - 200, 250, 400, 50)
            self.name_confirm_button = Button(screen_width // 2 - 75, 350, 150, 50,
                                              get_text(self.settings, "confirm"), 
                                              (50, 150, 50), (100, 255, 100), 
                                              self.font_normal)

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
                # Используем универсальные цвета
                color = self.ui_colors["path_button"]
                hover_color = self.ui_colors["path_button_hover"]
                selected_color = self.ui_colors["path_button_selected"]
                
                button = Button(start_x, button_y, button_width, button_height,
                                path_name, color, hover_color, self.font_normal)
                # Добавляем выбранный цвет как атрибут кнопки
                button.selected_color = selected_color
                # action будет установлено позже в handle_event
                self.path_buttons.append((path_data, button))

            # Кнопка "Выбрать" внизу левой панели
            self.select_path_button = Button(start_x, screen_height - 150, button_width, 50,
                                             get_text(self.settings, "select"), 
                                             (50, 150, 50), (100, 255, 100), 
                                             self.font_normal)

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
            
            # Проверяем наведение на кнопки путей
            for path_data, button in self.path_buttons:
                button.check_hover(mouse_pos)

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
                # Плейсхолдер обновляется при смене языка
                current_placeholder = get_text(self.settings, "enter_name_placeholder")
                if not display_text and not self.input_active:
                    display_text = current_placeholder
                    text_color = self.ui_colors["text_placeholder"]
                
                # Рендерим текст
                text_surface = self.font_normal.render(display_text, True, text_color)
                
                # Ограничиваем ширину текста, чтобы он помещался в поле ввода
                max_text_width = self.name_input_box.width - 20 # Отступы
                if text_surface.get_width() > max_text_width:
                    # Можно добавить прокрутку текста, если он длинный
                    # Пока просто обрезаем
                    # text_surface = text_surface.subsurface((0, 0, max_text_width, text_surface.get_height()))
                    # Лучше обрезать строку
                    temp_text = display_text
                    while self.font_normal.size(temp_text)[0] > max_text_width and len(temp_text) > 0:
                        temp_text = temp_text[:-1]
                    text_surface = self.font_normal.render(temp_text, True, text_color)
                
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
                
                current_y = info_start_y
                
                # 1. Заголовок - имя пути (белый цвет)
                path_name = get_localized_path_name(self.settings, self.viewing_path)
                title_surface = self.font_path_title.render(path_name, True, self.ui_colors["text_default"]) # Белый
                self.screen.blit(title_surface, (info_start_x, current_y))
                current_y += title_surface.get_height() + 10
                
                # 2. Изображение пути (если есть)
                path_id = self.viewing_path["id"]
                if path_id in self.path_images:
                    image = self.path_images[path_id]
                    # Масштабируем изображение, чтобы оно помещалось в отведенное пространство
                    img_max_width = info_width - 20
                    img_max_height = 300 # Максимальная высота изображения
                    img_w, img_h = image.get_size()
                    scale = min(img_max_width / img_w, img_max_height / img_h, 1.0) # Не увеличиваем
                    if scale < 1:
                        new_w, new_h = int(img_w * scale), int(img_h * scale)
                        scaled_img = pygame.transform.smoothscale(image, (new_w, new_h))
                    else:
                        scaled_img = image
                    
                    img_rect = scaled_img.get_rect(centerx=info_start_x + info_width // 2, top=current_y)
                    self.screen.blit(scaled_img, img_rect)
                    current_y += scaled_img.get_height() + 15
                else:
                    # Если изображения нет, добавим небольшой отступ
                    current_y += 10
                
                # 3. Подзаголовок - титул пути (белый цвет)
                path_title = get_localized_path_title(self.settings, self.viewing_path)
                title_surface = self.font_normal.render(path_title, True, self.ui_colors["text_default"]) # Белый
                self.screen.blit(title_surface, (info_start_x, current_y))
                current_y += title_surface.get_height() + 15
                
                # 4. Основное описание пути (белый цвет)
                description = get_localized_path_description(self.settings, self.viewing_path)
                desc_surfaces = wrap_text(description, self.font_small, info_width)
                # Убедимся, что весь текст белый
                white_desc_surfaces = []
                for surf in desc_surfaces:
                    # Получаем текст из поверхности pygame (это не всегда просто)
                    # Проще перерендерить с нужным цветом
                    # Но wrap_text уже создал поверхности. Предположим, что мы можем получить текст.
                    # В реальном проекте лучше передавать текст в wrap_text и рендерить там.
                    # Для демонстрации просто создадим новую поверхность белого цвета.
                    # Это немного костыльно, но сработает.
                    try:
                        # Попробуем получить текст (не работает напрямую с Surface)
                        # Лучше переписать wrap_text, чтобы он возвращал текст и мы рендерили сами.
                        # Пока оставим как есть, так как wrap_text из ui/text_renderer.py
                        # должен уже создавать поверхности с нужным цветом, если мы передадим его.
                        # Но в текущей реализации text_renderer.py цвет "зашит" как белый.
                        # Нужно модифицировать text_renderer.py или передавать цвет.
                        # Для простоты, просто пересоздадим поверхности.
                        
                        # Получаем bounding rect для получения размеров
                        text_rect = surf.get_rect()
                        # Создаем новую поверхность
                        new_surf = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
                        # Рендерим текст заново белым цветом
                        # Нам нужен исходный текст. wrap_text должен возвращать его.
                        # Переделаем логику.
                        pass # Логика обработки цвета в wrap_text/draw_wrapped_text
                        
                    except:
                        pass
                    white_desc_surfaces.append(surf) # Пока используем оригинальные поверхности
                        
                draw_wrapped_text(self.screen, white_desc_surfaces, info_start_x, current_y)
                # Рассчитываем новую Y позицию
                if white_desc_surfaces:
                    line_height = white_desc_surfaces[0].get_height() + 3 # +3 пикселя между строками
                    current_y += len(white_desc_surfaces) * line_height + 15
                else:
                    current_y += 15
                
                # 5. Навыки (белый цвет)
                skills_title = self.font_normal.render(get_text(self.settings, "path_skills") + ":", True, self.ui_colors["text_default"]) # Белый
                self.screen.blit(skills_title, (info_start_x, current_y))
                current_y += skills_title.get_height() + 10
                
                skills_list_start_y = current_y
                skills = self.viewing_path.get("skills", [])
                if skills:
                    total_skill_height = 0
                    skill_surfaces = [] # Для хранения поверхностей названий и описаний
                    for skill in skills:
                        # Название навыка
                        skill_name_text = f"• {skill['name']}"
                        skill_name_surf = self.font_small.render(skill_name_text, True, self.ui_colors["text_default"]) # Белый
                        
                        # Описание навыка
                        skill_desc_text = skill.get('description', '')
                        if isinstance(skill_desc_text, dict):
                            # Если описание локализованное
                            skill_desc_text = skill_desc_text.get(self.settings["language"], skill_desc_text.get("ru", ""))
                        
                        skill_desc_surfaces = wrap_text(skill_desc_text, self.font_small, info_width - 20)
                        # Убедимся, что описание тоже белое
                        white_skill_desc_surfaces = []
                        for desc_surf in skill_desc_surfaces:
                             white_skill_desc_surfaces.append(desc_surf) # Предполагаем, что wrap_text уже делает это
                             # В реальности нужно модифицировать wrap_text или перерендерить
                             
                        skill_surfaces.append((skill_name_surf, white_skill_desc_surfaces))
                        # Рассчитываем высоту для этого навыка
                        skill_height = skill_name_surf.get_height() + 5
                        if white_skill_desc_surfaces:
                            line_height = white_skill_desc_surfaces[0].get_height() + 3
                            skill_height += len(white_skill_desc_surfaces) * line_height
                        total_skill_height += skill_height + 10 # 10 пикселей между навыками
                    
                    # Теперь рисуем все навыки
                    current_skill_y = skills_list_start_y
                    for skill_name_surf, skill_desc_surfaces in skill_surfaces:
                        self.screen.blit(skill_name_surf, (info_start_x + 10, current_skill_y))
                        current_skill_y += skill_name_surf.get_height() + 5
                        if skill_desc_surfaces:
                            draw_wrapped_text(self.screen, skill_desc_surfaces, info_start_x + 20, current_skill_y)
                            line_height = skill_desc_surfaces[0].get_height() + 3
                            current_skill_y += len(skill_desc_surfaces) * line_height + 10
                        else:
                            current_skill_y += 10
                else:
                    # Если навыков нет
                    no_skills_text = self.font_small.render("Нет навыков", True, self.ui_colors["text_default"])
                    self.screen.blit(no_skills_text, (info_start_x + 10, skills_list_start_y))
