from .downloader_base import DownloaderBase
from ...lib import requests as req
from ... import logger
log = logger.get(__name__)
import traceback


class RequestsDownloader(DownloaderBase):
    """Downloader that uses the Requests library."""
    def get(self, url):
        try:
            log.debug('Requests downloader getting url %s', url)
            return req.get(url)
        except TypeError:
            log.error('This platform does not support SSL with the Requests downloader.')
            traceback.print_exc()
        return False

    def get_json(self, url):
        a = self.get(url)
        if a:
            try:
                a = a.json()
            except ValueError:
                log.error('URL %s does not contain a JSON file.', url)
                return False
        return a

    def get_file(self, url):
        a = self.get(url)
        if a:
            a = a.content
        return a
