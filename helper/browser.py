import logging
import os
import platform
from datetime import datetime


from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, \
    ElementClickInterceptedException, ElementNotVisibleException, \
    ElementNotInteractableException, NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from helper.driver import download_driver


class Browser(Chrome):
    def __init__(self, headless_mode: bool, user_agent: str):
        self.mobile_mode = 'android' in user_agent.lower()
        self.user_agent = user_agent

        path = Browser._prepare_driver()

        options = self._get_driver_options()

        if headless_mode:
            options.add_argument('--headless')

        super().__init__(path, chrome_options=options)

    @staticmethod
    def _prepare_driver():
        os.makedirs('drivers', exist_ok=True)
        path = os.path.join('drivers', 'chromedriver')
        system = platform.system()
        if system == "Windows" and not path.endswith(".exe"):
            path += ".exe"
        if not os.path.exists(path):
            download_driver(path, system)
        return path

    def _get_driver_options(self):
        options = Options()
        options.add_argument(f'user-agent={self.user_agent}')
        options.add_argument('--disable-webgl')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_experimental_option('w3c', False)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        prefs = {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        return options

    def _is_same_ua(self, user_agent):
        return user_agent == self.user_agent

    def wait_until_visible(self, by_: By, selector, time_to_wait=10, poll_frequency=0.5, raise_exc=False):
        try:
            WebDriverWait(self, time_to_wait, poll_frequency).until(
                ec.visibility_of_element_located((by_, selector)))
        except TimeoutException:
            self._wait_until_timeout_handler(selector, ' element not visible - Timeout Exception', raise_exc)
        except UnexpectedAlertPresentException:
            self._unexpected_alert_handler(selector)
        except WebDriverException:
            ss = self.screenshot(selector)
            logging.exception(msg=f'Webdriver Error for {selector} object. Screenshot saved to {ss}')

    def wait_until_clickable(self, by_: By, selector, time_to_wait=10, poll_frequency=0.5, raise_exc=False):
        try:
            WebDriverWait(self, time_to_wait, poll_frequency).until(
                ec.element_to_be_clickable((by_, selector)))
        except TimeoutException:
            self._wait_until_timeout_handler(selector, ' element not clickable - Timeout Exception', raise_exc)
        except UnexpectedAlertPresentException:
            self._unexpected_alert_handler(selector)
        except WebDriverException:
            ss = self.screenshot(selector)
            logging.exception(msg=f'Webdriver Error for {selector} object. Screenshot saved to {ss}')

    def _unexpected_alert_handler(self, selector):
        self.switch_to.alert.dismiss()
        ss = self.screenshot(selector)
        logging.exception(msg=f'Unexpected Alert Exception. Screenshot saved to {ss}', exc_info=False)
        self.refresh()

    def _wait_until_timeout_handler(self, selector, arg1, raise_exc):
        ss = self.screenshot(selector)
        msg = f'{selector}{arg1}. Screenshot saved to {ss}'
        if raise_exc:
            raise TimeoutException(msg)
        logging.exception(msg=msg, exc_info=False)

    def send_key(self, by_, selector, key, ignore_no_ele_exc=False) -> bool:
        try:
            self.find_element(by_, selector).send_keys(key)
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(msg=f'Found {selector} element by {by_}, but it is not visible or interactable.', exc_info=False)
        except NoSuchElementException:
            if not ignore_no_ele_exc:
                self._handle_no_such_element_exception(selector, by_)
        except WebDriverException:
            logging.exception(msg=f'Webdriver Error in sending key. Searched by {by_} for {selector}')
        finally:
            return False

    def click_element(self, by_, selector, ignore_no_ele_exc=False) -> bool:
        try:
            self.find_element(by_, selector).click()
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(msg=f'Found {selector} element by {by_}, but it is not visible or interactable. Attempting JS Click', exc_info=False)
            self.js_click(self.find_element(By.CLASS_NAME, selector))
        except NoSuchElementException:
            if not ignore_no_ele_exc:
                self._handle_no_such_element_exception(selector, by_)
        except WebDriverException:
            logging.exception(msg=f'Webdriver Error in clicking. Searched by {by_} for {selector}.')
        finally:
            return False

    def clear_element(self, by_, selector, ignore_no_ele_exc=False) -> bool:
        try:
            self.find_element(by_, selector).clear()
            return True
        except (ElementNotVisibleException, ElementNotInteractableException):
            logging.exception(msg=f'Found {selector} element by {by_}, but it is not visible or interactable.', exc_info=False)
        except NoSuchElementException:
            if not ignore_no_ele_exc:
                self._handle_no_such_element_exception(selector, by_)
        except WebDriverException:
            logging.exception(msg=f'Webdriver Error in clearing. Searched by {by_} for {selector}.')
        finally:
            return False

    def _handle_no_such_element_exception(self, selector, by_):
        ss = self.screenshot(selector)
        logging.exception(msg=f'Element not found when searched for {selector} by {by_}. Screenshot save to {ss}', exc_info=False, )
        self.refresh()

    def js_click(self, element):
        """Click any given element"""
        try:
            self.execute_script("arguments[0].click();", element)
        except Exception:
            logging.exception(msg='Exception when JS click')

    def screenshot(self, selector):
        logging.exception(msg=f'{selector} cannot be located.')
        screenshot_file_name = f'{datetime.now().strftime("%Y%m%d%%H%M%S")}_{selector}.png'
        screenshot_file_path = os.path.join('logs', screenshot_file_name)
        self.save_screenshot(screenshot_file_path)
        return screenshot_file_path

    def scroll_to_bottom(self):
        try:
            self.execute_script("scrollBy(0,250);")
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print('Exception when scrolling :', e)

    def scroll_to_top(self):
        try:
            self.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
        except Exception as e:
            print('Exception when scrolling :', e)

    def open_in_new_tab(self, url):
        self.execute_script("window.open('');")
        self.goto_latest_window()
        self.get(url)

    def goto_main_window_close_others(self):
        """
        Closes all other windows and switches focus back to main window
        :return: None
        """
        try:
            for _ in range(len(self.window_handles)-1):
                self.switch_to.window(self.window_handles[-1])
                self.close()
        except WebDriverException:
            logging.error('Error when switching to main_window')
        finally:
            self.switch_to.window(self.window_handles[0])

    def goto_latest_window(self):
        """
        Switches to newest open window
        :return:
        """
        self.switch_to.window(self.window_handles[-1])
