from functools import partialmethod

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
            self.set_markup()

    def get_rows_strings_from_table_id(self, css_id):
        rows = self.soup.select(f'#{css_id} + table > tr')
        return [str(row) for row in rows]

    def set_markup(self, source_callable=utils.fetch_html_from_repo):
        self.soup = BeautifulSoup(source_callable(), 'lxml')

    get_mission_rows_strings = partialmethod(
        get_rows_strings_from_table_id,
        css_id='missionRewards'
    )

    get_relic_rows_strings = partialmethod(
        get_rows_strings_from_table_id,
        css_id='relicRewards'
    )
