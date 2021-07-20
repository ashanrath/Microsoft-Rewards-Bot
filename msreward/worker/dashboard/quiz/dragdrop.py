import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from .quizbase import QuizBase


class DragDropQuiz(QuizBase):
    def __init__(self, browser):
        super().__init__(browser, 'Drag&Drop', 'rqAnswerOptionNum0', By.ID)

    def _do_quiz(self):
        while True:
            try:
                # find possible solution buttons
                drag_option = self._browser.find_by_class('rqOption')
                # find any answers marked correct with correctAnswer tag
                right_answers = self._browser.find_by_class('correctAnswer')
                # remove right answers from possible choices
                if right_answers:
                    drag_option = [
                        x for x in drag_option if x not in right_answers]
                if drag_option:
                    # select first possible choice and remove from options
                    choice_a = random.choice(drag_option)
                    drag_option.remove(choice_a)
                    # select second possible choice from remaining options
                    choice_b = random.choice(drag_option)
                    ActionChains(self._browser.browser).drag_and_drop(
                        choice_a, choice_b).perform()
            except (WebDriverException, TypeError):
                logging.debug(msg='Unknown Error.')
                continue
            finally:
                time.sleep(1)
                if self._browser.find_by_id('quizCompleteContainer'):
                    break
        self._close_quiz_comletion_splash()