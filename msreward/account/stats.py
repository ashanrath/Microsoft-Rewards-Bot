import logging
import time
import json
import re

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
        self.punch_card_progress = 0
        self.punch_card_max = 0
        self.punch_card_links = []

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
        return self.quiz_progress >= self.quiz_max

    @property
    def punch_card_done(self) -> bool:
        return self.punch_card_progress >= self.punch_card_max

    @property
    def all_done(self) -> bool:
        return self.punch_card_done and self.quiz_done and self.mob_search_done and self.pc_search_done1

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

        self.summary = MSRStatsSummary(log=True)
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
        self.summary.available_points = int(
            json_doc['userStatus']['availablePoints'])
        self._parse_pc_search(json_doc['userStatus']['counters'])
        self._parse_mobile_search(json_doc['userStatus']['counters'])
        self._parse_quiz(json_doc)
        self._parse_punch_cards(json_doc)

    def _parse_pc_search(self, counters):
        if 'pcSearch' not in counters:
            return
        pcs = counters['pcSearch'][0]
        self.summary.pc_search_progress = int(pcs['pointProgress'])
        self.summary.pc_search_max = int(pcs['pointProgressMax'])

    def _parse_mobile_search(self, counters):
        if 'mobileSearch' not in counters:
            return
        mbs = counters['mobileSearch'][0]
        self.summary.mobile_search_progress = int(mbs['pointProgress'])
        self.summary.mobile_search_max = int(mbs['pointProgressMax'])

    def _parse_quiz(self, status):
        if 'morePromotions' not in status:
            return
        for q in status['morePromotions']:
            self.summary.quiz_progress += int(q['pointProgress'])
            self.summary.quiz_max += int(q['pointProgressMax'])

    def _parse_punch_cards(self, status):
        if 'punchCards' not in status:
            return
        for c in status['punchCards']:
            p = c['parentPromotion']
            if not p:
                continue
            if p['promotionType'].startswith('appstore'):
                continue
            self.summary.punch_card_progress += int(p['pointProgress'])
            self.summary.punch_card_max += int(p['pointProgressMax'])
            self.summary.punch_card_links.append(p['destinationUrl'])