from os.path import isfile

from requests import get


DROP_REPO = 'https://www.warframe.com/repos/hnfvc0o3jnfvc873njb03enrf56.html'


def get_drop_html(file_name='drop.html'):
    """
    Get Warframe's official droprate repository html.

    To not strain the server too much this utility function saves
    html data as file with specified as parameter or default name
    and uses it next time its called.
    """
    if isfile(file_name):
        return fetch_html_from_file(file_name)
    else:
        drop_html = fetch_html_from_repo()
        save_html_to_file(drop_html, file_name)
        return drop_html


def fetch_html_from_repo(drop_repo=DROP_REPO):
    return get(url=drop_repo).text


def fetch_html_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def save_html_to_file(content, file_name):
    with open(file_name, 'w+') as f:
        f.write(content)
