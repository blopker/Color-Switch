from .downloader_base import DownloaderBase
from ... import logger
log = logger.get(__name__)
import traceback
import subprocess
import json
import shutil


def is_available():
    if shutil.which('wget'):
        return True
    return False


class WgetDownloader(DownloaderBase):
    """Downloader that uses the command line program wget."""
    def get(self, url):
        try:
            log.debug('Wget downloader getting url %s', url)
            result = subprocess.check_output(['wget', '-qO-', url])
        except subprocess.CalledProcessError:
            log.error('Wget downloader failed.')
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
