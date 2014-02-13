'''
Module to determine the correct downloader to use.
By @blopker
'''
from . import requests, wget, curl
from ... import logger
log = logger.get(__name__)


def get():
    if curl.is_available():
        log.debug('Using Curl downloader.')
        return curl.CurlDownloader()
    if wget.is_available():
        log.debug('Using WGET downloader.')
        return wget.WgetDownloader()
    log.debug('Using Requests downloader.')
    return requests.RequestsDownloader()
