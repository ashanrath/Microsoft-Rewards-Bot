from helper.browser import Browser
from ..account.stats import MSRStatsSummary
from ..account import MSRAccount
from .search import MSRSearch
from .offers import MSROffer
from .punchcard import MSRPunchCard


class MSRWorker:
    def __init__(self, browser:Browser, account:MSRAccount) -> None:
        self._browser = browser
        self._account = account
        self._search = MSRSearch(self._browser, self._account)
        self._offer = MSROffer(self._browser)
        self._punchcard = MSRPunchCard(self._browser)

    def do_search(self, num_of_search_needed):
        if num_of_search_needed > 0:
            self._search.search(num_of_search_needed)

    def do_offer(self, summary: MSRStatsSummary):
        if not summary.quiz_done:
            self._offer.do_offers()
    
    def do_punchcard(self, summary: MSRStatsSummary):
        if len(summary.punch_card_incomplete_links) and not summary.punch_card_done:
            self._punchcard.do_punch_cards(summary.punch_card_incomplete_links)
