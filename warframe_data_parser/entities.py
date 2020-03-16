class MissionReward:
    def __init__(
        self,
        reward_name,
        rotation,
        mission_name,
        rarity_type,
        percentage,
        planet,
        mission_type
    ):
        self.reward_name = reward_name
        self.rotation = rotation
        self.mission_name = mission_name
        self.rarity_type = rarity_type
        self.percentage = percentage
        self.planet = planet
        self.mission_type = mission_type

    def __repr__(self):
        return f'{self.percentage} {self.reward_name} | {self.mission_name}/{self.planet} {self.mission_type} {self.rotation}'


class RelicReward:
    def __init__(
        self,
        relic_type,
        relic_name,
        relic_refinement,
        reward_name,
        rarity_type,
        percentage,
    ):
        self.relic_type = relic_type
        self.relic_name = relic_name
        self.relic_refinement = relic_refinement
        self.reward_name = reward_name
        self.rarity_type = rarity_type
        self.percentage = percentage
