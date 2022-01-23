import logging

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementNotVisibleException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from helper.browser import Browser

class MSRLinkQuest:
    _browser: Browser

    def do_link_quest(self):
        try:
            html = self._browser.find_element(By.TAG_NAME, 'html')
            # scroll up and down to trigger points
            for _ in range(3):
                html.send_keys(Keys.END)
                html.send_keys(Keys.HOME)
            logging.info('Link Quest completed')
            self._browser.goto_main_window_close_others()
        except TimeoutException:
            logging.exception(msg='Explore Daily Timeout Exception.')
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(msg='Element not clickable or visible.')
        except WebDriverException:
            logging.exception(msg='Error.')