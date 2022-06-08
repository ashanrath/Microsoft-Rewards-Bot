import json
import logging
import os
import random
import time
from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from msreward.account import MSRAccount
from helper.browser import Browser
import env

class MSRSearch():
    SEARCH_TERM_LOCAL_FILE = 'search_terms.json'

    def __init__(self, browser:Browser, account:MSRAccount) -> None:
        self._browser = browser
        self._account = account        

    def search(self, num_of_searches:int) -> None:
        """
        Searches using an enumerated list of search terms, prints search item and number
        :param num_of_searches: int, NUmber of searches to perform
        :return: None
        """        
        self._browser.get(env.URL_BING_SEARCH)
        search_name = f'{"Mobile" if self._browser.mobile_mode else "PC"} search'
        if num_of_searches < 1:
            logging.info(msg=f'{search_name} completed, no more search needs to be done.')
            return

        logging.info(msg=f'{search_name} started.')
        search_terms = SearchTerms.get()
        if search_terms == [] or search_terms is None:
            logging.info(msg=f'{search_name} aborted. No search terms.')
            return

        self._search(search_terms, num_of_searches)
        logging.info(msg=f'{search_name} completed.')

    def _get_num_of_searches(self):
        point_summary = self._account.get_summary()
        return point_summary.num_of_mobile_search_needed if self._browser.mobile_mode else point_summary.num_of_pc_search_needed

    def _search(self, search_terms:list[str], num_of_searches:int):
        for num, item in enumerate(search_terms):
            try:
                logging.info(msg=f'Search #{num}: {item[:80]}')
                self._search_term(item)
                if num == num_of_searches - 1:
                    remaining = self._get_num_of_searches()
                    if remaining <= 0:
                        break
                    num_of_searches += remaining
            except UnexpectedAlertPresentException:
                self._browser.switch_to.alert.dismiss()
                self._browser.get(env.URL_BING_SEARCH)

    def _search_term(self, term):
        # clears search bar and enters in next search term
        time.sleep(1)
        self._browser.wait_until_visible(By.ID, 'sb_form_q', 15)
        self._browser.clear_element(By.ID, 'sb_form_q')
        self._browser.send_key(By.ID, 'sb_form_q', term)
        time.sleep(0.1)
        self._browser.send_key(By.ID, 'sb_form_q', Keys.RETURN)
        # random sleep for more human-like, and let ms reward website keep up.
        time.sleep(random.randint(1, 3))
        self._browser.wait_until_clickable(
            By.XPATH, '//*[@id="id_rc" or @id="bpage"]', 5)
        self._browser.scroll_to_bottom()
        time.sleep(random.randint(1, 3))
        self._browser.scroll_to_top()

def today_str():
    return datetime.now().strftime("%Y%m%d")

def get_dates(days_to_get=4) -> str:
    """
    Returns a list of dates from today to x days ago in year, month, day format
    :param days_to_get: number of days to get from api
    :return: list of string of dates in year, month, day format
    """
    dates = []
    for i in range(days_to_get):
        # get dates
        date = datetime.now() - timedelta(days=i)
        # append in year month date format
        dates.append(date.strftime('%Y%m%d'))
    return dates

class SearchTerms:
    SEARCH_TERM_LOCAL_FILE = 'logs/search_terms.json'

    def __init__(self):
        self.search_terms = []

    @staticmethod
    def get():
        s = SearchTerms()
        s._get_search_terms()
        return s.search_terms

    def _get_search_terms(self):
        dates = get_dates()

        if self._get_cached_search_terms():
            return

        for date in dates:
            try:
                self._get_terms_from_google_trends(date)
            except RequestException:
                logging.error('Error retrieving google trends json.')
            except KeyError:
                logging.error('Cannot parse, JSON keys are modified.')

        logging.info(msg=f'# of search items: {len(self.search_terms)}\n')
        self._dump_cached_search_terms()
        list(set(self.search_terms))

    def _get_terms_from_google_trends(self, date):
        url = f'{env.URL_GTREND}&ed={date}'
        request = requests.get(url)
        response = json.loads(request.text[5:])
        # get all trending searches with their related queries
        for topic in response['default']['trendingSearchesDays'][0]['trendingSearches']:
            self.search_terms.append(topic['title']['query'].lower())
            for related_topic in topic['relatedQueries']:
                self.search_terms.append(related_topic['query'].lower())

    def _get_cached_search_terms(self) -> bool:
        if not os.path.exists(self.SEARCH_TERM_LOCAL_FILE):
            return False

        with open(self.SEARCH_TERM_LOCAL_FILE, 'r') as f:
            data = json.load(f)

        if data['date_cached'] != today_str():
            return False
        self.search_terms = data['terms']
        return True

    def _dump_cached_search_terms(self):
        data = {'date_cached': today_str(),
                'terms': self.search_terms
                }
        with open(self.SEARCH_TERM_LOCAL_FILE, 'w') as file:
            json.dump(data, file)