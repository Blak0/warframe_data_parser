from bs4 import BeautifulSoup

from . import utils


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Soup(Borg):
    def __init__(self):
        super().__init__()
        if 'soup' not in self.__dict__:
            self.soup = BeautifulSoup(utils.fetch_html_from_repo(), 'lxml')

    def get_row_strings_from_table_id(self, table_id):
        rows = self.soup.select(f'#{table_id} + table > tr')
        return [str(row) for row in rows]
