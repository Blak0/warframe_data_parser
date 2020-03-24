import unittest

from warframe_data_parser import soup


class TestSoup(unittest.TestCase):
    def test_get_rows_from_table_id(self):
        rows = soup.get_row_strings_from_table_id('missionRewards')
        self.assertGreater(len(rows), 0)
        self.assertIs(type(rows[0]), str)
        self.assertIs(type(rows), list)