"""
This module implements the singleton as a module.

This is useful because creating the beaufitulsoup object
is resource heavy and it makes sense to create one and share it
between several objects.
"""
from bs4 import BeautifulSoup

from . import utils


soup = BeautifulSoup(utils.fetch_html_from_repo(), 'lxml')
