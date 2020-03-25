from abc import ABC, abstractmethod

from .soup import Soup


class BaseRowsProvider(ABC):
    def _get_row_strings_from_id(self, table_id):
        return Soup().get_row_strings_from_table_id(table_id)

    @abstractmethod
    def get_rows(self):
        """Should invoke _get_rows_from_id with proper parameters"""


class MissionRowsProvider(BaseRowsProvider):
    def get_rows(self):
        return self._get_row_strings_from_id('missionRewards')


class RelicRowsProvider(BaseRowsProvider):
    def get_rows(self):
        return self._get_row_strings_from_id('relicRewards')

class NoneRowsProvider(BaseRowsProvider):
    def get_rows(self):
        """This null object can only represent its interface for template method in baseclass"""