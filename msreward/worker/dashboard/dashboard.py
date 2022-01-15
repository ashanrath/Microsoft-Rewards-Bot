import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .linkquest import MSRLinkQuest
from .quiz import MSRQuiz
from .punchcard import MSRPunchCard
from helper.browser import Browser
from msreward.account import MSRAccount

DASHBOARD_URL = 'https://account.microsoft.com/rewards/dashboard'

class MSRDashboardWorker(MSRQuiz, MSRPunchCard, MSRLinkQuest):
    def __init__(self, browser:Browser, account:MSRAccount):
        self._browser = browser
        self._account = account
        super().__init__()

class MSRDashboard:
    def __init__(self, browser:Browser, account:MSRAccount) -> None:
        self._dashboard_worker = MSRDashboardWorker(browser, account)
        self._browser = browser

    def do_dashboard(self, max_attempts=5):
        #TODO Use quiz name to find link
        for _ in range(max_attempts):
            offer_links = self._goto_dashboard_get_offer_links()
            if not offer_links:
                logging.info(msg='No more dashboard offers found.')
                return
            
            for link in offer_links:
                self._do_offer(link)
        
        self._browser.get(DASHBOARD_URL)
        time.sleep(0.1)
        self._browser.wait_until_visible(By.TAG_NAME, 'body', 10)  # checks for page load
        open_offers = self._browser.find_elements(By.XPATH, 
            '//span[contains(@class, "mee-icon-AddMedium")]')
        logging.info(
            msg=f'Max attempt reached. Number of incomplete offers: {len(open_offers)}')

    def do_punch_card(self, links):
        for link in links:
            self._dashboard_worker.do_punch_card(link)

    def _do_offer(self, link):
        logging.debug(msg='Offer found.')
        self._goto_offer_link(link)
            
        if not self._dashboard_worker.do_quiz():
            logging.debug(msg='Explore Daily identified.')
            self._dashboard_worker.do_link_quest()

    def _goto_offer_link(self, link):
        link.click()
        self._browser.goto_latest_window()
        time.sleep(5)
        self._complete_sign_in_prompt()
    
    def _goto_dashboard_get_offer_links(self) -> list[WebElement]:
        self._browser.get(DASHBOARD_URL)
        time.sleep(4)
        open_offers = self._browser.find_elements(By.XPATH, '//span[contains(@class, "mee-icon-AddMedium")]/ancestor::div[contains(@data-bi-id, "Default")]')
        logging.info(msg=f'Number of open offers: {len(open_offers)}')
        if not open_offers:
            return []
        return [
            offer.find_element(By.TAG_NAME, 'a')
            for offer in open_offers
        ]

    def _complete_sign_in_prompt(self):
        sign_in_prompt_msg = self._browser.find_elements(By.CLASS_NAME, 'simpleSignIn')
        if not sign_in_prompt_msg:
            return
        logging.info(msg='Detected sign-in prompt')
        self._browser.wait_until_clickable(By.LINK_TEXT, 'Sign in', 15)
        self._browser.click_element(By.LINK_TEXT, 'Sign in')
        logging.info(msg='Clicked sign-in prompt')
        time.sleep(4)