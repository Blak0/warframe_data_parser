from os import path


DROP_REPO = 'https://www.warframe.com/repos/hnfvc0o3jnfvc873njb03enrf56.html'


def get_drop_html():
    if not path.exists('../data.html'):
        from requests import get
        req = get(url=DROP_REPO)
        with open('data.html', 'w+') as f:
            f.write(req.text)
            return req.text
    else:
        with open('data.html', 'r') as f:
            return f.read()
