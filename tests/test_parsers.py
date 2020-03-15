import unittest
from unittest.mock import MagicMock, patch

from warframe_data_parser.parsers import MissionRowParser
from warframe_data_parser.rewards import Reward


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
        with patch.object(Reward, '__init__', return_value=None) as mock_constructor:
            rewards = row_parser.get_results()
            mock_constructor.assert_called()

        # Assert if there are two rewards
        rewards = row_parser.get_results()
        self.assertEqual(len(rewards), 2)

        #Assert if it returns Reward objects
        first, second = rewards
        
        self.assertIsInstance(first, Reward)
        self.assertIsInstance(second, Reward)
