import unittest

from warframe_data_parser.soup import Soup


class TestSoup(unittest.TestCase):
    def test_is_borg(self):
        s1 = Soup()
        s2 = Soup()
        self.assertIs(s1.soup, s2.soup)

    def test_get_rows_from_table_id(self):
        rows = Soup().get_row_strings_from_table_id('missionRewards')
        self.assertGreater(len(rows), 0)
        self.assertIs(type(rows[0]), str)
        self.assertIs(type(rows), list)
