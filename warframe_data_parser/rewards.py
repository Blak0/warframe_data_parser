class Reward:
    def __init__(
        self,
        name,
        rotation,
        mission_name,
        rarity_type,
        percentage,
        planet,
        mission_type
    ):
        self.name = name
        self.rotation = rotation
        self.mission_name = mission_name
        self.rarity_type = rarity_type
        self.percentage = percentage
        self.planet = planet
        self.mission_type = mission_type

    def __repr__(self):
        return f'{self.percentage} {self.name} | {self.mission_name}/{self.planet} {self.mission_type} {self.rotation}'
