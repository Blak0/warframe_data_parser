import unittest
from unittest.mock import mock_open, patch

from warframe_data_parser import utils


class FetchHtmlFromRepo(unittest.TestCase):
    @patch('warframe_data_parser.utils.get')
    def test_get_right_params(self, mock_get):
        mock_get().text = 'Data from repo'
        mock_get.reset_mock()
        result = utils.fetch_html_from_repo()
        mock_get.assert_called_once()

        self.assertEqual(result, 'Data from repo')

    @patch('warframe_data_parser.utils.get')
    def test_default_url(self, mock_get):
        custom_repo = 'https://www.customrepository.com/'
        result = utils.fetch_html_from_repo(custom_repo)
        mock_get.assert_called_once_with(url=custom_repo)
