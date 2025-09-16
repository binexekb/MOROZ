# game_states/splash_screen.py
"""Модуль для экрана заставки."""

import pygame
import os

# Пути к медиафайлам
SPLASH_IMAGE_FILE = "assets/zastavka.png" # Или .jpg
SPLASH_VIDEO_FILE = "assets/zastavka.mp4"
SPLASH_DURATION = 3000 # 3 секунды в миллисекундах

# Попытка импорта MoviePy
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("MoviePy не найден. Будет использована статичная заставка.")

class SplashScreen:
    def __init__(self, screen, settings, on_finish):
        self.screen = screen
        self.settings = settings
        self.on_finish = on_finish # Callback при завершении заставки

        self.state = "loading" # "loading", "video", "image", "finished"
        self.start_time = pygame.time.get_ticks()
        
        # --- Загрузка медиа ---
        self.splash_clip = None
        self.splash_surface = None
        
        if MOVIEPY_AVAILABLE:
            try:
                if os.path.exists(SPLASH_VIDEO_FILE):
                    self.splash_clip = VideoFileClip(SPLASH_VIDEO_FILE)
                    self.state = "video"
                    print(f"Видео заставка '{SPLASH_VIDEO_FILE}' загружена.")
                else:
                    raise FileNotFoundError(f"Видео файл {SPLASH_VIDEO_FILE} не найден.")
            except Exception as e:
                print(f"Не удалось загрузить видео заставку '{SPLASH_VIDEO_FILE}': {e}")
                self._load_static_image()
        else:
            self._load_static_image()

    def _load_static_image(self):
        """Загружает статическое изображение заставки."""
        try:
            if os.path.exists(SPLASH_IMAGE_FILE):
                self.splash_surface = pygame.image.load(SPLASH_IMAGE_FILE).convert()
                self.state = "image"
                print(f"Загружена статичная заставка '{SPLASH_IMAGE_FILE}'.")
            else:
                raise FileNotFoundError(f"Изображение {SPLASH_IMAGE_FILE} не найдено.")
        except (pygame.error, FileNotFoundError) as e:
            print(f"Не удалось загрузить изображение заставки '{SPLASH_IMAGE_FILE}': {e}")
            self.state = "finished" # Пропускаем заставку

    def handle_event(self, event, mouse_pos):
        """Обрабатывает события."""
        if self.state != "finished":
            # Позволяем пропустить заставку по нажатию клавиши или клику мыши
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                self._finish()

    def update(self, mouse_pos):
        """Обновляет логику заставки."""
        if self.state == "finished":
            return # Ничего не делаем, если уже завершено

        current_time = pygame.time.get_ticks()
        elapsed_time_ms = current_time - self.start_time

        if self.state == "video":
            clip_duration_ms = self.splash_clip.duration * 1000
            if elapsed_time_ms > clip_duration_ms:
                self._finish()
        
        elif self.state == "image":
            if elapsed_time_ms > SPLASH_DURATION:
                self._finish()

    def draw(self):
        """Отрисовывает заставку."""
        if self.state == "video":
            current_time = pygame.time.get_ticks()
            elapsed_time_ms = current_time - self.start_time
            t = elapsed_time_ms / 1000.0
            if 0 <= t <= self.splash_clip.duration:
                try:
                    frame = self.splash_clip.get_frame(t=t)
                    if frame is not None and frame.size > 0:
                        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                        # Масштабируем под экран, сохраняя пропорции
                        screen_w, screen_h = self.settings["screen_width"], self.settings["screen_height"]
                        img_w, img_h = frame_surface.get_size()
                        scale = min(screen_w / img_w, screen_h / img_h)
                        new_w, new_h = int(img_w * scale), int(img_h * scale)
                        scaled_frame = pygame.transform.smoothscale(frame_surface, (new_w, new_h))
                        rect = scaled_frame.get_rect(center=(screen_w//2, screen_h//2))
                        self.screen.blit(scaled_frame, rect)
                    else:
                        self.screen.fill((0, 0, 0))
                except Exception as e:
                    print(f"Ошибка получения кадра видео: {e}")
                    self.screen.fill((0, 0, 0))
        
        elif self.state == "image" and self.splash_surface:
            # Масштабируем изображение под экран, сохраняя пропорции
            screen_w, screen_h = self.settings["screen_width"], self.settings["screen_height"]
            img_w, img_h = self.splash_surface.get_size()
            scale = min(screen_w / img_w, screen_h / img_h)
            new_w, new_h = int(img_w * scale), int(img_h * scale)
            scaled_image = pygame.transform.smoothscale(self.splash_surface, (new_w, new_h))
            rect = scaled_image.get_rect(center=(screen_w//2, screen_h//2))
            self.screen.blit(scaled_image, rect)
        
        # Если state == "finished" или изображение/видео не загружено, экран остается черным

    def _finish(self):
        """Завершает показ заставки и освобождает ресурсы."""
        self.state = "finished"
        if self.splash_clip:
            self.splash_clip.close()
            self.splash_clip = None
        self.on_finish() # Вызываем callback

    def is_finished(self):
        """Проверяет, завершена ли заставка."""
        return self.state == "finished"