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
    def test_local_file_returns(self, mock_file_exists, mock_get_from_file):
        result = utils.get_drop_html()
        self.assertEqual(result, 'file content')

    @patch(f'{module}.{fetch_from_file}', return_value='file content')
    @patch(f'{module}.{file_exists}', return_value=True)
    def test_local_file_without_filename_call_no_param(self, mock_file_exists, mock_get_from_file):
        utils.get_drop_html()

        mock_get_from_file.assert_called_once_with('drop.html')

    @patch(f'{module}.{fetch_from_file}', return_value='file content')
    @patch(f'{module}.{file_exists}', return_value=True)
    def test_local_file_with_filename_call_param(self, mock_file_exists, mock_get_from_file):
        utils.get_drop_html('custom_file.html')

        mock_get_from_file.assert_called_once_with('custom_file.html')

    @patch(f'{module}.{save_html_file}')
    @patch(f'{module}.{fetch_from_repo}', return_value='remote repo content')
    def test_no_local_file_filename_not_specified(self, mock_fetch_from_repo, mock_save_to_file):
        with patch('warframe_data_parser.utils.isfile', return_value=False):
            utils.get_drop_html()

            mock_fetch_from_repo.assert_called_once()
            mock_save_to_file.assert_called_once_with(
                'remote repo content', 'drop.html')

    @patch(f'{module}.{save_html_file}')
    @patch(f'{module}.{fetch_from_repo}', return_value='remote repo content')
    def test_no_local_file_filename_specified(self, mock_fetch_from_repo, mock_save_to_file):
        with patch('warframe_data_parser.utils.isfile', return_value=False):
            utils.get_drop_html('custom_filename.html')

            mock_fetch_from_repo.assert_called_once()
            mock_save_to_file.assert_called_once_with(
                'remote repo content', 'custom_filename.html')


class FetchHtmlFromRepo(unittest.TestCase):
    @patch(f'{module}.get')
    def test_get_right_params(self, mock_get):
        mock_get().text = 'Data from repo'
        mock_get.reset_mock()
        result = utils.fetch_html_from_repo()
        mock_get.assert_called()
        self.assertEqual(result, 'Data from repo')

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
