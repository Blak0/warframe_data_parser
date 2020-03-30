import unittest
from unittest.mock import patch

from warframe_data_parser import exceptions, parsers


class TestGetParserClass(unittest.TestCase):
    def test_raises_exception(self):
        with self.assertRaises(exceptions.ParserNotFoundError):
            parsers.get_parser_class('nonexistent')

    def test_get_mission_class(self):
        parser_class = parsers.get_parser_class('mission')
        self.assertIs(parser_class, parsers.MissionRowParser)

    def test_get_relic_class(self):
        parser_class = parsers.get_parser_class('relic')
        self.assertIs(parser_class, parsers.RelicRowParser)


class TestMissionRowParser(unittest.TestCase):
    @patch('warframe_data_parser.parsers.soup.Soup')
    def test_get_results(self, mock_soup):
        test_rows = [
            '<th colspan="2">Mercury/Apollodorus (Survival)</th>',
            '<th colspan="2">Rotation A<th>',
            "<tr><td>Hell's Chamber</td><td>Rare (6.67%)</td></tr>",
            "<td>400X Alloy Plate</td><td>Uncommon (12.65%)</td>",
        ]
        mock_soup().get_mission_rows_strings.return_value = test_rows

        row_parser = parsers.MissionRowParser()
        rewards = row_parser.get_results()

        self.assertEqual(len(rewards), 2)

        first, second, *_ = rewards

        self.assertIsInstance(first, parsers.MissionReward)
        self.assertIsInstance(second, parsers.MissionReward)


class TestRelicRowParser(unittest.TestCase):
    @patch('warframe_data_parser.parsers.soup.Soup')
    def test_get_results(self, mock_soup):
        test_rows = [
            '<tr><th colspan="2">Lith M1 Relic (Exceptional)</th></tr>',
            '<tr><td>Mag Prime Blueprint</td><td>Rare (4.00%)</td></tr>',
            '<tr><td>Lex Prime Receiver</td><td>Uncommon (23.33%)</td></tr>',
            '<tr><td>Soma Prime Blueprint</td><td>Uncommon (13.00%)</td></tr>',
            '<tr><td>Dakra Prime Blueprint</td><td>Uncommon (13.00%)</td></tr>',
        ]
        mock_soup().get_relic_rows_strings.return_value = test_rows

        row_parser = parsers.RelicRowParser()
        rewards = row_parser.get_results()

        for reward in rewards:
            self.assertIsInstance(reward, parsers.RelicReward)
        self.assertEqual(len(rewards), 4)
