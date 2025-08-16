import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from pages.login_page import Login
from utils.logger import get_logger
from utils.read_test_data import read_login_data
from utils.screenshot import capture_screenshot

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="false")
    parser.addoption("--environment_url", action="store", default="staging")

@pytest.fixture
def get_browser(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    environment_url = request.config.getoption("--environment_url")
    url = {
        "dev": "https://app.dev.aerosimple.com",
        "test": "https://app.test.aerosimple.com",
        "staging": "https://app.staging.aerosimple.com",
        "production": "https://app.aerosimple.com"
    }

    current_url = url.get(environment_url)
    logger = get_logger("browser_setup")

    try:
        logger.info(f"Starting browser: {browser}, Headless: {headless}, URL: {current_url}")
        if browser == "chrome":
            options = ChromeOptions()
            if headless.lower() == "true":
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)

        elif browser == "edge":
            options = EdgeOptions()
            if headless.lower() == "true":
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.get(current_url)
        driver.maximize_window()
        logger.info("Browser launched and maximized.")
        yield driver

    except Exception as e:
        logger.exception(f"Error during browser setup: {e}")
        if 'driver' in locals():
            capture_screenshot(driver, name="browser_setup_failure")
        raise
    finally:
        if 'driver' in locals():
            driver.quit()
            logger.info("Browser closed.")


@pytest.fixture
def login_page(get_browser):
    browser = get_browser
    logger = get_logger("test_login")

    try:
        test_data = read_login_data('Login')
        Email = test_data.get('Email_ID')
        Password = test_data.get('Password')
        logger.info(f"Loaded login test data for user: {Email}")

        login = Login(browser)

        login.click_on_next()
        logger.info("Clicked on 'Next' (Email step)")

        login.check_validation()
        logger.info("Validated mandatory field")

        login.enter_email(Email)
        logger.info(f"Entered email: {Email}")

        login.click_on_next()
        logger.info("Clicked on 'Next' (Password step)")

        login.close_modal_if_present()

        login.click_on_next()
        login.check_validation()
        login.enter_password(Password)
        logger.info("Entered password")

        login.click_on_next()
        logger.info("Clicked final 'Next' to login")

        return browser

    except Exception as e:
        logger.exception(f"Login fixture failed: {e}")
        capture_screenshot(browser, name="login_fixture_failure")
        raise
