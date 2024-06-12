import time
import traceback

from retrying import retry
import binascii

from quantplay.utils.selenium_utils import Selenium
from quantplay.exception.exceptions import (
    InvalidArgumentException,
    RetryableException,
    BrokerException,
    retry_exception,
    WrongLibrarySetup,
)
import pyotp
from selenium.common.exceptions import WebDriverException, NoSuchElementException


class AliceblueLogin:
    @staticmethod
    def check_error(page_source):
        for error_message in [
            "User profile not found",
            "Invalid username or password",
            "Invalid TOTP",
        ]:
            if error_message in page_source:
                raise InvalidArgumentException(error_message)

        if "Invalid" in page_source:
            start_index = page_source.find("Invalid")
            print(page_source[start_index : min(start_index + 20, len(page_source))])

        if "Invalid" in page_source and "api_key":
            raise InvalidArgumentException(f"Invalid API Key")

    def click_on_login(driver):
        login = '//*[@id="login_card_inital"]/div[6]/button'
        login = driver.find_element("xpath", login)
        login.click()

    def enter_user_id(driver, user_id):
        time.sleep(0.5)
        user_id_xpath = '//*[@id="userid_inp"]'
        driver.find_element("xpath", user_id_xpath).send_keys(user_id)

        time.sleep(0.5)
        next_xpath = '//*[@id="userId_btn_label"]'
        driver.find_element("xpath", next_xpath).click()

    def enter_password(driver, password):
        time.sleep(0.5)
        password_xpath = '//*[@id="password_inp"]'
        driver.find_element("xpath", password_xpath).send_keys(password)

        time.sleep(0.5)
        next_xpath = '//*[@id="password_btn"]'
        driver.find_element("xpath", next_xpath).click()

    def enter_totp(driver, totp):
        time.sleep(1.5)
        totp_xpath = '//*[@id="totp_otp_inp"]'
        driver.find_element("xpath", totp_xpath).send_keys(totp)

        # time.sleep(0.5)
        # next_xpath = '//*[@id="totp_btn"]'
        # driver.find_element("xpath", next_xpath).click()

    @staticmethod
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def login(user_id, password, totp):
        try:
            driver = Selenium().get_browser(headless=True)

            # TODO api should be fetched from configuration

            driver.get("https://ant.aliceblueonline.com/")
            AliceblueLogin.click_on_login(driver)
            AliceblueLogin.enter_user_id(driver, user_id)
            AliceblueLogin.enter_password(driver, password)
            AliceblueLogin.enter_totp(driver, pyotp.TOTP(totp).now())

        except binascii.Error as e:
            raise InvalidArgumentException("Invalid TOTP key provided")
        except InvalidArgumentException as e:
            raise
        except NoSuchElementException as e:
            raise BrokerException(
                "Login to Aliceblue failed. Please log in manually to generate a new token"
            )
        except WebDriverException as e:
            traceback.print_exc()
            raise RetryableException("Selenium setup need to be fixed")
        except Exception as e:
            print(traceback.print_exc())
            raise RetryableException(str(e))
