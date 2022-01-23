import random
import time

from selenium.webdriver.common.by import By

from .quizbase import QuizBase


class PollQuiz(QuizBase):
    def __init__(self, browser):
        super().__init__(browser, 'Poll', 'btoption0', By.ID)

    def _do_quiz(self):
        # click poll option
        choices = ['btoption0', 'btoption1']
        self._browser.click_element(By.ID, random.choice(choices))
        time.sleep(1)
        self._browser.goto_main_window_close_others()