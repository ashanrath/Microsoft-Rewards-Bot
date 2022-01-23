import logging
import time

from selenium.webdriver.common.by import By

from .quizbase import QuizBase


class LightningQuiz(QuizBase):
    def __init__(self, browser):
        super().__init__(browser, 'Lightning', 'rqAnswerOption0', By.ID)

    def _do_quiz(self):
        for question_round in range(10):
            logging.debug(msg=f'Round# {question_round}')
            if self._browser.find_elements(By.ID, 'rqAnswerOption0'):
                time.sleep(3)
                for i in range(10):
                    if self._browser.find_elements(By.ID, f'rqAnswerOption{i}'):
                        self._browser.execute_script(
                            f"document.querySelectorAll('#rqAnswerOption{i}').forEach(el=>el.click());")
                        logging.debug(msg=f'Clicked {i}')
                        time.sleep(2)
            # let new page load
            time.sleep(1)
            if self._browser.find_elements(By.ID, 'quizCompleteContainer'):
                break
        self._close_quiz_comletion_splash()