# data/paths.py
"""Модуль, определяющий данные о Путях (Аэтралах)."""

# Импортируем навыки
from .skills import SKILLS_DATA
from . import localization # Для получения локализованных названий/описаний

# Цвета для путей (RGB)
PATH_COLORS = {
    "relaamon": (25, 25, 112),      # DARK BLUE
    "vortira": (139, 0, 0),         # DARK RED
    "light_shadow": (148, 0, 211),  # DARK VIOLET
    "sailyora": (255, 215, 0),      # GOLD
    "gravaan": (47, 79, 79),        # DARK SLATE GRAY
    "kyriel": (0, 191, 255),        # DEEP SKY BLUE
    "nerradis_onna": (34, 139, 34), # FOREST GREEN
}

# Определяем данные путей с расширенными описаниями (титулами)
PATHS_DATA = [
    {
        "id": "relaamon",
        "name_key": "path_relaamon",
        "title_key": "path_relaamon_title", # Новый ключ для титула
        "description_key": "path_relaamon_desc",
        "color_key": "relaamon",
        "primary_attributes": ["energy_crystal", "harmony", "intelligence"],
        "skills": SKILLS_DATA.get("path_relaamon", [])
    },
    {
        "id": "vortira",
        "name_key": "path_vortira",
        "title_key": "path_vortira_title",
        "description_key": "path_vortira_desc",
        "color_key": "vortira",
        "primary_attributes": ["energy_chaos", "energy_order", "health"],
        "skills": SKILLS_DATA.get("path_vortira", [])
    },
    {
        "id": "light_shadow",
        "name_key": "path_light_shadow",
        "title_key": "path_light_shadow_title",
        "description_key": "path_light_shadow_desc",
        "color_key": "light_shadow",
        "primary_attributes": ["balance_light", "balance_shadow", "dexterity"],
        "skills": SKILLS_DATA.get("path_light_shadow", [])
    },
    {
        "id": "sailyora",
        "name_key": "path_sailyora",
        "title_key": "path_sailyora_title",
        "description_key": "path_sailyora_desc",
        "color_key": "sailyora",
        "primary_attributes": ["energy_threads", "intelligence", "dexterity"],
        "skills": SKILLS_DATA.get("path_sailyora", [])
    },
    {
        "id": "gravaan",
        "name_key": "path_gravaan",
        "title_key": "path_gravaan_title",
        "description_key": "path_gravaan_desc",
        "color_key": "gravaan",
        "primary_attributes": ["gravitational_potential", "stamina", "strength"],
        "skills": SKILLS_DATA.get("path_gravaan", [])
    },
    {
        "id": "kyriel",
        "name_key": "path_kyriel",
        "title_key": "path_kyriel_title",
        "description_key": "path_kyriel_desc",
        "color_key": "kyriel",
        "primary_attributes": ["chronic_energy", "intelligence", "dexterity"],
        "skills": SKILLS_DATA.get("path_kyriel", [])
    },
    {
        "id": "nerradis_onna",
        "name_key": "path_nerradis_onna",
        "title_key": "path_nerradis_onna_title",
        "description_key": "path_nerradis_onna_desc",
        "color_key": "nerradis_onna",
        "primary_attributes": ["life_energy", "stamina", "strength"],
        "skills": SKILLS_DATA.get("path_nerradis_onna", [])
    },
]

def get_localized_path_name(settings, path_data):
    """Получает локализованное имя пути."""
    return localization.get_text(settings, path_data["name_key"])

def get_localized_path_title(settings, path_data):
    """Получает локализованный титул пути."""
    return localization.get_text(settings, path_data["title_key"])

def get_localized_path_description(settings, path_data):
    """Получает локализованное описание пути."""
    return localization.get_text(settings, path_data["description_key"])

def get_path_color(path_data):
    """Получает цвет пути."""
    return PATH_COLORS.get(path_data["color_key"], (100, 100, 100)) # Серый по умолчанию

# Добавим функцию для получения пути по ID
def get_path_by_id(path_id):
    """Возвращает данные пути по его ID."""
    for path in PATHS_DATA:
        if path["id"] == path_id:
            return path
    return None