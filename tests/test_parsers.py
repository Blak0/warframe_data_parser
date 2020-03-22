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
    def test_get_results(self):
        test_rows = [
            '<th colspan="2">Mercury/Apollodorus (Survival)</th>',
            '<th colspan="2">Rotation A<th>',
            "<tr><td>Hell's Chamber</td><td>Rare (6.67%)</td></tr>",
            "<td>400X Alloy Plate</td><td>Uncommon (12.65%)</td>",
        ]
        row_parser = parsers.MissionRowParser()

        with patch.object(row_parser, '_get_rows_from_provider', return_value=test_rows):
            rewards = row_parser.get_results()
            self.assertEqual(len(rewards), 2)

            first, second = rewards
            self.assertIsInstance(first, parsers.MissionReward)
            self.assertIsInstance(second, parsers.MissionReward)

    def test_has_proper_provider(self):
        row_parser = parsers.MissionRowParser()
        assert hasattr(row_parser._get_rows_provider(), 'get_rows')


class TestRelicRowParser(unittest.TestCase):
    def test_get_results(self):
        test_rows = [
            '<tr><th colspan="2">Lith M1 Relic (Exceptional)</th></tr>',
            '<tr><td>Mag Prime Blueprint</td><td>Rare (4.00%)</td></tr>',
            '<tr><td>Lex Prime Receiver</td><td>Uncommon (23.33%)</td></tr>',
            '<tr><td>Soma Prime Blueprint</td><td>Uncommon (13.00%)</td></tr>',
            '<tr><td>Dakra Prime Blueprint</td><td>Uncommon (13.00%)</td></tr>',
        ]

        row_parser = parsers.RelicRowParser()

        with patch.object(row_parser, '_get_rows_from_provider', return_value=test_rows):
            rewards = row_parser.get_results()
            for reward in rewards:
                self.assertIsInstance(reward, parsers.RelicReward)

        self.assertEqual(len(rewards), 4)

    def test_has_proper_provider(self):
        row_parser = parsers.RelicRowParser()
        assert hasattr(row_parser._get_rows_provider(), 'get_rows')
