'''
Module to set the view status of Sublime Text plugins.
By @blopker
'''

from .lib.concurrent import futures
from . import logger
log = logger.get(__name__)
import time
import sublime

statusPool = futures.ThreadPoolExecutor(max_workers=1)
PLUGIN_NAME = 'Color Switch'
# Default status display time in seconds
TIMEOUT = 10
current_message = None


def message(msg, seconds=TIMEOUT):
    log.info(msg)

    global current_message
    if current_message is not None:
        current_message.stop()

    current_message = Message(msg, seconds)
    return current_message


def error(msg, seconds=TIMEOUT):
    log.error(msg)
    msg = 'ERROR: ' + msg
    message(msg)
    return current_message


def loading(msg, seconds=TIMEOUT):
    # longer time out for loading cus it could be a while.
    return Loader(msg, seconds*2)


class Message(object):
    '''Class to start and cancel the status message.
    Call stop() on this object to remove the message.'''
    def __init__(self, message, timeout):
        self.message = message
        self.running = True
        self.timeout = timeout
        self.start_time = time.time()
        self.msg_id = self._get_id(message)
        statusPool.submit(self._show_message)

    def _get_current_view(self):
        window = sublime.active_window()
        view = window.active_view()
        return view

    def _append_plugin_name(self, msg):
        return '%s: %s' % (PLUGIN_NAME, msg)

    def _get_id(self, msg):
        return msg + str(time.time())

    def _update_timer(self):
        elapsed = time.time() - self.start_time
        if elapsed > self.timeout:
            self.stop()

    def _show_message(self):
        view = self._get_current_view()
        while self.running:
            msg = self._get_message()
            stat = self._append_plugin_name(msg)
            view.set_status(self.msg_id, stat)
            time.sleep(.1)
            self._update_timer()
        view.erase_status(self.msg_id)

    def _get_message(self):
        return self.message

    def stop(self):
        self.running = False


class Loader(Message):
    def _get_message(self):
        pos = getattr(self, 'pos', 0)
        loadingChars = '⣾⣽⣻⢿⡿⣟⣯⣷'
        msg = self.message + ' [' + loadingChars[pos] + ']'
        self.pos = (pos + 3) % len(loadingChars)
        return msg

    def stop(self):
        self.running = False
