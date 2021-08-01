import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyotp

from helper.browser import Browser

# URLs
LOGIN_URL = 'https://login.live.com/'
BING_SEARCH_URL = 'https://www.bing.com/search'

# Web elements
LOGIN_EMAIL_INPUT_NAME = 'loginfmt'
LOGIN_PASSWWORD_INPUT_NAME = 'passwd'
LOGIN_OTC_INPUT_NAME = 'otc'
LOGIN_SIGN_IN_BUTTON_XPATH = '//input[@type="submit"]'

class FailToSignInException(Exception):
    pass

class MSRLogin:
    _browser: Browser
    email: str
    psw: str
    otp_secret: str

    def log_in(self):
        logging.info(msg=f'Logging in {self.email}...')
        self._browser.get(LOGIN_URL)
        time.sleep(0.5)

        self._enter_email()
        self._enter_password()
        if self.otp_secret:
            self._enter_otc()
        time.sleep(1)
        self._click_i_look_good()

        if self._browser.find_by_xpath(LOGIN_SIGN_IN_BUTTON_XPATH):
            self._browser.click_by_xpath(LOGIN_SIGN_IN_BUTTON_XPATH)
        self._browser.wait_until_visible(
            By.XPATH, '//*[@id="uhfLogo" or @id="microsoft"]', 10)

        self._log_into_bing_mobile() if self._browser.mobile_mode else self._log_into_bing_pc()
        time.sleep(1)
        self._accept_bnp()
        time.sleep(1)
        logging.info(msg='Logging successful.')

    def _enter_email(self):
        self._enter_login_screen_value(
            LOGIN_EMAIL_INPUT_NAME, self.email, 'Sent Email Address.'
        )

    def _enter_password(self):
        self._enter_login_screen_value(
            LOGIN_PASSWWORD_INPUT_NAME, self.pswd, 'Sent Password.'
        )

    def _enter_otc(self):
        logging.debug(msg='OTC information is provided.')
        if not self._browser.find_elements_by_name(LOGIN_OTC_INPUT_NAME):
            self._switch_to_otc_method()
        totp = pyotp.TOTP(self.otp_secret)
        otc = totp.now()
        self._enter_login_screen_value(LOGIN_OTC_INPUT_NAME, otc, 'Sent OTC')

    def _switch_to_otc_method(self):
        logging.debug(msg='Switching to OTC verification method.')
        sign_in_another_way = self._browser.find_by_id('signInAnotherWay')
        if not sign_in_another_way:
            raise FailToSignInException('Sign in is failed. Unable to switch to OTC verification method. Did not find the "sign in another way" link.')

        sign_in_another_way[0].click()
        time.sleep(1)
        verificaiton_methods = self._browser.find_by_xpath('//div[@data-bind="text: display"]')
        for vm in verificaiton_methods:
            if 'mobile app' in vm.text:
                vm.click()
                break
        else:
            raise FailToSignInException(f'Sign in is failed. Unable to switch to OTC verification method. No such option. All options are:\n{[x.text for x in verificaiton_methods]}')

    def _enter_login_screen_value(self, ele_name, value, msg):
        self._browser.wait_until_clickable(By.NAME, ele_name, 10)
        self._browser.send_key_by_name(ele_name, value)
        logging.debug(msg=msg)
        time.sleep(0.5)
        self._browser.send_key_by_name(ele_name, Keys.RETURN)
        time.sleep(0.5)

    def sign_in_prompt(self):
        time.sleep(3)
        sign_in_prompt_msg = self._browser.find_by_class('simpleSignIn')
        if sign_in_prompt_msg:
            logging.info(msg='Detected sign-in prompt')
            self._browser.wait_until_clickable(By.LINK_TEXT, 'Sign in', 15)
            self._browser.find_element_by_link_text('Sign in').click()
            logging.info(msg='Clicked sign-in prompt')
            time.sleep(4)

    def _log_into_bing_pc(self):
        self._browser.get(BING_SEARCH_URL)
        self._browser.wait_until_clickable(By.ID, 'id_l', 5)
        self._browser.click_by_id('id_l')
        time.sleep(0.1)
        self._browser.wait_until_clickable(By.ID, 'id_l', 5)
        # self._browser.wait_until_clickable(
        #     By.XPATH, "//*[text()='Sign in' and @aria-hidden='false']//parent::a", 5)
        # if self._browser.find_by_xpath("//*[text()='Sign in' and @aria-hidden='false']//parent::a"):
        #     self._browser.click_by_xpath(
        #         "//*[text()='Sign in' and @aria-hidden='false']//parent::a")
        # self._browser.wait_until_clickable(
        #     By.XPATH, "//*[text()='Sign in']//parent::a", 5)

    def _log_into_bing_mobile(self):
        self._browser.get(BING_SEARCH_URL)
        self._browser.wait_until_clickable(
            By.XPATH, '//*[@aria-label="Preferences"]', 5)
        self._browser.click_by_xpath('//*[@aria-label="Preferences"]')
        time.sleep(0.1)
        self._browser.wait_until_clickable(
            By.XPATH, "//*[text()='Sign in']//parent::a", 5)
        if self._browser.find_by_xpath("//*[text()='Sign in']//parent::a"):
            self._browser.click_by_xpath("//*[text()='Sign in']//parent::a")
            self._browser.wait_until_clickable(
                By.XPATH, '//*[@aria-label="Preferences"]', 5)
        else:
            self._browser.click_by_xpath('//*[@aria-label="Preferences"]')

    def _accept_bnp(self):
        btn = self._browser.find_elements_by_class_name('bnp_btn_accept')
        if not btn:
            return
        btn[0].click()

    def _click_i_look_good(self):
        btn = self._browser.find_elements_by_id('iLooksGood')
        if not btn:
            return
        btn[0].click()