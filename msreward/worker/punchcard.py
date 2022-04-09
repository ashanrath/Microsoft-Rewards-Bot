import logging
import time
from warnings import catch_warnings

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementNotVisibleException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from helper.browser import Browser
from .offerquests import OfferQuests

class MSRPunchCard:
    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._quests = OfferQuests(self._browser)

    def do_punch_cards(self, links):
        for link in links:
            self._do_punch_card(link)

    def _do_punch_card(self, link, max_attempts=3):
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
                    self._browser.close_all_but_main()
                    return
                logging.debug(msg=f'Punch Card did not complete. Attempt: {i}/{max_attempts}')
                self._browser.close_all_but_main()
        logging.info(msg='Punch Card is incomplete. Max number of attempts reached.')

    def _click_through_punch_card(self, max_attempts=5):
        for _ in range(max_attempts):
            try:
                if not self._browser.click_element(By.XPATH, '//a[@class= "offer-cta"]/child::button[contains(@class, "btn-primary")]') and not self._goto_incomplete_quest():
                    break
                time.sleep(1)                
                self._browser.goto_latest_window()
                self._quests.do_quest()
                logging.debug(msg='Clicked one punch card quest.')
                self._browser.refresh()
            except WebDriverException:
                logging.exception(msg='Error occurred when clicking a punch card.')

    def _verify_punch_card_completion(self):
        return not self._browser.find_elements(By.XPATH, '//a[@class= "offer-cta" and ./button[contains(@class, "btn-primary")]]')
                
    def _goto_incomplete_quest(self):
        if not self._browser.find_element(By.CLASS_NAME, 'c-progress'):
            return False
        link = self._browser.find_element(By.XPATH, '//progress[@class="c-progress"]//parent::div/parent::div/div/a')
        try:
            link.click()
        except ElementClickInterceptedException:
            url = link.get_attribute('href')
            self._browser.open_in_new_tab(url)
        return True
