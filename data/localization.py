# data/localization.py
"""Модуль для локализации текстов игры."""

LOCALIZATION = {
    "ru": {
        "title": "Вселенная Релаамо",
        "main_menu": "Главное Меню",
        "new_game": "Новая Игра",
        "load_game": "Загрузить Игру",
        "settings": "Настройки",
        "exit": "Выход",
        "class_selection_title": "Выберите свой Путь",
        "back": "Назад",
        "continue": "Нажмите любую клавишу для продолжения...",
        "settings_title": "Настройки",
        "language": "Язык",
        "music_volume": "Громкость музыки",
        "sfx_volume": "Громкость эффектов",
        "resolution": "Разрешение",
        "fullscreen": "Полноэкранный режим",
        "on": "Вкл",
        "off": "Выкл",
        "selected": "Выбрано",
        "path_selected": "Вы выбрали",
        "loading_not_implemented": "Функция загрузки ещё не реализована.",
        "resolution_prompt": "Нажмите Enter для применения",
        "fullscreen_prompt": "Нажмите F для переключения",
        # --- Для создания персонажа ---
        "enter_name_title": "Введите имя вашего персонажа",
        "enter_name_placeholder": "Введите имя героя...", # <-- Новый ключ
        "confirm": "Подтвердить",
        "choose_path_title": "{name}, выберите свой Путь",
        "view_path_title": "Детали Пути",
        "select": "Выбрать",
        "path_description": "Описание",
        "path_skills": "Навыки",
        "character_created": "Персонаж {name} создан! Путь: {path}",
        # --- Названия и описания Путей ---
        "path_relaamon": "Путь Релаамона",
        "path_relaamon_title": "Верховный Ткач, Отец-Кристалл", # <-- Новый ключ
        "path_relaamon_desc": "Не бог, но сама суть Релаамо, проявленная в сознании. Его голос — гул энергетических вихрей, а тело — структура Кристалла. Он не вмешивается в миры, но его ритм задает законы бытия. Мудрецы Страрии верят, что медитация на его грани открывает истину мироздания.",
        "path_vortira": "Путь Вортиры",
        "path_vortira_title": "Мать Хаоса и Порядка, Владычица Эфирных Воронок", # <-- Новый ключ
        "path_vortira_desc": "Рожденная из первого импульса, ударившего в эфирную воронку. Её двойственная природа отражается в спиралях галактик и бурях на молодых планетах. Её храмы на Страрии строят в виде вращающихся башен, где жрецы вычисляют «моменты равновесия» между разрушением и созиданием.",
        "path_light_shadow": "Путь Светотени",
        "path_light_shadow_title": "Близнецы Света и Тени", # <-- Новый ключ
        "path_light_shadow_desc": "Две грани одного Аэтрала. Люминар наполняет звёзды сиянием, а Ноктюр плетёт чёрные дыры — «врата перерождения». На фресках Нэрадиса их изображают сцепленными руками, образуя кольцо. Легенды Страрии гласят, что их вечный спор рождает смену дня и ночи даже в мирах без солнц.",
        "path_sailyora": "Путь Сайлоры",
        "path_sailyora_title": "Богиня Звёздных Нитей", # <-- Новый ключ
        "path_sailyora_desc": "Её пальцы сплетают магнитные поля и нейтринные реки. Говорят, каждая сверхновая — это узел на её космическом станке. На планетах с кольцами её почитают как покровительницу влюблённых, обменивающихся кольцами из звёздной пыли.",
        "path_gravaan": "Путь Граваана",
        "path_gravaan_title": "Хранитель Гравитационных Узлов", # <-- Новый ключ
        "path_gravaan_desc": "Его тело — сеть из чёрных дыр и тёмной материи. Молятся ему, бросая в пропасти камни с высеченными молитвами: считается, что те, что не достигнут дна, будут подхвачены его незримыми руками.",
        "path_kyriel": "Путь Кириэль",
        "path_kyriel_title": "Стражиха Времени, Та, Что Режет Истории", # <-- Новый ключ
        "path_kyriel_desc": "Её клинок — вспышки гамма-излучений — обрывает линии судеб. На Страрии её культ запрещён, но в подпольных святилищах ей дарят песочные часы, наполненные прахом умерших, веря, что так она продлит участь живых.",
        "path_nerradis_onna": "Путь Нэрадис-Онна",
        "path_nerradis_onna_title": "Дух-Мать Галактики", # <-- Новый ключ
        "path_nerradis_onna_desc": "Её тело — рукава спирали Нэрадис, глаза — скопления сверхновых. Планета Стрария — родинка на её ладони. Шаманы вызывают её дух, танцуя под светом трёх лун, пока тело не покроется узорами, похожими на звёздные карты.",
    },
    "en": {
        "title": "Universe of Relaamo",
        "main_menu": "Main Menu",
        "new_game": "New Game",
        "load_game": "Load Game",
        "settings": "Settings",
        "exit": "Exit",
        "class_selection_title": "Choose Your Path",
        "back": "Back",
        "continue": "Press any key to continue...",
        "settings_title": "Settings",
        "language": "Language",
        "music_volume": "Music Volume",
        "sfx_volume": "SFX Volume",
        "resolution": "Resolution",
        "fullscreen": "Fullscreen Mode",
        "on": "On",
        "off": "Off",
        "selected": "Selected",
        "path_selected": "You have chosen",
        "loading_not_implemented": "Loading function is not yet implemented.",
        "resolution_prompt": "Press Enter to apply",
        "fullscreen_prompt": "Press F to toggle",
        # --- For Character Creation ---
        "enter_name_title": "Enter your character's name",
        "enter_name_placeholder": "Enter hero's name...", # <-- New key
        "confirm": "Confirm",
        "choose_path_title": "{name}, choose your Path",
        "view_path_title": "Path Details",
        "select": "Select",
        "path_description": "Description",
        "path_skills": "Skills",
        "character_created": "Character {name} created! Path: {path}",
        # --- Path Names and Descriptions ---
        "path_relaamon": "Path of Relaamon",
        "path_relaamon_title": "Supreme Weaver, Father-Crystal", # <-- New key
        "path_relaamon_desc": "Not a god, but the very essence of Relaamo, manifested in consciousness. His voice is the hum of energetic vortices, and his body is the structure of the Crystal. He does not interfere in the worlds, but his rhythm sets the laws of being. The sages of Staria believe that meditation on his facet reveals the truth of the universe.",
        "path_vortira": "Path of Vortira",
        "path_vortira_title": "Mother of Chaos and Order, Mistress of Aether Vortices", # <-- New key
        "path_vortira_desc": "Born from the first impulse that struck an aether vortex. Her dual nature is reflected in the spirals of galaxies and storms on young planets. Her temples on Staria are built as rotating towers, where priests calculate the 'moments of equilibrium' between destruction and creation.",
        "path_light_shadow": "Path of Light and Shadow",
        "path_light_shadow_title": "Twins of Light and Shadow", # <-- New key
        "path_light_shadow_desc": "Two facets of one Aetral. Luminar fills the stars with radiance, while Noctur weaves black holes - 'gates of rebirth'. Frescoes on Nerradis depict them clasping hands, forming a ring. Legends of Staria say their eternal strife gives birth to day and night even in sunless worlds.",
        "path_sailyora": "Path of Sailyora",
        "path_sailyora_title": "Goddess of Stellar Threads", # <-- New key
        "path_sailyora_desc": "Her fingers weave magnetic fields and neutrino rivers. They say every supernova is a knot on her cosmic loom. On ringed planets, she is revered as the patroness of lovers exchanging rings made of stardust.",
        "path_gravaan": "Path of Gravaan",
        "path_gravaan_title": "Guardian of Gravitational Nodes", # <-- New key
        "path_gravaan_desc": "His body is a network of black holes and dark matter. Prayers are offered to him by casting stones with engraved prayers into the abyss: it is believed that those that do not reach the bottom will be caught by his unseen hands.",
        "path_kyriel": "Path of Kyriel",
        "path_kyriel_title": "Guardian of Time, She Who Cuts Histories", # <-- New key
        "path_kyriel_desc": "Her blade - bursts of gamma radiation - severs lines of fate. On Staria, her cult is forbidden, but in underground shrines, they give her hourglasses filled with the ashes of the dead, believing that she will thus extend the lives of the living.",
        "path_nerradis_onna": "Path of Nerradis-Onna",
        "path_nerradis_onna_title": "Galaxy Mother Spirit", # <-- New key
        "path_nerradis_onna_desc": "Her body is the arms of the Nerradis spiral, her eyes - clusters of supernovas. The planet Staria is a mole on her palm. Shamans invoke her spirit, dancing under the light of three moons until their bodies are covered with patterns resembling star maps.",
    }
}

def get_text(settings, key):
    """Получает текст на текущем языке."""
    return LOCALIZATION.get(settings.get("language", "ru"), LOCALIZATION["ru"]).get(key, key)
