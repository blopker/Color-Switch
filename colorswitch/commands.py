'''
Collection of functions the plugin can invoke. Most if not all should be
non-blocking (@async) functions to keep the main UI thread from freezing.

These functions should catch all unexpected exceptions so the plugin does not
have to. Unexpected exceptions should return False. Expected exceptions should
be caught by other modules this module uses. Log all unusual behavior.

All @async functions have an optional callback parameter as the last argument.
'''

from . import logger
log = logger.get(__name__)
from . import settings
from . import http
from . import io
from .async import async
from .repository import Theme, Themes


def get_current_theme():
    current_path = settings.get_color_scheme()
    return Theme(file_path=current_path)


@async
def fetch_theme_list():
    urls = settings.get('repos', [])
    themes = []
    for url in urls:
        if url[-1] == '/':
            url = url[:-1]
        json = http.get_json(url + '/themes.json')
        themes += [Theme.from_repo(j, url) for j in json]
    return Themes(themes)


@async
def get_theme(theme):
    return _get_theme(theme)


def _get_theme(theme):
    theme.file_path = io.get_theme_path(theme.file_name)
    if theme.file_path:
        return theme

    data = http.get_file(theme.url)

    if not data:
        return theme

    # Sanity check
    if '<plist version=' not in str(data):
        return theme

    theme.file_path = io.save_theme(data, theme.file_name)
    return theme


def set_theme(theme, commit=False):
    settings.set_color_scheme(theme.file_path)
    if commit:
        settings.save_user()


@async
def install_theme(theme):
    theme = _get_theme(theme)
    if theme.file_path is None:
        return None
    set_theme(theme, commit=True)
    return theme
