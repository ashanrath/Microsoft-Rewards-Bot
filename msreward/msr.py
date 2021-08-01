import logging

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
    def __init__(self, email: str, pswd: str, opt_secret: str=None, headless_mode: bool=True) -> None:
        self.browser = None
        self.email = email
        self.pswd = pswd
        self.opt_secret = opt_secret
        self.headless_mode = headless_mode

    def _start_browser(self, user_agent: str, log_in: bool = False) -> None:
        self.browser = Browser(self.headless_mode, user_agent)
        self.account = MSRAccount(self.browser, self.email, self.pswd, self.opt_secret)
        self.worker = MSRWorker(self.browser, self.account)
        if log_in:
            try:
                self.account.log_in()
            except Exception:
                logging.error(msg=f'{"Failed to sign in. An error has occurred."}', exc_info=True)
                return False
        return True

    def _quit_browser(self) -> None:
        if self.browser:
            self.browser.quit()

    def work(self, flag_pc: bool, flag_mob: bool, flag_quiz: bool) -> None:
        ua = PC_USER_AGENT if flag_pc or flag_quiz else MOBILE_USER_AGENT
        if not self._start_browser(ua, log_in=True):
            logging.info('Fail to initiate.')
            return

        summary = self.account.get_summary(log=True)
        if summary.all_done:
            logging.info(msg=f'{"Already done":-^33}')
        else:
            self._work(flag_pc, flag_mob, flag_quiz)
        self._quit_browser()

    def _work(self, flag_pc: bool, flag_mob: bool, flag_quiz: bool) -> None:
        logging.info(msg=f'{"Work started":-^33}')
        summary = self.account.summary
        if flag_quiz:
            self.worker.do_dashboard(summary)
            self.worker.do_punchcard(summary)
        if flag_pc and not summary.pc_search_done:
            self.worker.do_search(summary.num_of_pc_search_needed)
        if flag_mob and not summary.mob_search_done:
            self._prep_mobile()
            self.worker.do_search(summary.num_of_mobile_search_needed)

        logging.info(msg=f'{"Work finished":-^33}')
        self.account.get_summary(log=True)

    def _prep_mobile(self) -> None:
        if self.browser:
            if self.browser.mobile_mode:
                return
            self._quit_browser()
        self._start_browser(MOBILE_USER_AGENT, log_in=True)
