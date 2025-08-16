import pytest
from pages.airfield_work_orders.reassignment import Reassignment
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot

def test_reassignment(login_page):
    browser = login_page
    wo_reassignment=Reassignment(browser)
    logger = get_logger("test_reassignment")

    try:
        test_data = read_test_case_data('AWO', 'TC_ID_005')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        status_to_update = 'In Progress'
        reassignment = test_data.get('Reassignment')

        wo_reassignment.close_feedback_modal_if_present()

        wo_reassignment.click_on_apps()
        logger.info("Clicked on Apps.")

        wo_reassignment.click_on_module(module)
        logger.info(f"Clicked on Module: {module}")

        wo_reassignment.click_on_sub_module(sub_module)
        logger.info(f"Clicked on Sub Module: {sub_module}")

        wo_reassignment.click_on_filters()
        logger.info("click on filters")

        wo_reassignment.click_on_clear_filters()
        logger.info('click on clear filters')

        wo_reassignment.click_on_apply()
        logger.info('click on apply ')

        work_order_number = wo_reassignment.work_order()
        status = wo_reassignment.work_order_status()
        logger.info(f'current status of work order {work_order_number} is in {status}')

        wo_reassignment.click_on_view(status)
        logger.info(f"Viewed work order with status: {status}")

        wo_reassignment.click_reassignment()
        logger.info('click on reassignment')

        wo_reassignment.click_on_search()
        logger.info('click on search option')

        wo_reassignment.enter_input_to_search_option(reassignment)
        logger.info(f'enter input to search option:{reassignment}')

        wo_reassignment.click_on_assign()
        logger.info('click on assign')

        wo_reassignment.click_on_save()
        logger.info('click on save button')

        user_name = wo_reassignment.verify_assigned_user()
        assert user_name == reassignment, f"Assigned user mismatch: expected '{reassignment}', got '{user_name}'"
        logger.info(f"Successfully reassigned to: {user_name}")

    except Exception as e:
        capture_screenshot(browser, name="reassignment_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
