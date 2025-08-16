import pytest
from pages.airfield_work_orders.create_awo import CreateAwo
from pages.non_airfield_work_orders.create_nawo import Create_NAWO
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot

def test_create_awo(login_page):
    browser = login_page
    work_order = Create_NAWO(browser)
    logger = get_logger('test_create_nwo')
    try:
        logger.info("Starting test: Create Airfield Work Order")

        test_data = read_test_case_data('AWO', 'TC_ID_001')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")
        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')
        work_order.click_on_module(module)
        work_order.click_on_sub_module(sub_module)
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        capture_screenshot(browser, name="create_awo_assertion_failure")
        pytest.fail(str(ae))

    except Exception as e:
        logger.exception(f"Test failed due to unexpected error: {e}")
        capture_screenshot(browser, name="create_awo_unexpected_failure")
        pytest.fail(str(e))