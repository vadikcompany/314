[app]

# (str) Название твоего приложения
title = Hybrid Chat

# (str) Имя пакета (уникальный ID для Android)
package.name = hybridchat

# (str) Домен пакета (обычно это твой ник или домен наоборот)
package.domain = org.test

# (str) Путь к исходникам (точка означает текущую папку)
source.dir = .

# (list) Расширения файлов, которые нужно включить в APK
source.include_exts = py,png,jpg,kv,atlas

# (str) Версия приложения
version = 0.1

# (list) Зависимости (библиотеки, которые buildozer сам скачает)
# ВАЖНО: для работы сети и уведомлений на Android нужны эти библиотеки
requirements = python3,kivy,plyer

# (str) Ориентация экрана (portrait - вертикально, landscape - горизонтально)
orientation = portrait

# (list) Разрешения Android
# INTERNET — обязательно для работы сокетов
android.permissions = INTERNET, WAKE_LOCK

# (int) API уровень (31 — это Android 12, оптимально для текущих сборок)
android.api = 31

# (int) Минимальная версия Android (21 — это Android 5.0)
android.minapi = 21

# (bool) Использовать ли полноэкранный режим
fullscreen = 0

# (str) Имя главного файла (по умолчанию main.py)
# Если у тебя файл называется по-другому, переименуй его в main.py!

[buildozer]
# (int) Уровень детализации логов (2 — максимально подробно)
log_level = 2

# (str) Папка для хранения скачанных SDK и прочего (не меняй)
bin_dir = ./bin
