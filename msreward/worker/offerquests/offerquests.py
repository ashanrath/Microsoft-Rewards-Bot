from selenium.webdriver.common.by import By
from telegram import Poll

from helper.browser import Browser
from .linkexplore import LinkExplore
from .poll import Poll
from .quiz.click import ClickQuiz
from .quiz.dragdrop import DragDropQuiz
from .quiz.lightning import LightningQuiz


class OfferQuests:
    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self.click_quiz = ClickQuiz(self._browser)
        self.drag_n_drop_quiz = DragDropQuiz(self._browser)
        self.lightning_quiz = LightningQuiz(self._browser)
        self.poll_quest = Poll(self._browser)
        self.link_explore = LinkExplore(self._browser)

    def do_quest(self):
        if self._browser.click_element(By.ID, 'rqStartQuiz', ignore_no_ele_exc=True) and self._has_the_quiz_started():
            return self._do_quiz()
        if self.poll_quest.do():
            return True
        return self.link_explore.do()

    def _has_the_quiz_started(self):
        return len(self._browser.find_elements(By.CLASS_NAME, 'rqECredits')) > 0

    def _do_quiz(self):
        if self.click_quiz.do():
            return True
        if self.drag_n_drop_quiz.do():
            return True
        return self.lightning_quiz.do()
