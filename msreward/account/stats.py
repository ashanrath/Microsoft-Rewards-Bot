import logging
import time
import json
import re
import datetime

from helper.browser import Browser


# URLs
DASHBOARD_URL = 'https://account.microsoft.com/rewards/'

class MSRStatsSummary:
    POINT_PER_MOB_SEARCH = 3
    POINT_PER_PC_SEARCH = 3

    def __init__(self):
        self.available_points = 0
        self.pc_search_progress = 0
        self.pc_search_max = 0
        self.mobile_search_progress = 0
        self.mobile_search_max = 0
        self.quiz_progress = 0
        self.quiz_max = 0
        self.quiz_incomplete_names = []
        self.punch_card_progress = 0
        self.punch_card_max = 0
        self.punch_card_incomplete_links = []

    @property
    def num_of_pc_search_needed(self) -> int:
        return (self.pc_search_max - self.pc_search_progress)/MSRStatsSummary.POINT_PER_PC_SEARCH

    @property
    def num_of_mobile_search_needed(self) -> int:
        return (self.mobile_search_max - self.mobile_search_progress)/MSRStatsSummary.POINT_PER_MOB_SEARCH

    @property
    def quiz_points_availability(self) -> int:
        return self.quiz_max - self.quiz_progress

    @property
    def punch_card_points_availability(self) -> bool:
        return self.punch_card_max - self.punch_card_progress

    @property
    def pc_search_done(self) -> bool:
        return self.pc_search_progress >= self.pc_search_max
    
    @property
    def mob_search_done(self) -> bool:
        return self.mobile_search_progress >= self.mobile_search_max

    @property
    def quiz_done(self) -> bool:
        return self.quiz_incomplete_names == []

    @property
    def punch_card_done(self) -> bool:
        return self.punch_card_incomplete_links == []

    @property
    def all_done(self) -> bool:
        return self.punch_card_done and self.quiz_done and self.mob_search_done and self.pc_search_done

    def print(self):
        logging.info(msg=f'Account summary:')
        logging.info(msg=f'{"Available Points":.<25} {self.available_points}')
        logging.info(
            msg=f'{"PC Search ":.<25} {self.pc_search_progress}/{self.pc_search_max}')
        logging.info(
            msg=f'{"Mobile Search ":.<25} {self.mobile_search_progress}/{self.mobile_search_max}')
        logging.info(
            msg=f'{"Quiz ":.<25} {self.quiz_progress}/{self.quiz_max}')
        logging.info(
            msg=f'{"Punch Card ":.<25} {self.punch_card_progress}/{self.punch_card_max}')


class MSRStats:
    _browser: Browser

    def get_summary(self, cached=False, log=False):
        if cached:
            return self.summary

        self._browser.open_in_new_tab(DASHBOARD_URL)
        time.sleep(1)
        
        if self._browser.click_by_xpath('//a[contains(@class, "signup-btn welcome")]'):
            logging.info('Welcome page detected.')
            time.sleep(4)

        self.summary = MSRStatsSummary()
        self._parse_user_status(self._get_user_status_json())

        self._browser.goto_main_window()

        if log:
            self.summary.print()
        return self.summary

    def _get_user_status_json(self):
        js = self._browser.find_elements_by_xpath(
            '//script[text()[contains(., "userStatus")]]')
        if not js:
            return {}

        matches = re.search(
            r'(?=\{"userStatus":).*(=?\}\};)', js[0].get_attribute('text'))
        if not matches:
            return {}
        return json.loads(matches[0][:-1])

    def _parse_user_status(self, json_doc):
        if 'userStatus' not in json_doc:
            logging.exception('Cannot find key "userStatus"')
            return
        self._parse_available_points(json_doc['userStatus'])
        self._parse_pc_search(json_doc['userStatus']['counters'])
        self._parse_mobile_search(json_doc['userStatus']['counters'])
        self._parse_quiz(json_doc)
        self._parse_daily(json_doc)
        self._parse_punch_cards(json_doc)

    def _parse_available_points(self, user_status):
        if 'availablePoints' not in user_status:
            logging.exception('Cannot find key "availablePoints"')
            return
        self.summary.available_points = int(user_status['availablePoints'])

    def _parse_pc_search(self, counters):
        if 'pcSearch' not in counters:
            logging.exception('Cannot find key "pcSearch"')
            return
        pcs = counters['pcSearch'][0]
        self.summary.pc_search_progress = int(pcs['pointProgress'])
        self.summary.pc_search_max = int(pcs['pointProgressMax'])

    def _parse_mobile_search(self, counters):
        if 'mobileSearch' not in counters:
            logging.info('Cannot find key "mobileSearch". Mobile search is unavailable.')
            return
        mbs = counters['mobileSearch'][0]
        self.summary.mobile_search_progress = int(mbs['pointProgress'])
        self.summary.mobile_search_max = int(mbs['pointProgressMax'])

    def _parse_quiz(self, json_doc):
        if 'morePromotions' not in json_doc:
            logging.exception('Cannot find key "morePromotions"')
            return
        for d in json_doc['morePromotions']:
            self._add_quiz_to_summary(d)

    def _parse_daily(self, json_doc):
        if 'dailySetPromotions' not in json_doc:
            logging.exception('Cannot find key "dailySetPromotions"')
            return
        today = f'{datetime.datetime.now():%m/%d/%Y}'
        if today not in json_doc['dailySetPromotions']:
            return
        for d in json_doc['dailySetPromotions'][today]:
            self._add_quiz_to_summary(d)

    def _add_quiz_to_summary(self, d):
        self.summary.quiz_progress += int(d['pointProgress'])
        self.summary.quiz_max += int(d['pointProgressMax'])
        if not d['complete']:
            self.summary.quiz_incomplete_names += d['name']

    def _parse_punch_cards(self, json_doc):
        if 'punchCards' not in json_doc:
            logging.exception('Cannot find key "punchCards"')
            return
        for d in json_doc['punchCards']:
            p = d['parentPromotion']
            if not p:
                continue
            if p['promotionType'].startswith('appstore'):
                continue
            self.summary.punch_card_progress += int(p['pointProgress'])
            self.summary.punch_card_max += int(p['pointProgressMax'])
            if not p['complete']:
                self.summary.punch_card_incomplete_links.append(p['destinationUrl'])