from functools import lru_cache
from os.path import isfile

from requests import get


DROP_REPO = 'https://www.warframe.com/repos/hnfvc0o3jnfvc873njb03enrf56.html'


def fetch_html_from_repo(drop_repo=DROP_REPO):
    """
    Get Warframe's official droprate repository html.
    """
    return get(url=drop_repo).text
