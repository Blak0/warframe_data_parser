import unittest
from unittest.mock import patch

from warframe_data_parser import rows_providers as rp


def read_test_table(type):
    with open(f'tests/data_samples/tables/{type}_table.txt', 'r') as f:
        return f.read()


class TestRowProviders(unittest.TestCase):
    def check_output(self, row_provider):
        rows = row_provider.get_rows()
        self.assertGreater(len(rows), 0)
        self.assertIs(type(rows[0]), str)
        self.assertIs(type(rows), list)

    @patch('warframe_data_parser.rows_providers.utils')
    def test_get_mission_rows(self, mock_utils):
        mock_utils.get_drop_html.return_value = read_test_table('mission')
        row_provider = rp.MissionRowsProvider()
        self.check_output(row_provider)

    @patch('warframe_data_parser.rows_providers.utils')
    def test_get_relic_rows(self, mock_utils):
        mock_utils.get_drop_html.return_value = read_test_table('relic')
        row_provider = rp.RelicRowsProvider()
        self.check_output(row_provider)
