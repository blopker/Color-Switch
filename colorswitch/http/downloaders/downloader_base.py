from abc import ABCMeta, abstractmethod


class DownloaderBase(object, metaclass=ABCMeta):
    """Abstract base class for downloaders. Downloaders must implement these
    methods."""
    @abstractmethod
    def get(self, url):
        '''Get raw content from URL'''
        raise NotImplementedError()

    @abstractmethod
    def get_json(self, url):
        '''Get a JSON object from a URL'''
        raise NotImplementedError()

    @abstractmethod
    def get_file(self, url):
        '''Get a binary file from a URL'''
        raise NotImplementedError()
