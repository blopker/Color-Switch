from . import logger
from . import settings
log = logger.get(__name__)


def init():
    # Load dem settings
    settings.load()
    # Initialize the logger with this package's root name
    logger.init(__name__, settings.get('debug'))
    log.debug('Loaded.')
