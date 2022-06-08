import logging
import random
import time

from selenium.webdriver.common.by import By

from ..offerquestbase import OfferQuestBase

class ClickQuiz(OfferQuestBase):
    def __init__(self, browser):
        super().__init__(browser, 'Click Quiz', 'wk_Circle', By.CLASS_NAME)

    def _do_quest(self):
        while True:
            if self._browser.find_elements(By.CSS_SELECTOR, '.cico.btCloseBack'):
                self._browser.find_elements(By.CSS_SELECTOR, '.cico.btCloseBack')[0].click()[0].click()
                logging.debug(msg='Quiz popped up during a click quiz...')
            if choices := self._browser.find_elements(By.CLASS_NAME, 'wk_Circle'):
                random.choice(choices).click()
                time.sleep(3)
            # click the 'next question' button
            self._browser.wait_until_clickable(By.CLASS_NAME, 'wk_button', 10)
            self._browser.click_element(By.CLASS_NAME, 'wk_button')
            # if the green check mark reward icon is visible, end loop
            time.sleep(1)
            if self._browser.find_elements(By.CSS_SELECTOR, 'span[class="rw_icon"]'):
                break