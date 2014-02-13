'''
Global settings module for Color Switch
By @blopker
'''
import sublime
import os

plugin_name = 'ColorSwitch'
FOLDER_REL = os.path.join('Packages', 'User', plugin_name)
FOLDER_THEMES_REL = os.path.join(FOLDER_REL, 'themes')
FOLDER_ABS = None
FOLDER_THEMES_ABS = None

PLUGIN_PREF = 'ColorSwitch.sublime-settings'
SUBLIME_PREF = 'Preferences.sublime-settings'

pluginObj = {}
sublimeObj = {}


def load():
    global FOLDER_ABS, FOLDER_THEMES_ABS
    FOLDER_ABS = os.path.join(sublime.packages_path(), 'User', plugin_name)
    FOLDER_THEMES_ABS = os.path.join(FOLDER_ABS, 'themes')

    global pluginObj
    pluginObj = sublime.load_settings(PLUGIN_PREF)

    global sublimeObj
    sublimeObj = sublime.load_settings(SUBLIME_PREF)

    # In case settings file is missing the debug value.
    debug = pluginObj.get('debug', None)
    if debug is None:
        pluginObj.set('debug', True)


def get(*args):
    return pluginObj.get(*args)


def get_themes_abs():
    return FOLDER_THEMES_ABS


def get_themes_rel():
    return FOLDER_THEMES_REL


def get_color_scheme():
    return sublimeObj.get('color_scheme', '')


def set_color_scheme(path):
    return sublimeObj.set('color_scheme', path)


def save_user():
    sublime.save_settings(SUBLIME_PREF)


def isDebug():
    return get('debug')


def platform():
    return sublime.platform()


def sublime_version():
    return int(sublime.version())
