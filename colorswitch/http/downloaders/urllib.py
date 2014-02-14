from .downloader_base import DownloaderBase
from ... import logger
log = logger.get(__name__)
import traceback
import json
from urllib import request, error


try:
    import ssl
    SSL = True
except ImportError:
    SSL = False


def is_available():
    return SSL


class UrllibDownloader(DownloaderBase):
    """Downloader that uses the native Python HTTP library.
    Does not verify HTTPS certificates... """
    def get(self, url):
        try:
            log.debug('Urllib downloader getting url %s', url)
            result = request.urlopen(url)
        except error.URLError as e:
            log.error('Urllib downloader failed: %s' % e.reason)
            traceback.print_exc()
            result = b''
        if result.getcode() >= 400:
            return b''
        return result.read()

    def get_json(self, url):
        a = self.get(url)
        if a:
            try:
                a = json.loads(a.decode('utf-8'))
            except ValueError:
                log.error('URL %s does not contain a JSON file.', url)
                return False
        return a

    def get_file(self, url):
        return self.get(url)
