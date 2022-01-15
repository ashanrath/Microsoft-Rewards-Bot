import logging
import random
import time

from selenium.webdriver.common.by import By

from .quizbase import QuizBase

class ClickQuiz(QuizBase):
    def __init__(self, browser):
        super().__init__(browser, 'Click', 'wk_Circle', By.CLASS_NAME)

    def _do_quiz(self):
        while True:
            if self._browser.find_elements(By.CSS_SELECTOR, '.cico.btCloseBack'):
                self._browser.find_elements(By.CSS_SELECTOR, '.cico.btCloseBack')[0].click()[0].click()
                logging.debug(msg='Quiz popped up during a click quiz...')
            choices = self._browser.find_elements(By.CLASS_NAME, 'wk_Circle')
            # click answer
            if choices:
                random.choice(choices).click()
                time.sleep(3)
            # click the 'next question' button
            self._browser.wait_until_clickable(By.CLASS_NAME, 'wk_button', 10)
            self._browser.click_element(By.CLASS_NAME, 'wk_button')
            # if the green check mark reward icon is visible, end loop
            time.sleep(1)
            if self._browser.find_elements(By.CSS_SELECTOR, 'span[class="rw_icon"]'):
                break
        self._close_quiz_comletion_splash()