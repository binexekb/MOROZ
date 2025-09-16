# main.py
"""Главная точка входа в игру."""

import pygame
import sys
import os

# Импорты из наших модулей
from data.settings import (
    load_settings, save_settings, set_display_mode, apply_volume_settings,
    load_main_menu_background, load_button_sound
)
from data.localization import get_text
from game_states.splash_screen import SplashScreen
from game_states.main_menu import MainMenu
from game_states.settings_menu import SettingsMenu
from game_states.character_creation import CharacterCreation

# --- Константы ---
FPS = 60

def main():
    """Главная функция игры."""
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512) # Улучшает задержку звука
    pygame.mixer.init()
    
    # --- Загрузка настроек ---
    settings = load_settings()
    
    # --- Инициализация экрана ---
    screen = set_display_mode(settings)
    pygame.display.set_caption(get_text(settings, "title"))
    clock = pygame.time.Clock()

    # --- Загрузка медиафайлов ---
    button_sound = load_button_sound()
    if button_sound:
        print("Звук кнопки успешно загружен.")
        from ui.button import Button
        Button.click_sound = button_sound
        # Устанавливаем начальную громкость звуков
        Button.sfx_volume = settings["sfx_volume"]
    else:
        print("Звук кнопки НЕ БЫЛ загружен. Проверьте путь к файлу и его формат.")
    
    main_menu_music_file = "assets/main_menu.mp3" # Путь дублируется, можно вынести в settings
    main_menu_music_loaded = False
    if os.path.exists(main_menu_music_file):
        try:
            pygame.mixer.music.load(main_menu_music_file)
            apply_volume_settings(settings) # Применяем громкость музыки сразу после загрузки
            main_menu_music_loaded = True
        except pygame.error as e:
            print(f"Ошибка загрузки музыки '{main_menu_music_file}': {e}")
    else:
        print(f"Файл музыки '{main_menu_music_file}' не найден.")

    # --- Состояния игры ---
    class GameState:
        SPLASH = "splash"
        MAIN_MENU = "main_menu"
        SETTINGS = "settings"
        CHARACTER_CREATION = "character_creation"

    current_state = GameState.SPLASH

    # --- Callback для обновления screen у всех состояний ---
    def update_all_screens(new_screen):
        """Обновляет screen у всех игровых состояний."""
        nonlocal screen
        screen = new_screen
        try:
            splash_screen.screen = screen
        except NameError:
            pass # splash_screen еще не создан
        main_menu.screen = screen
        # settings_menu.screen будет обновлен в draw/update цикле при необходимости
        character_creation.screen = screen
        pygame.display.set_caption(get_text(settings, "title"))

    # --- Инициализация состояний (с callback'ами) ---
    def finish_splash():
        """Вызывается по завершении заставки."""
        nonlocal current_state
        current_state = GameState.MAIN_MENU
        # Начинаем воспроизводить музыку главного меню после заставки
        if main_menu_music_loaded:
            try:
                # Громкость уже установлена в apply_volume_settings при загрузке
                pygame.mixer.music.play(-1) # -1 для зацикливания
            except pygame.error as e:
                print(f"Ошибка воспроизведения музыки: {e}")

    def start_new_game():
        """Вызывается при нажатии 'Новая Игра'."""
        nonlocal current_state
        current_state = GameState.CHARACTER_CREATION
        # Музыка меню продолжает играть во время создания персонажа

    def go_to_settings():
        """Вызывается при нажатии 'Настройки'."""
        nonlocal current_state, settings_menu
        current_state = GameState.SETTINGS
        # settings_menu будет создан/пересоздан в цикле

    def exit_game():
        """Вызывается при нажатии 'Выход'."""
        save_settings(settings)
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    def back_to_main_menu():
        """Вызывается при нажатии 'Назад' в различных меню."""
        nonlocal current_state
        current_state = GameState.MAIN_MENU
        # Перезапускаем музыку меню при возврате, если она не играет
        if main_menu_music_loaded and not pygame.mixer.music.get_busy():
            try:
                # Убеждаемся, что громкость актуальна
                apply_volume_settings(settings)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Ошибка воспроизведения музыки: {e}")

    def character_created(character_data):
        """Callback при завершении создания персонажа."""
        # Этот callback вызывается, когда создание персонажа завершено.
        # Здесь будет логика перехода к真正的 игре, где музыка меню должна остановиться.
        from data.paths import get_localized_path_name, get_path_by_id
        path_data = get_path_by_id(character_data['path_id'])
        if path_data:
            path_name = get_localized_path_name(settings, path_data)
        else:
            path_name = character_data['path_id'] # fallback
        print(get_text(settings, "character_created").format(name=character_data['name'], path=path_name))
        
        print("Персонаж создан. Переход к основной игре...")
        # TODO: Здесь нужно остановить музыку меню и запустить игровую музыку/логику
        pygame.mixer.music.stop() # Останавливаем музыку меню при переходе к реальной игре
        print("Музыка меню остановлена. Запуск игры...")
        # Пока просто возвращаем в меню
        back_to_main_menu()

    # Создание экземпляров состояний
    splash_screen = SplashScreen(screen, settings, finish_splash)
    # Инициализируем меню без фона, он будет рисоваться в основном цикле
    main_menu = MainMenu(screen, settings, start_new_game, lambda: print(get_text(settings, "loading_not_implemented")), go_to_settings, exit_game)
    # settings_menu инициализируем как None, будет создан при переходе
    settings_menu = None
    character_creation = CharacterCreation(screen, settings, character_created, back_to_main_menu)

    # --- Основной игровой цикл ---
    running = True
    # Для отрисовки фона меню
    main_menu_background = None
    main_menu_background_dims = (0, 0) # Для отслеживания изменений размера

    while running:
        # Загружаем/обновляем фон, если это необходимо
        screen_width, screen_height = screen.get_size()
        if (main_menu_background is None or 
            main_menu_background_dims != (screen_width, screen_height)):
            main_menu_background = load_main_menu_background(screen_width, screen_height)
            main_menu_background_dims = (screen_width, screen_height)
            
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                save_settings(settings)
                running = False

            # --- ТЕСТ: Воспроизведение звука по нажатию 'B' ---
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_b and button_sound:
            #         print("Тестовое воспроизведение звука по нажатию 'B'")
            #         button_sound.set_volume(settings["sfx_volume"])
            #         button_sound.play()
            # --- КОНЕЦ ТЕСТА ---

            # --- Обработка событий в зависимости от состояния ---
            # ВАЖНО: Убираем проверки 'and settings_menu' и т.д.
            # Если состояние SETTINGS, мы должны обрабатывать события, даже если объект еще не создан
            if current_state == GameState.SPLASH:
                splash_screen.handle_event(event, mouse_pos)
            elif current_state == GameState.MAIN_MENU:
                main_menu.handle_event(event, mouse_pos)
            elif current_state == GameState.SETTINGS:
                 # settings_menu будет создан ниже, если он нужен
                 if settings_menu: # Только если он уже существует
                     settings_menu.handle_event(event, mouse_pos)
            elif current_state == GameState.CHARACTER_CREATION:
                character_creation.handle_event(event, mouse_pos)

        # --- Обновление ---
        if current_state == GameState.SPLASH:
            splash_screen.update(mouse_pos)
        elif current_state == GameState.MAIN_MENU:
             main_menu.update(mouse_pos)
        elif current_state == GameState.SETTINGS:
             # Пересоздаем settings_menu при каждом цикле в состоянии SETTINGS
             # Это гарантирует, что он всегда существует и имеет правильные параметры
             if settings_menu is None:
                 settings_menu = SettingsMenu(screen, settings, back_to_main_menu)
             settings_menu.update(mouse_pos)
             
             if settings_menu:
                 change_type = getattr(settings_menu, 'pending_change', None)
                 if change_type == "language":
                     print("Применение изменений языка...")
                     save_settings(settings)
                     main_menu = MainMenu(screen, settings, start_new_game, lambda: print(get_text(settings, "loading_not_implemented")), go_to_settings, exit_game)
                     character_creation = CharacterCreation(screen, settings, character_created, back_to_main_menu)
                     # Пересоздаем settings_menu с новым языком
                     settings_menu = SettingsMenu(screen, settings, back_to_main_menu)
                     settings_menu.pending_change = None
                 elif change_type == "music_volume":
                     print("Применение изменений громкости музыки...")
                     save_settings(settings)
                     # НЕМЕДЛЕННО применяем громкость музыки
                     apply_volume_settings(settings) # Применяет pygame.mixer.music.set_volume
                     # Пересоздаем settings_menu, чтобы обновить отображение громкости
                     settings_menu = SettingsMenu(screen, settings, back_to_main_menu)
                     settings_menu.pending_change = None
                 elif change_type == "sfx_volume":
                     print("Применение изменений громкости звуков...")
                     save_settings(settings)
                     # НЕМЕДЛЕННО обновляем громкость звуков для кнопок
                     if button_sound:
                         from ui.button import Button
                         Button.sfx_volume = settings["sfx_volume"]
                     # Пересоздаем settings_menu, чтобы обновить отображение громкости
                     settings_menu = SettingsMenu(screen, settings, back_to_main_menu)
                     settings_menu.pending_change = None
        elif current_state == GameState.CHARACTER_CREATION:
             character_creation.update(mouse_pos)

        # --- Рендеринг ---
        # Всегда рисуем фон, если он загружен и мы не на заставке
        # Используем режим "cover" - изображение масштабируется, чтобы покрыть весь экран
        if main_menu_background and current_state != GameState.SPLASH:
            # Центрируем фон (он уже правильно масштабирован)
            bg_rect = main_menu_background.get_rect(center=(screen_width//2, screen_height//2))
            screen.blit(main_menu_background, bg_rect)
        
        # ВАЖНО: Убираем проверки 'and settings_menu'
        if current_state == GameState.SPLASH:
            splash_screen.draw()
        elif current_state == GameState.MAIN_MENU:
            main_menu.draw()
        elif current_state == GameState.SETTINGS:
            # Убедимся, что settings_menu существует перед рисованием
            # (на случай, если он не был создан в update)
            if settings_menu is None:
                settings_menu = SettingsMenu(screen, settings, back_to_main_menu)
            settings_menu.draw()
        elif current_state == GameState.CHARACTER_CREATION:
            character_creation.draw()

        pygame.display.flip()
        clock.tick(FPS)

    save_settings(settings)
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
