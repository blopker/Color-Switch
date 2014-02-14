'''
Module to determine the correct downloader to use.
'''
from . import urllib, wget, curl
from ... import logger
log = logger.get(__name__)


def get():
    if curl.is_available():
        log.debug('Using Curl downloader.')
        return curl.CurlDownloader()
    if wget.is_available():
        log.debug('Using WGET downloader.')
        return wget.WgetDownloader()
    if urllib.is_available():
        log.debug('Using Urllib downloader.')
        return urllib.UrllibDownloader()
    log.error('No usable downloader found. Your platform is not supported.')
    return None
