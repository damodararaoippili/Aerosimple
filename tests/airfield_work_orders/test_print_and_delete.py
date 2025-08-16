import pytest
from pages.airfield_work_orders.print_and_delete import Print_and_Delete_inspection
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot
def test_print_and_delete(login_page):
    browser = login_page
    print_and_delete_inspection = Print_and_Delete_inspection(browser)
    logger = get_logger("test_print_and_delete")
    try:
        test_data = read_test_case_data('AWO', 'TC_ID_005')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        print_and_delete_inspection.close_feedback_modal_if_present()

        print_and_delete_inspection.click_on_apps()
        logger.info("Clicked on Apps.")

        print_and_delete_inspection.click_on_module(module)
        logger.info(f"Clicked on Module: {module}")

        print_and_delete_inspection.click_on_sub_module(sub_module)
        logger.info(f"Clicked on Sub Module: {sub_module}")

        print_and_delete_inspection.click_on_filters()
        logger.info("click on filters")

        print_and_delete_inspection.click_on_clear_filters()
        logger.info('click on clear filters')

        print_and_delete_inspection.click_on_apply()
        logger.info('click on apply ')

        work_order_number = print_and_delete_inspection.work_order()
        status = print_and_delete_inspection.work_order_status()
        logger.info(f'current status of work order {work_order_number} is in {status}')

        print_and_delete_inspection.click_on_view(status)
        logger.info(f"Viewed work order with status: {status}")

        print_and_delete_inspection.click_on_Actions()
        logger.info('click on Actions')

        clicked_text = print_and_delete_inspection.click_on_action_items('Print')
        if clicked_text:
            logger.info(f"Clicked on action item: {clicked_text}")
        else:
            logger.error("Failed to click on any action item.")
        clicked_text = print_and_delete_inspection.click_on_action_items('Delete')
        if clicked_text:
            logger.info(f"Clicked on action item: {clicked_text}")
        else:
            logger.error("Failed to click on any action item.")
        print_and_delete_inspection.enter_input_to_delete('DELETE')
        logger.info('click and enter input to delete field : DELETE')

        print_and_delete_inspection.click_on_confirm_delete()
        logger.info('click on Confirm Delete')

    except Exception as e:
        capture_screenshot(browser, name="print_and_delete_inspection_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
