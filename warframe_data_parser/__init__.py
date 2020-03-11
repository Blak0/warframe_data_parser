from bs4 import BeautifulSoup
from . import RewardScrappers as rs
from . import utils


def do_for_all_rewards(callback):
    """
    Given the callable function as a parameter invoke it for each of the rewards
    """
    soup = BeautifulSoup(utils.get_drop_html(), 'lxml')
    rewards = rs.MissionRewardScrapper(soup).get_results()
    for reward in rewards:
        callback(reward)
