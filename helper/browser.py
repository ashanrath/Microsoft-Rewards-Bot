import logging
import os
import platform
import time
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, \
    ElementClickInterceptedException, ElementNotVisibleException, \
    ElementNotInteractableException, NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from helper.driver import download_driver

class Browser(webdriver.Chrome):
    def __init__(self, headless_mode: bool, user_agent):
        self.mobile_mode = 'android' in user_agent.lower()
        self.user_agent = user_agent
        
        path = Browser._prepare_driver()

        options = self._get_driver_options()

        prefs = {
            "profile.default_content_setting_values.geolocation": 2, 
            "profile.default_content_setting_values.notifications": 2
        }

        options.add_experimental_option("prefs", prefs)

        if headless_mode:
            options.add_argument('--headless')

        super().__init__(path, options=options)

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
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('w3c', False)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return options

    def _is_same_ua(self, user_agent):
        return user_agent == self.user_agent

    def find_by_id(self, obj_id):
        """
        Searches for elements matching ID
        :param obj_id:
        :return: List of all nodes matching provided ID
        """
        return self.find_elements_by_id(obj_id)


    def find_by_xpath(self, selector):
        """
        Finds elements by xpath
        :param selector: xpath string
        :return: returns a list of all matching selenium objects
        """
        return self.find_elements_by_xpath(selector)


    def find_by_class(self, selector):
        """
        Finds elements by class name
        :param selector: Class selector of html obj
        :return: returns a list of all matching selenium objects
        """
        return self.find_elements_by_class_name(selector)


    def find_by_css(self, selector):
        """
        Finds nodes by css selector
        :param selector: CSS selector of html node obj
        :return: returns a list of all matching selenium objects
        """
        return self.find_elements_by_css_selector(selector)

    def wait_until_visible(self, by_:By, selector, time_to_wait=10, raise_exc=False, silent=True):
        """
        Searches for selector and if found, end the loop
        Else, keep repeating every 2 seconds until time elapsed, then refresh page
        :param by_: string which tag to search by
        :param selector: string selector
        :param time_to_wait: int time to wait
        :return: Boolean if selector is found
        """
        start_time = time.time()
        while (time.time() - start_time) < time_to_wait:
            if self.find_elements(by=by_, value=selector):
                return True
            self.refresh()  # for other checks besides points url
            time.sleep(2)
        
        msg = f'{selector} element not visible - Timeout Exception'
        self.screenshot(selector)
        if raise_exc:
            raise TimeoutException(msg)
        logging.exception(msg=msg, exc_info=False)
        return False


    def wait_until_clickable(self, by_:By, selector, time_to_wait=10, raise_exc=False):
        """
        Waits 5 seconds for element to be clickable
        :param by_:  BY module args to pick a selector
        :param selector: string of xpath, css_selector or other
        :param time_to_wait: Int time to wait
        :return: None
        """
        try:
            WebDriverWait(self, time_to_wait).until(
                ec.element_to_be_clickable((by_, selector)))
        except TimeoutException:
            msg = f'{selector} element not clickable - Timeout Exception'
            self.screenshot(selector)
            if raise_exc:                
                raise TimeoutException(msg)
            logging.exception(msg=msg, exc_info=False)
        except UnexpectedAlertPresentException:
            # FIXME
            self.switch_to.alert.dismiss()
            # logging.exception(msg=f'{selector} element Not Visible - Unexpected Alert Exception', exc_info=False)
            # screenshot(selector)
            # browser.refresh()
        except WebDriverException:
            logging.exception(msg=f'Webdriver Error for {selector} object')
            self.screenshot(selector)


    def send_key_by_name(self, name, key) -> bool:
        """
        Sends key to target found by name
        :param name: Name attribute of html object
        :param key: Key to be sent to that object
        :return: True if successful else False
        """
        try:
            self.find_element_by_name(name).send_keys(key)
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(
                msg=f'Send key by name to {name} element not visible or clickable.', exc_info=False)
        except NoSuchElementException:
            logging.exception(msg=f'Send key to {name} element, no such element.', exc_info=False)
            self.screenshot(name)
            self.refresh()
        except WebDriverException:
            logging.exception(msg=f'Webdriver Error for send key to {name} object')
        finally:
            return False


    def send_key_by_id(self, obj_id, key) -> bool:
        """
        Sends key to target found by id
        :param obj_id: ID attribute of the html object
        :param key: Key to be sent to that object
        :return: True if successful else False
        """
        try:
            self.find_element_by_id(obj_id).send_keys(key)
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(
                msg=f'Send key by ID to {obj_id} element not visible or clickable.', exc_info=False)
        except NoSuchElementException:
            logging.exception(
                msg=f'Send key by ID to {obj_id} element, no such element.', exc_info=False)
            self.screenshot(obj_id)
            self.refresh()
        except WebDriverException:
            logging.exception(
                msg=f'Webdriver Error for send key by ID to {obj_id} object')
        finally:
            return False


    def click_by_class(self, selector) -> bool:
        """
        Clicks on node object selected by class name
        :param selector: class attribute
        :return: True if click was successful, else False
        """
        try:
            self.find_element_by_class_name(selector).click()
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(
                msg=f'Send key by class to {selector} element not visible or clickable. Attempting JS Click', exc_info=False)
            self.js_click(self.find_element_by_class_name(selector))
        except NoSuchElementException:
            logging.debug(
                msg=f'Send key by class to {selector} element, no such element.', exc_info=False)
        except WebDriverException:
            logging.exception(
                msg=f'Webdriver Error for send key by class to {selector} object')
        finally:
            return False


    def click_by_id(self, obj_id) -> bool:
        """
        Clicks on object located by ID
        :param obj_id: id tag of html object
        :return: True if click is successful, else False
        """
        try:
            self.find_element_by_id(obj_id).click()
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.exception(
                msg=f'Click by ID to {obj_id} element not visible or clickable. Attempting JS Click', exc_info=False)
            self.js_click(self.find_element_by_id(obj_id))
        except NoSuchElementException:
            logging.debug(
                msg=f'Click by ID to {obj_id} element, no such element.', exc_info=False)
        except WebDriverException:
            logging.exception(
                msg=f'Webdriver Error for click by ID to {obj_id} object')
        finally:
            return False


    def click_by_xpath(self, xpath) -> bool:
        """
        Clicks on object located by XPATH
        :param xpath: xpath tag of html object
        :return: True if click is successful, else False
        """
        try:
            self.find_element_by_xpath(xpath).click()
            return True
        except (ElementNotVisibleException, ElementClickInterceptedException, ElementNotInteractableException):
            logging.warning(
                msg=f'Click by xpath to {xpath} element not visible or clickable. Attempting JS Click', exc_info=False)
            self.js_click(self.find_element_by_xpath(xpath))
        except NoSuchElementException:
            logging.debug(
                msg=f'Click by xpath to {xpath} element, no such element.', exc_info=False)
        except WebDriverException:
            logging.exception(
                msg=f'Webdriver Error for click by xpath to {xpath} object')
        finally:
            return False

    def clear_by_id(self, obj_id) -> bool:
        """
        Clear object found by id
        :param obj_id: ID attribute of html object
        :return: True if clear is successful, else False
        """
        try:
            self.find_element_by_id(obj_id).clear()
            return True
        except (ElementNotVisibleException, ElementNotInteractableException):
            logging.warning(
                msg=f'Clear by ID to {obj_id} element not visible or clickable.', exc_info=False)
        except NoSuchElementException:
            logging.exception(
                msg=f'Send key by ID to {obj_id} element, no such element', exc_info=False)
            self.screenshot(obj_id)
            self.refresh()
        except WebDriverException:
            logging.exception(msg='Error.')
        finally:
            return False


    def js_click(self, element):
        """Click any given element"""
        try:
            self.execute_script("arguments[0].click();", element)
        except Exception as e:
            logging.exception(msg=f'Exception when JS click')


    def screenshot(self, selector):
        """
        Snaps screenshot of webpage when error occurs
        :param selector: The name, ID, class, or other attribute of missing node object
        :return: None
        """
        logging.exception(msg=f'{selector} cannot be located.')
        screenshot_file_name = f'{datetime.now().strftime("%Y%m%d%%H%M%S")}_{selector}.png'
        screenshot_file_path = os.path.join('logs', screenshot_file_name)
        self.save_screenshot(screenshot_file_path)

    def scroll_to_bottom(self):
        """Scroll to bottom of the page"""
        try:
            self.execute_script("scrollBy(0,250);")
            self.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print('Exception when scrolling : %s' % e)

    def scroll_to_top(self):
        """Scroll to top of the page"""
        try:
            self.find_element_by_tag_name('body').send_keys(Keys.HOME)
        except Exception as e:
            print('Exception when scrolling : %s' % e)

    def open_in_new_tab(self, url):
        """
        Opens the url in and switch focus to a new tab
        :return: None
        """
        self.execute_script("window.open('');")
        self.goto_latest_window()
        self.get(url)

    def goto_main_window(self):
        """
        Closes current window and switches focus back to main window
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
