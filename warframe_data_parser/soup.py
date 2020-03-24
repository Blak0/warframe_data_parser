"""
This module implements the singleton as a module.

This is useful because creating the beautifulsoup object
is resource heavy and it makes sense to create one and share it
between several objects.
"""
from bs4 import BeautifulSoup

from . import utils


soup = BeautifulSoup(utils.fetch_html_from_repo(), 'lxml')


def get_row_strings_from_table_id(table_id):
    rows = soup.select(f'#{table_id} + table > tr')
    return [str(row) for row in rows]
