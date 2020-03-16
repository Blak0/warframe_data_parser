import unittest

from warframe_data_parser.rows import (
    ItemRow,
    MissionSignatureRow,
    RelicSignatureRow,
    NoneRow,
    RotationRow,
    get_row_class_from_markup,
)


def generate_data_samples(type):
    with open(f'tests/data_samples/{type}_rows.txt', 'r') as f:
        for line in f.readlines():
            yield line


class TestGetRowClassFromMarkup(unittest.TestCase):
    def test_get_class_mission(self):
        markup = '<th colspan="2">Jupiter/Carpo (Caches)</th>'
        row_class = get_row_class_from_markup(markup)
        self.assertIsInstance(row_class(markup), MissionSignatureRow)

    def test_get_class_relic(self):
        markup = '<tr><th colspan="2">Meso R4 Relic (Flawless)(</th></tr>'
        row_class = get_row_class_from_markup(markup)
        self.assertIsInstance(row_class(markup), RelicSignatureRow)

    def test_get_class_item(self):
        markup = "<tr><td>Hell's Chamber</td><td>Rare (6.67%)</td></tr>"
        row_class = get_row_class_from_markup(markup)
        self.assertIsInstance(row_class(markup), ItemRow)

    def test_get_class_rotation(self):
        markup = '<tr><th colspan="2">Rotation A</th></tr>'
        row_class = get_row_class_from_markup(markup)
        self.assertIsInstance(row_class(markup), RotationRow)

    def test_get_class_blank_row(self):
        markup = '<tr class="blank-row"><td class="blank-row" colspan="2"></td></tr>'
        row_class = get_row_class_from_markup(markup)
        self.assertIsInstance(row_class(markup), NoneRow)


class TestMissionSignatureRow(unittest.TestCase):
    def test_get_content(self):
        mission_markup = '<tr><th colspan="2">Mercury/Apollodorus (Survival)</th></tr>'
        mission_row = MissionSignatureRow(mission_markup)

        self.assertEqual(
            mission_row.get_data(),
            ('Mercury', 'Apollodorus', 'Survival'),
            'MissionSignatureRow().get_data() should result in a tuple with data if markup is correct.',
        )

        item_markup = '<tr><td>Arrow Mutation</td><td>Rare (3.76%)</td></tr>'
        mission_row = MissionSignatureRow(item_markup)
        self.assertEqual(mission_row.get_data(), None)

    def test_does_markup_fit(self):
        for mission_markup in generate_data_samples(type='mission'):
            mission_row = MissionSignatureRow(mission_markup)
            self.assertTrue(mission_row.does_markup_fit(),
                            f'{mission_row} should fit to {mission_markup}')

        for item_markup in generate_data_samples(type='item'):
            mission_row = MissionSignatureRow(item_markup)
            self.assertFalse(mission_row.does_markup_fit(),
                             f'{mission_row} should not fit to {item_markup}')


class TestRelicSignatureRow(unittest.TestCase):
    def test_get_content(self):
        relic_markup = '<tr><th colspan="2">Axi A1 Relic (Intact)</th></tr>'
        relic_row = RelicSignatureRow(relic_markup)

        self.assertEqual(relic_row.get_data(), ('Axi', 'A1', 'Intact'))

        mission_markup = '<tr><th colspan="2">Mercury/Apollodorus (Survival)</th></tr>'
        relic_row = RelicSignatureRow(mission_markup)
        self.assertEqual(relic_row.get_data(), None)

    def test_markup_fit(self):
        for relic_markup in generate_data_samples(type='relic'):
            relic_row = RelicSignatureRow(relic_markup)
            self.assertTrue(relic_row.does_markup_fit(),
                            f'{relic_row} should fit to {relic_markup}')

        for mission_markup in generate_data_samples(type='mission'):
            relic_row = RelicSignatureRow(mission_markup)
            self.assertFalse(relic_row.does_markup_fit(),
                             f'{relic_row} should not fit to {mission_markup}')


class TestRotationRow(unittest.TestCase):
    def test_get_content(self):
        rotation_markup = '<tr><th colspan="2">Rotation A</th></tr>'
        rotation_row = RotationRow(rotation_markup)
        self.assertEqual(rotation_row.get_data(), ('Rotation A',))

        mission_markup = '<tr><th colspan="2">Mercury/Apollodorus (Survival)</th></tr>'
        rotation_row = RotationRow(mission_markup)
        self.assertEqual(rotation_row.get_data(), None)

    def test_does_markup_fit(self):
        for rotation_markup in generate_data_samples(type='rotation'):
            rotation_row = RotationRow(rotation_markup)
            self.assertTrue(rotation_row.does_markup_fit(),
                            f'{rotation_row} should fit to {rotation_markup}')

        for mission_markup in generate_data_samples(type='mission'):
            rotation_row = RotationRow(mission_markup)
            self.assertFalse(rotation_row.does_markup_fit(),
                             f'{rotation_row} should not fit to {mission_markup}')


class TestItemRow(unittest.TestCase):
    def test_get_content(self):
        item_markup = "<tr><td>Hell's Chamber</td><td>Rare (6.67%)</td></tr>"
        item_row = ItemRow(item_markup)
        self.assertEqual(item_row.get_data(),
                         ("Hell's Chamber", 'Rare', '6.67%'))

    def test_does_markup_fit(self):
        for item_markup in generate_data_samples(type='item'):
            item_row = ItemRow(item_markup)
            self.assertTrue(item_row.does_markup_fit(),
                            f'{item_row} should fit to {item_markup}')

        for mission_markup in generate_data_samples(type='mission'):
            item_row = ItemRow(mission_markup)
            self.assertFalse(item_row.does_markup_fit(),
                             f'{item_row} should not fit to {mission_markup}')
