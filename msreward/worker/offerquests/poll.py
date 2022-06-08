import random
import time

from selenium.webdriver.common.by import By

from .offerquestbase import OfferQuestBase


class Poll(OfferQuestBase):
    def __init__(self, browser):
        super().__init__(browser, 'Poll', 'btoption0', By.ID)

    def _do_quest(self):
        # click poll option
        choices = ['btoption0', 'btoption1']
        self._browser.click_element(By.ID, random.choice(choices))
        time.sleep(1)