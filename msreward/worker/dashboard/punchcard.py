import logging
import time

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementNotVisibleException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from helper.browser import Browser

class MSRPunchCard:
    _browser: Browser

    def do_punch_card(self, link, max_attempts=3):
        for i in range(max_attempts):
            try:
                self._browser.open_in_new_tab(link)
                self._click_through_punch_card()
            except TimeoutException:
                logging.exception(msg='Explore Daily Timeout Exception.')
            except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
                logging.exception(msg='Element not clickable or visible.')
            except WebDriverException:
                logging.exception(msg='Error.')
            finally:
                if self._verify_punch_card_completion():
                    logging.info(msg='Punch Card is completed')
                    self._browser.goto_main_window_close_others()
                    return
                logging.debug(msg=f'Punch Card did not complete. Attempt: {i}/{max_attempts}')
                self._browser.goto_main_window_close_others()
        logging.info(msg='Punch Card is incomplete. Max number of attempts reached.')

    def _click_through_punch_card(self, max_attempts=10):
        for _ in range(max_attempts):
            try:
                if not self._browser.click_element(By.XPATH, '//a[@class= "offer-cta"]/child::button[contains(@class, "btn-primary")]'):
                    break
                time.sleep(1)
                self._browser.goto_latest_window()
                self._browser.close()
                self._browser.goto_latest_window()
                logging.debug(msg='Clicked one punch card quest.')
            except WebDriverException:
                logging.exception(msg='Error occurred when clicking a punch card.')

    def _verify_punch_card_completion(self):
        return not self._browser.find_elements(By.XPATH, '//a[@class= "offer-cta" and ./button[contains(@class, "btn-primary")]]')
                
        