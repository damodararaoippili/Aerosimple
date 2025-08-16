import time

import pytest
from pages.airfield_work_orders.status_update import Status_update
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot
from utils.logger import get_logger

def test_update_status(login_page):
    browser = login_page
    update_status = Status_update(browser)
    logger = get_logger("update_status")

    try:
        test_data = read_test_case_data('AWO', 'TC_ID_002')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        status_to_update = 'In Progress'

        update_status.click_on_apps()
        logger.info("Clicked on Apps.")

        update_status.click_on_module(module)
        logger.info(f"Clicked on Module: {module}")

        update_status.click_on_sub_module(sub_module)
        logger.info(f"Clicked on Sub Module: {sub_module}")

        update_status.click_on_filters()
        logger.info("click on filters")

        update_status.click_on_clear_filters()
        logger.info('click on clear filters')

        update_status.click_on_apply()
        logger.info('click on apply ')

        list_of_status = ["In Progress","Maintenance Review", "On Hold", "Monitor Mode", "Awaiting Parts"]
        for status in list_of_status:
            result = update_status.work_order_status(status)
            logger.info(f"Work order with status '{status}' found and opened")
            if result:
                print(f"[✓] Work order with status '{status}' found and opened.")
                break
        else:
            print("[x] No work order found for any of the expected statuses.")
            logger.info("No work order found for any of the expected statuses")

        update_status.click_on_update_status()
        logger.info('click on update status')

        for status in list_of_status:
            if status == 'Maintenance Review':
                status_to_update = 'In Progress'
            elif status == 'In Progress':
                status_to_update = 'On Hold'
            elif status == 'On Hold':
                status_to_update = 'Remove Hold'
            elif status == 'Monitor Mode':
                status_to_update = 'Remove Monitor Mode'
            elif status == 'Awaiting Parts':
                status_to_update = 'In Progress'

        update_status.click_on_status(status_to_update)
        logger.info(f"work order update status :{status_to_update}")
        time.sleep(10)


    except Exception as e:
        capture_screenshot(browser, name="update_status_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
