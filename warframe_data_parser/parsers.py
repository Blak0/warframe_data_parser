from . import rows
from .entities import MissionReward, RelicReward


class RowParser:
    def __init__(self, rows_list):
        self.rows = rows_list

    def get_results_generator(self):
        for row in self.rows:
            reward = self._scrap_reward_from_row(row)
            if reward is not None:
                yield reward

    def get_results(self):
        results = []
        for reward in self.get_results_generator():
            results.append(reward)
        return results

    def _scrap_reward_from_row(self, row_markup):
        row_class = rows.get_row_class_from_markup(row_markup)
        reward = row_class(row_markup).accept(self)
        return reward


class MissionRowParser(RowParser):
    def do_for_mission_signature(self, planet, name, mission_type):
        self.planet = planet
        self.mission_name = name
        self.mission_type = mission_type

    def do_for_item(self, name, rarity_type, percentage):
        self.item_name = name
        self.rarity = rarity_type
        self.percentage = percentage

        return MissionReward(
            reward_name=self.item_name,
            rotation=self.rotation,
            mission_name=self.mission_name,
            rarity_type=self.rarity,
            percentage=self.percentage,
            planet=self.planet,
            mission_type=self.mission_type,
        )

    def do_for_rotation(self, rotation):
        self.rotation = rotation


class RelicRowParser(RowParser):
    def do_for_relic_signature(self, kind, name, refinement):
        self.relic_type = kind
        self.relic_name = name
        self.refinement = refinement

    def do_for_item(self, name, rarity_type, percentage):
        self.item_name = name
        self.rarity = rarity_type
        self.percentage = percentage

        return RelicReward(
            relic_type=self.relic_type,
            relic_name=self.relic_name,
            relic_refinement=self.refinement,
            reward_name=self.item_name,
            rarity_type=self.rarity,
            percentage=self.percentage,
        )