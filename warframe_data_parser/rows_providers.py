from abc import ABC, abstractmethod

from . import utils

from bs4 import BeautifulSoup


soup = BeautifulSoup(utils.fetch_html_from_repo(), 'lxml')


class BaseRowsProvider(ABC):
    def _get_rows_from_id(self, table_id):
        row_tags = soup.select(f'#{table_id} + table > tr')
        return [str(x) for x in row_tags]

    @abstractmethod
    def get_rows(self):
        """Should invoke _get_rows_from_id with proper parameters"""


class MissionRowsProvider(BaseRowsProvider):
    def get_rows(self):
        return self._get_rows_from_id('missionRewards')


class RelicRowsProvider(BaseRowsProvider):
    def get_rows(self):
        return self._get_rows_from_id('relicRewards')
