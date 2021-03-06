import unittest
from unittest.mock import patch

from warframe_data_parser.soup import Soup


class TestSoup(unittest.TestCase):
    def setUp(self):
        # because Soup is a borg we need to set it to predictable state
        # and then test it
        self.soup = Soup()
        self.soup.set_markup('any markup')

    @patch('warframe_data_parser.soup.utils.fetch_html_from_repo')
    def test_is_borg(self, mock_fetch_html):
        s1 = Soup()
        s1.set_markup('markup')
        s2 = Soup()
        s2.set_markup('new markup')
        self.assertIs(s1._soup, s2._soup)

    def returns_row_lists(self, func):
        rows = func()
        return rows == ['<tr>Row1</tr>', '<tr>Row2</tr>']

    @patch('warframe_data_parser.soup.utils.fetch_html_from_repo')
    def test_get_mission_rows(self, mock_fetch_html):
        self.soup.set_markup('<h3 id="missionRewards"></h3><table><tr>Row1</tr><tr>Row2</tr></table>')
        returns_rows = self.returns_row_lists(self.soup.get_mission_rows_strings)
        self.assertTrue(returns_rows)

    @patch('warframe_data_parser.soup.utils.fetch_html_from_repo')
    def test_get_relic_rows(self, mock_fetch_html):
        self.soup.set_markup('<h3 id="relicRewards"></h3><table><tr>Row1</tr><tr>Row2</tr></table>')
        returns_rows = self.returns_row_lists(self.soup.get_relic_rows_strings)
        self.assertTrue(returns_rows)
