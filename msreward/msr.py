import logging
from msreward.account.stats import MSRStatsSummary

from msreward.account import MSRAccount
from msreward.worker import MSRWorker
from helper.browser import Browser

# URLs
DASHBOARD_URL = 'https://account.microsoft.com/rewards/dashboard'

# user agents for edge/pc and mobile
PC_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134')
MOBILE_USER_AGENT = ('Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; WebView/3.0) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/64.118.222 '
                     'Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15063')


class MSR:
    def __init__(self, email: str, pswd: str, opt_secret=None, headless_mode=True):
        self.browser = None
        self.email = email
        self.pswd = pswd
        self.opt_secret = opt_secret
        self.headless_mode = headless_mode

    def _start_browser(self, user_agent, log_in=False):
        self.browser = Browser(self.headless_mode, user_agent)
        self.account = MSRAccount(self.browser, self.email, self.pswd, self.opt_secret)
        self.worker = MSRWorker(self.browser, self.account)
        if log_in:
            self.account.log_in()

    def _quit_browser(self):
        if self.browser:
            self.browser.quit()

    def work(self, pc: bool, mobile: bool, quiz: bool):
        ua = PC_USER_AGENT if pc or quiz else MOBILE_USER_AGENT
        self._start_browser(ua, log_in=True)

        summary = self.account.get_summary()        
        if summary.all_done:
            logging.info(msg=f'{"Already done":-^33}')            
        else:
            self._work(pc, mobile, quiz, summary)
        self._quit_browser()

    def _work(self, pc, mobile, quiz, summary:MSRStatsSummary):
        logging.info(msg=f'{"Work started":-^33}')
        if quiz:
            self.worker.do_dashboard(summary)
            self.worker.do_punchcard(summary)
        if pc and not summary.pc_search_done:
            self.worker.do_search(summary.num_of_pc_search_needed)
        if mobile and not summary.mob_search_done:
            self._prep_mobile()
            self.worker.do_search(summary.num_of_mobile_search_needed)

        logging.info(msg=f'{"Work finished":-^33}')
        self.account.get_summary(log=True)

    def _prep_mobile(self):
        if self.browser:
            if self.browser.mobile_mode:
                return
            self._quit_browser()
        self._start_browser(MOBILE_USER_AGENT, log_in=True)
            