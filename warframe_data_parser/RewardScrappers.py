from abc import ABC, abstractmethod
import re

from bs4 import BeautifulSoup

from .rewards import Reward


class AbstractRewardScrapper(ABC):
    def __init__(self, soup):
        self.soup = soup
        self.rows = self.soup.select(f'#{self.source_table_id} + table > tr')

    @property
    @abstractmethod
    def source_table_id(self):
        """
        Css id for the table containing parse data
        """
        raise NotImplementedError

    @abstractmethod
    def get_results(self):
        """
        Abstract operation resulting in an array of some kind of rewards
        """
        raise NotImplementedError


class MissionRewardScrapper(AbstractRewardScrapper):
    @property
    def source_table_id(self):
        return 'missionRewards'

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

    def _scrap_reward_from_row(self, row):
        row_text = str(row)
        if self._should_row_be_ignored(row):
            return

        self._set_mission_details(row_text)
        self._set_rotation_details(row_text)
        if self._set_reward_details(row):
            return Reward(
                name=self.reward_name,
                rotation=self.rotation,
                mission_name=self.mission_name,
                rarity_type=self.rarity,
                percentage=self.percentage,
                planet=self.planet,
                mission_type=self.mission_type,
            )

    def _should_row_be_ignored(self, row):
        if 'Conclave' in str(row) or 'Index' in str(row):
            return True  # who tf cares lol
        if self._is_blank_row(row):
            return True
        return False

    def _is_blank_row(self, row):
        return row.select('.blank-row')

    def _set_reward_details(self, row):
        """
        Returns True if pattern is found and properties are assigned
        Does nothing if row doesnt contain item data
        """
        if len(row.find_all('td')) == 2:
            rarity_td, percent_td = row.find_all('td')
            self.reward_name = rarity_td.text
            self._set_item_percentage_and_rarity(percent_td.text)
            return True

    def _set_mission_details(self, text):
        """
        "(...) Veil/Flexa (Caches) (...)" -> ("Veil", "Flexa", "Caches")
        Returns True if pattern is found and properties are assigned
        """
        planet = r'([a-zA-Z]+)'
        name = r'([\w -\']+)'
        kind = r'\((\D+)\)'

        pattern = rf'{planet}/{name} {kind}'
        match = re.search(pattern, text)

        if match:
            self.planet, self.mission_name, self.mission_type = match.groups()
            return True

    def _set_rotation_details(self, text):
        """
        "(...) Rotation B (...)" -> "Rotation B"
        Returns True if pattern is found and properties are assigned
        """
        pattern = r'(Rotation .){1}'
        match = re.search(pattern, text)
        if match:
            self.rotation = match.group(0)
            return True

    def _set_item_percentage_and_rarity(self, text):
        """
        "(...) Common (21.37%) (...) -> ("Common", "21.37%")
        Returns True if pattern is found and properties are assigned
        """
        rarity = r'([a-zA-Z]+)'
        percentage = r'(\d*\.\d*%)'
        pattern = rf'{rarity} \({percentage}\)'
        match = re.search(pattern, text)
        if match:
            self.rarity, self.percentage = match.groups()
            return True
