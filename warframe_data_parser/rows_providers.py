from abc import ABC, abstractmethod

from .soup import get_row_strings_from_table_id


class BaseRowsProvider(ABC):
    def _get_row_strings_from_id(self, table_id):
        return get_row_strings_from_table_id(table_id)
        

    @abstractmethod
    def get_rows(self):
        """Should invoke _get_rows_from_id with proper parameters"""


class MissionRowsProvider(BaseRowsProvider):
    def get_rows(self):
        return self._get_row_strings_from_id('missionRewards')


class RelicRowsProvider(BaseRowsProvider):
    def get_rows(self):
        return self._get_row_strings_from_id('relicRewards')
