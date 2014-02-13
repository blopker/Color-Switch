'''
Abstraction for the HTTP layer.
By @blopker
'''
from .cache import cache
from . import downloaders
from .. import logger
log = logger.get(__name__)
import sys
import traceback

downloader = downloaders.get()


@cache
def get(url):
    return _run_downloader(downloader.get, url)


@cache
def get_json(url):
    return _run_downloader(downloader.get_json, url)


@cache
def get_file(url):
    return _run_downloader(downloader.get_file, url)


def _run_downloader(fn, url):
    try:
        log.debug('HTTP url %s with function %s', url, fn.__name__)
        return fn(url)
    except NotImplementedError:
        log.error('Function %s not implemented in downloader %s.',
                  fn.__name__, downloader.__class__.__name__)
    except AttributeError as e:
        log.error(e)
        traceback.print_exc()
    except:
        log.error('Unexpected exception: %s', sys.exc_info()[0])
        traceback.print_exc()
    return False
