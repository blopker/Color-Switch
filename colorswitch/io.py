from . import settings
import os


def _check_folders_exist():
    folder = settings.get_themes_abs()
    if not os.path.exists(folder):
        os.makedirs(folder)


def save_theme(data, file_name):
    _check_folders_exist()
    themes_dir = settings.get_themes_abs()
    theme_path = os.path.join(themes_dir, file_name)
    with open(theme_path, 'wb') as f:
        f.write(data)
    file_path = settings.get_themes_rel() + '/' + file_name
    return file_path


def get_theme_path(file_name):
    _check_folders_exist()
    themes_dir = settings.get_themes_abs()
    p = os.path.join(themes_dir, file_name)
    if os.path.exists(p):
        return settings.get_themes_rel() + '/' + file_name
    return None
