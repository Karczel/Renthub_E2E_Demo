from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from common_steps import log_in


class Browser:
    """Provide access to an instance of a Selenium web driver."""

    @classmethod
    def get_browser(cls):
        """Class method to initialize a headless Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    @classmethod
    def get_logged_in_browser(username, password):
        """Class method to initialize a headless driver and log in."""
        driver = Browser.get_browser()
        log_in(driver, username, password)
        return driver
