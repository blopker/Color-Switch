from .downloader_base import DownloaderBase
from ... import logger
log = logger.get(__name__)
import traceback
import subprocess
import json
import shutil


def is_available():
    if shutil.which('curl'):
        return True
    return False


class CurlDownloader(DownloaderBase):
    """Downloader that uses the command line program curl."""
    def get(self, url):
        try:
            log.debug('Curl downloader getting url %s', url)
            result = subprocess.check_output(['curl', '--fail', url])
        except subprocess.CalledProcessError:
            log.error('Curl downloader failed.')
            traceback.print_exc()
            result = False
        return result

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
