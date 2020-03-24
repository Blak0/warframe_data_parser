import unittest
from unittest.mock import patch

from warframe_data_parser import rows_providers as rp


class TestRowProviders(unittest.TestCase):
    @patch('warframe_data_parser.rows_providers.get_row_strings_from_table_id')
    def test_get_mission_rows(self, mock_get_row_strings):
        row_provider = rp.MissionRowsProvider()
        row_provider.get_rows()
        mock_get_row_strings.assert_called_once_with('missionRewards')

    @patch('warframe_data_parser.rows_providers.get_row_strings_from_table_id')
    def test_get_relic_rows(self, mock_get_row_strings):
        row_provider = rp.RelicRowsProvider()
        row_provider.get_rows()
        mock_get_row_strings.assert_called_once_with('relicRewards')
