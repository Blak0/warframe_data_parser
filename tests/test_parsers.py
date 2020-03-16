import unittest
from unittest.mock import MagicMock, patch

from warframe_data_parser.parsers import MissionRowParser, RelicRowParser
from warframe_data_parser.entities import MissionReward, RelicReward


class TestMissionRowParser(unittest.TestCase):
    def test_get_results(self):
        test_rows = [
            '<th colspan="2">Mercury/Apollodorus (Survival)</th>',
            '<th colspan="2">Rotation A<th>',
            "<tr><td>Hell's Chamber</td><td>Rare (6.67%)</td></tr>",
            "<td>400X Alloy Plate</td><td>Uncommon (12.65%)</td>",
        ]

        # Assert if reward is constructed in the process
        row_parser = MissionRowParser(test_rows)
        with patch.object(MissionReward, '__init__', return_value=None) as mock_constructor:
            rewards = row_parser.get_results()
            mock_constructor.assert_called()

        # Assert if there are two rewards
        rewards = row_parser.get_results()
        self.assertEqual(len(rewards), 2)

        #Assert if it returns Reward objects
        first, second = rewards
        
        self.assertIsInstance(first, MissionReward)
        self.assertIsInstance(second, MissionReward)


class TestRelicRowParser(unittest.TestCase):
    def test_get_results(self):
        test_rows = [
            '<tr><th colspan="2">Lith M1 Relic (Exceptional)</th></tr>',
            '<tr><td>Mag Prime Blueprint</td><td>Rare (4.00%)</td></tr>',
            '<tr><td>Lex Prime Receiver</td><td>Uncommon (23.33%)</td></tr>',
            '<tr><td>Soma Prime Blueprint</td><td>Uncommon (13.00%)</td></tr>',
            '<tr><td>Dakra Prime Blueprint</td><td>Uncommon (13.00%)</td></tr>',
        ]
        
        row_parser = RelicRowParser(test_rows)
        with patch.object(RelicReward, '__init__', return_value=None) as mock_constructor:
                rewards = row_parser.get_results()
                mock_constructor.assert_called()

        rewards = row_parser.get_results()

        for reward in rewards:
            self.assertIsInstance(reward, RelicReward)

        self.assertEqual(len(rewards), 4)

