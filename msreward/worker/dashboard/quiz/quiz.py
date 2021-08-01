from helper.browser import Browser
from .click import ClickQuiz
from .dragdrop import DragDropQuiz
from .lightning import LightningQuiz
from .poll import PollQuiz

BUTTON_ID_QUIZ_START = 'rqStartQuiz'

class MSRQuiz:
    _browser: Browser
    def __init__(self) -> None:
        self.click_quiz = ClickQuiz(self._browser)
        self.drag_n_drop_quiz = DragDropQuiz(self._browser)
        self.lightning_quiz = LightningQuiz(self._browser)
        self.poll_quiz = PollQuiz(self._browser)

    def do_quiz(self):
        if self._browser.find_by_id(BUTTON_ID_QUIZ_START):
            self._browser.click_by_id(BUTTON_ID_QUIZ_START)
        elif not self._has_the_quiz_started():
            return self.poll_quiz.do()            
        if self.click_quiz.do():
            return True
        if self.drag_n_drop_quiz.do():
            return True
        return self.lightning_quiz.do()
        
    def _has_the_quiz_started(self):
        return len(self._browser.find_elements_by_class_name('rqECredits')) > 0