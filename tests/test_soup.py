import unittest
from unittest.mock import patch

from warframe_data_parser.soup import Soup


class TestSoup(unittest.TestCase):
    def test_is_borg(self):
        s1 = Soup()
        s2 = Soup()
        self.assertIs(s1.soup, s2.soup)

    def returns_row_lists(self, func):
        rows = func()
        return rows == ['<tr>Row1</tr>', '<tr>Row2</tr>']

    @patch('warframe_data_parser.soup.utils.fetch_html_from_repo')
    def test_get_mission_rows(self, mock_fetch_html):
        soup = Soup()
        soup.set_markup(lambda: '<h3 id="missionRewards"></h3><table><tr>Row1</tr><tr>Row2</tr></table>')
        returns_rows = self.returns_row_lists(soup.get_mission_rows_strings)
        self.assertTrue(returns_rows)

    @patch('warframe_data_parser.soup.utils.fetch_html_from_repo')
    def test_get_relic_rows(self, mock_fetch_html):
        soup = Soup()
        soup.set_markup(lambda: '<h3 id="relicRewards"></h3><table><tr>Row1</tr><tr>Row2</tr></table>')
        returns_rows = self.returns_row_lists(soup.get_relic_rows_strings)
        self.assertTrue(returns_rows)
