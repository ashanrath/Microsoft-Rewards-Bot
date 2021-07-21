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
        open_offers = self._browser.find_elements_by_xpath(
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
        open_offers = self._browser.find_elements_by_xpath('//span[contains(@class, "mee-icon-AddMedium")]')
        if not open_offers:
            return []
        return self._extract_offer_links(open_offers)

    def _extract_offer_links(self, open_offer_ele):
        logging.info(msg=f'Number of open offers: {len(open_offer_ele)}')
        # get common parent element of open_offers
        parent_elements = [open_offer.find_element_by_xpath(
            '..//..//..//..') for open_offer in open_offer_ele]
        # get points links from parent, # finds link (a) descendant of selected node
        return [
            parent.find_element_by_xpath(
                'div[contains(@class,"actionLink")]//descendant::a')
            for parent in parent_elements
        ]

    def _complete_sign_in_prompt(self):
        sign_in_prompt_msg = self._browser.find_by_class('simpleSignIn')
        if not sign_in_prompt_msg:
            return
        logging.info(msg='Detected sign-in prompt')
        self._browser.wait_until_clickable(By.LINK_TEXT, 'Sign in', 15)
        self._browser.find_element_by_link_text('Sign in').click()
        logging.info(msg='Clicked sign-in prompt')
        time.sleep(4)