from msreward.account.stats import MSRStatsSummary
from helper.browser import Browser
from msreward.account import MSRAccount
from .search import MSRSearch
from .dashboard import MSRDashboard

class MSRWorker:
    account: MSRAccount

    def __init__(self, browser:Browser, account:MSRAccount) -> None:
        self._browser = browser
        self._account = account
        self._dashboard = MSRDashboard(self._browser, self._account)
        self._search = MSRSearch(self._browser, self._account)

    def do_search(self, num_of_search_needed):
        if num_of_search_needed > 0:
            self._search.search(num_of_search_needed)

    def do_dashboard(self, summary: MSRStatsSummary):
        if not summary.quiz_done:
            self._dashboard.do_dashboard()
    
    def do_punchcard(self, summary: MSRStatsSummary):
        if len(summary.punch_card_links):
            self._dashboard.do_punch_card(summary.punch_card_links)
