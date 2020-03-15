import unittest
from unittest.mock import mock_open, patch

from warframe_data_parser import utils

# for mocking purposes
module = 'warframe_data_parser.utils'
file_exists = 'isfile'
fetch_from_file = 'fetch_html_from_file'
fetch_from_repo = 'fetch_html_from_repo'
save_html_file = 'save_html_to_file'


class TestGetDropHtml(unittest.TestCase):
    @patch(f'{module}.{fetch_from_file}', return_value='file content')
    @patch(f'{module}.{file_exists}', return_value=True)
    def test_local_file_exists(self, mock_file_exists, mock_get_from_file):
        self.assertEqual(utils.get_drop_html(), 'file content')

    @patch(f'{module}.{save_html_file}')
    @patch(f'{module}.{fetch_from_repo}', return_value='remote repo content')
    def test_local_file_doesnt_exist(self, mock_fetch_from_repo, mock_save_to_file):
        with patch('warframe_data_parser.utils.isfile', return_value=False):
            result = utils.get_drop_html()
            self.assertEqual(result, 'remote repo content')
            mock_save_to_file.assert_called_once_with(
                'remote repo content', 'drop.html')

            mock_save_to_file.reset_mock()

            result = utils.get_drop_html('custom_path.html')
            self.assertEqual(result, 'remote repo content')
            mock_save_to_file.assert_called_once_with(
                'remote repo content', 'custom_path.html')


class FetchHtmlFromRepo(unittest.TestCase):
    @patch(f'{module}.get', return_value='content from get')
    def test_get_right_params(self, mock_get):
        result = utils.fetch_html_from_repo()
        mock_get.assert_called_once()
        self.assertEqual(result, mock_get())

        custom_repo = 'https://www.customrepository.com/'
        result = utils.fetch_html_from_repo(custom_repo)
        mock_get.assert_called_with(url=custom_repo)

class FetchHtmlFromFile(unittest.TestCase):
    def test_called_with_right_params(self):
        with patch(f'{module}.open', new=mock_open(read_data='File data')) as mock_openfile:
            utils.fetch_html_from_file('file_to_read.html')
            mock_openfile.assert_called_with('file_to_read.html', 'r')
            mock_openfile().read.assert_called_once_with()

class SaveHtmlFile(unittest.TestCase):
    def test_called_with_right_params(self):
        with patch(f'{module}.open', new=mock_open(read_data='File data')) as mock_openfile:
            utils.save_html_to_file('saved content', 'file_to_write.html')
            mock_openfile.assert_called_with('file_to_write.html', 'w+')
            mock_openfile().write.assert_called_with('saved content')
