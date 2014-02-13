from .colorswitch import commands
from .colorswitch import status
from . import colorswitch
import sublime_plugin

NO_SELECTION = -1


class ColorSwitchInstallSchemeCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('Running install command.')
        self.theme_status = {}
        self.status = status.loading('Getting scheme list')
        self.original_theme = commands.get_current_theme()
        commands.fetch_theme_list(self.display_list)

    def display_list(self, themes):
        self.status.stop()
        if not themes:
            status.error('Scheme list not found. Please check internet ' +
                         'connection or enable debug in the settings and ' +
                         'report the stack traces.')
            return
        self.themes = themes
        self.window.show_quick_panel(themes.quick_list(),
                                     self.on_select,
                                     on_highlight=self.on_highlighted)

    def on_highlighted(self, theme_index):
        theme = self.themes[theme_index]
        self.theme_status[theme.name] = status.loading('Downloading scheme %s' % theme.name)
        self.current_theme = theme
        commands.get_theme(self.themes[theme_index], self.on_get)

    def on_get(self, theme):
        self.theme_status[theme.name].stop()
        if not theme.file_path:
            status.error('Scheme %s download failed.' % theme.name)
            return
        # Don't set if user has moved on already
        if theme.file_name == self.current_theme.file_name:
            status.message('Showing scheme %s.' % theme.name)
            commands.set_theme(theme)

    def on_select(self, theme_index):
        if theme_index is NO_SELECTION:
            commands.set_theme(self.original_theme)
            status.message('Scheme install canceled.')
            return
        theme = self.themes[theme_index]
        status.message('Installing scheme: %s' % theme)
        commands.install_theme(theme, self.install_done)

    def install_done(self, theme):
        self.status.stop()

        if theme is None:
            commands.set_theme(self.original_theme)
            status.error('Scheme install was unsuccessful. Please check console.')
            return

        commands.set_theme(theme)
        status.message('Scheme installed successfully!')


def plugin_loaded():
    colorswitch.init()
