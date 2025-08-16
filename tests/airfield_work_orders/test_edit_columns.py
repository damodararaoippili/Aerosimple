import time
import pytest
from pages.airfield_work_orders.edit_columns import Edit_columns
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from pages.airfield_work_orders.export_to_excel import wait_without_sleep
from utils.screenshot import capture_screenshot

def test_edit_column(login_page):
    browser = login_page
    edit_columns = Edit_columns(browser)
    logger = get_logger("edit columns")
    try:
        test_data = read_test_case_data('AWO', 'TC_ID_002')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")
        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        edit_columns.click_on_apps()
        logger.info('click on apps button')

        edit_columns.click_on_module(module)
        logger.info(f'click on module: {module}')

        edit_columns.click_on_sub_module(sub_module)
        logger.info(f'click on sub module :{sub_module}')

        wait_without_sleep(browser, 5)

        headers = edit_columns.header_edit_columns()
        logger.info(f'edit columns:{headers}')

        edit_columns.click_on_Actions()
        logger.info('click on Actions')

        edit_columns.click_on_edit_columns()
        logger.info('click on edit columns')

        text = 'Description'

        edit_columns.click_on_edit_column_search(text)
        logger.info('failed to click and enter input to search bar')

        edit_columns.click_on_select_edit_columns('Description')
        logger.info(f'failed to select edit column :{text}')

        edit_columns.click_on_Apply()
        logger.info('failed to click on apply button')

        headers= edit_columns.header_edit_columns()
        logger.info(f'edit columns:{headers}')

        time.sleep(50)

    except Exception as e:
        capture_screenshot(browser, name="edit_column_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
