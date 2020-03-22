from functools import lru_cache
from os.path import isfile

from requests import get

DROP_REPO = 'https://www.warframe.com/repos/hnfvc0o3jnfvc873njb03enrf56.html'


@lru_cache(maxsize=1)
def fetch_html_from_repo(drop_repo=DROP_REPO):
    """
    Get Warframe's official droprate repository html.

    To not strain the server too much this utility function caches
    downloaded html data. For this reason if you need to get the most recent
    version of repo, call the get_drop_html.cache_clear()
    """
    return get(url=drop_repo).text
