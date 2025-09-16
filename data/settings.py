# data/settings.py
"""Модуль для работы с настройками игры."""
import json
import os
import pygame

# --- Константы путей к медиафайлам ---
MAIN_MENU_MUSIC_FILE = "assets/main_menu.mp3"
BUTTON_SOUND_FILE = "assets/button_sound.mp3"
MAIN_MENU_BACKGROUND_FILE = "assets/mainpage_image.png"
SPLASH_IMAGE_FILE = "assets/zastavka.png"
SPLASH_VIDEO_FILE = "assets/zastavka.mp4"

# --- Константы по умолчанию ---
try:
    display_info = pygame.display.Info()
    DEFAULT_SCREEN_WIDTH = display_info.current_w
    DEFAULT_SCREEN_HEIGHT = display_info.current_h
except Exception:
    DEFAULT_SCREEN_WIDTH = 1920
    DEFAULT_SCREEN_HEIGHT = 1080

DEFAULT_SETTINGS = {
    "screen_width": DEFAULT_SCREEN_WIDTH,
    "screen_height": DEFAULT_SCREEN_HEIGHT,
    "fullscreen": True,
    "language": "ru",
    "music_volume": 0.5, # 50% для музыки
    "sfx_volume": 0.7,   # 70% для звуковых эффектов
}
SETTINGS_FILE = "settings.json"

COMMON_RESOLUTIONS = [
    (1280, 720), (1366, 768), (1440, 900), (1600, 900),
    (1680, 1050), (1920, 1080), (2560, 1440), (3840, 2160),
]

def load_settings():
    """Загружает настройки из файла или возвращает значения по умолчанию."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                for key, default_value in DEFAULT_SETTINGS.items():
                    if key not in settings:
                        settings[key] = default_value
                settings["fullscreen"] = True
                return settings
        except (json.JSONDecodeError, IOError, Exception) as e:
            print(f"Ошибка загрузки настроек: {e}. Используются настройки по умолчанию.")
            default_copy = DEFAULT_SETTINGS.copy()
            default_copy["fullscreen"] = True
            return default_copy
    else:
        default_copy = DEFAULT_SETTINGS.copy()
        default_copy["fullscreen"] = True
        save_settings(default_copy)
        return default_copy

def save_settings(settings):
    """Сохраняет настройки в файл."""
    settings["fullscreen"] = True
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        print(f"Ошибка сохранения настроек: {e}")

def set_display_mode(settings):
    """Устанавливает режим отображения на основе настроек (всегда полноэкранный)."""
    flags = pygame.FULLSCREEN | pygame.SCALED
    try:
        screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]), flags)
        return screen
    except pygame.error as e:
        print(f"Не удалось установить режим отображения с SCALED: {e}. Пробуем обычный FULLSCREEN.")
        flags = pygame.FULLSCREEN
        try:
            screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]), flags)
            return screen
        except pygame.error as e2:
            print(f"Не удалось установить полноэкранный режим: {e2}")
            try:
                screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]))
                print("Запуск в оконном режиме из-за ошибки установки полноэкранного режима.")
                return screen
            except pygame.error as e3:
                print(f"Критическая ошибка инициализации дисплея: {e3}")
                raise

def apply_display_settings(screen, settings):
    """Применяет настройки отображения (разрешение)."""
    flags = pygame.FULLSCREEN | pygame.SCALED
    try:
        new_screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]), flags)
        return new_screen
    except pygame.error as e:
        print(f"Не удалось применить настройки отображения: {e}")
        flags = pygame.FULLSCREEN
        try:
            new_screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]), flags)
            return new_screen
        except pygame.error as e2:
            print(f"Не удалось применить настройки отображения даже без SCALED: {e2}")
            return screen

def get_common_resolutions(current_width, current_height):
    """Возвращает список общих разрешений, включая текущее."""
    res_list = COMMON_RESOLUTIONS.copy()
    current_res = (current_width, current_height)
    if current_res not in res_list:
        res_list.append(current_res)
    res_list.sort()
    return res_list

def apply_volume_settings(settings):
    """Применяет настройки громкости ко всем аудио компонентам."""
    # Устанавливаем громкость для музыки
    pygame.mixer.music.set_volume(settings["music_volume"])
    # Громкость для звуков будет устанавливаться при их воспроизведении
    # или через глобальный механизм, если он будет добавлен

# --- Функции для загрузки медиафайлов ---
def load_main_menu_background(screen_width, screen_height):
    """Загружает и масштабирует фоновое изображение главного меню в режиме 'cover'."""
    try:
        if os.path.exists(MAIN_MENU_BACKGROUND_FILE):
            background = pygame.image.load(MAIN_MENU_BACKGROUND_FILE).convert()
            img_w, img_h = background.get_size()
            
            # Рассчитываем коэффициенты масштабирования
            scale_w = screen_width / img_w
            scale_h = screen_height / img_h
            
            # Выбираем больший коэффициент, чтобы изображение покрывало весь экран
            scale_factor = max(scale_w, scale_h)

            # Новые размеры изображения
            new_w = int(img_w * scale_factor)
            new_h = int(img_h * scale_factor)

            # Масштабируем изображение
            scaled_background = pygame.transform.smoothscale(background, (new_w, new_h))
            return scaled_background
        else:
            print(f"Файл фонового изображения '{MAIN_MENU_BACKGROUND_FILE}' не найден.")
            return None
    except pygame.error as e:
        print(f"Ошибка загрузки фонового изображения '{MAIN_MENU_BACKGROUND_FILE}': {e}")
        return None

def load_button_sound():
    """Загружает звук нажатия кнопки."""
    try:
        if os.path.exists(BUTTON_SOUND_FILE):
            button_sound = pygame.mixer.Sound(BUTTON_SOUND_FILE)
            return button_sound
        else:
            print(f"Файл звука кнопки '{BUTTON_SOUND_FILE}' не найден.")
            return None
    except pygame.error as e:
        print(f"Ошибка загрузки звука кнопки '{BUTTON_SOUND_FILE}': {e}")
        return None
