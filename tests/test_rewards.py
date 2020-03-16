import unittest

from warframe_data_parser import entities


class TestMissionReward(unittest.TestCase):
    def setUp(self):
        self.reward = entities.MissionReward(
            'Item name',
            'Rotation',
            'Mission name',
            'Rarity string',
            'Rarity in percentage',
            'Planet',
            'Mission type',
        )

    def test_repr(self):
        reward_to_string = 'Rarity in percentage Item name | Mission name/Planet Mission type Rotation'
        self.assertEqual(str(self.reward), reward_to_string)
