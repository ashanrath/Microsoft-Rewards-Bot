import logging

from selenium.webdriver.common.by import By

from helper.browser import Browser


class QuizBase:
    def __init__(self, browser:Browser, name, selector, by:By):
        self._browser = browser
        self._name = name
        self._selector = selector
        self._by = by

    def do(self):
        if self.available():
            self._do_quiz()
            logging.info(msg=f'{self._name} Quiz completed.')
            return True
        return False

    def available(self):
        if self._browser.find_elements(self._by, self._selector):
            logging.debug(msg=f'{self._name} Quiz identified.')
            return True
        return False

    def _do_quiz(self):
        NotImplementedError()

    def _close_quiz_comletion_splash(self):
        self._browser.goto_main_window()
