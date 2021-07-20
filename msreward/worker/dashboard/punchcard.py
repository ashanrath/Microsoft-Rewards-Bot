import logging
import time

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementNotVisibleException, NoSuchElementException, TimeoutException, WebDriverException

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
                    logging.info(msg='Punch Card completed')
                    self._browser.goto_main_window()
                    return
                logging.debug(msg=f'Punch Card did not complete. Attempt completed: {i}/3')
                self._browser.goto_main_window()
        logging.info(msg='Punch Card not incomplete. Max number of attempts reached')

    def _click_through_punch_card(self, max_attempts=5):
        for _ in range(max_attempts):
            try:
                if not self._browser.click_by_xpath('//a[@class= "offer-cta"]/child::button[contains(@class, "btn-primary")]'):
                    self._browser.close()
                    self._browser.goto_latest_window()
                    break
                time.sleep(4)
                self._browser.goto_latest_window()
                self._browser.close()
                self._browser.goto_latest_window()
                logging.debug(msg='Clicked one punch card quest.')
            except WebDriverException:
                logging.exception(msg='Error occurred when clicking a punch card.')

    def _verify_punch_card_completion(self):
        return not self._browser.find_by_xpath('//a[@class= "offer-cta" and ./button[contains(@class, "btn-primary")]]')
                
        