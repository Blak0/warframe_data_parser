from functools import partialmethod

from bs4 import BeautifulSoup

from . import utils


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Soup(Borg):
    def get_rows_strings_from_table_id(self, css_id):
        rows = self.soup.select(f'#{css_id} + table > tr')
        return [str(row) for row in rows]

    def set_markup(self, source_string):
        markup = source_string or utils.fetch_html_from_repo()
        self.soup = BeautifulSoup(markup, 'lxml')

    get_mission_rows_strings = partialmethod(
        get_rows_strings_from_table_id,
        css_id='missionRewards'
    )

    get_relic_rows_strings = partialmethod(
        get_rows_strings_from_table_id,
        css_id='relicRewards'
    )
