from .. import settings
import time


def cache(fn):
    ''' A decorator to cache method invocation.
    Cache expires after a set time.
    '''
    cacheDB = {}

    def putCache(args, ans):
        # Disable cache for debug.
        if settings.isDebug():
            return

        if ans:
            cacheDB[args] = (time.time(), ans)

    def getCache(args):
        # Disable cache for debug.
        if settings.isDebug():
            return False

        # Get result while cleaning old cache.
        t = time.time()
        cache_time = settings.get('cache_time', 0)
        ans = False
        for c in cacheDB:
            age = t - cacheDB[c][0]
            if age > cache_time:
                del cacheDB[c]
                continue
            if c == args:
                ans = cacheDB[args][1]
        return ans

    def wrap(*args):
        ans = getCache(args)
        if ans is False:
            ans = fn(*args)
            putCache(args, ans)
        return ans
    return wrap
