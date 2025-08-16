import pytest
from pages.airfield_work_orders.edit_work_orders import Edit_work_order
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot
def test_edit_work_order(login_page):
    browser = login_page
    edit_work_order = Edit_work_order(browser)
    logger = get_logger("test_edit_inspection")
    try:
        test_data = read_test_case_data('AWO', 'TC_ID_005')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        edit_work_order.close_feedback_modal_if_present()

        edit_work_order.click_on_apps()
        logger.info("Clicked on Apps.")

        edit_work_order.click_on_module(module)
        logger.info(f"Clicked on Module: {module}")

        edit_work_order.click_on_sub_module(sub_module)
        logger.info(f"Clicked on Sub Module: {sub_module}")

        edit_work_order.click_on_filters()
        logger.info("click on filters")

        edit_work_order.click_on_clear_filters()
        logger.info('click on clear filters')

        edit_work_order.click_on_apply()
        logger.info('click on apply ')

        work_order_number = edit_work_order.work_order()
        status = edit_work_order.work_order_status()
        logger.info(f'current status of work order {work_order_number} is in {status}')

        edit_work_order.click_on_view(status)
        logger.info(f"Viewed work order with status: {status}")

        edit_work_order.click_on_Actions()
        logger.info('click on Actions')

        clicked_text = edit_work_order.click_on_action_items('Edit')
        if clicked_text:
            logger.info(f"Clicked on action item: {clicked_text}")
        else:
            logger.error("Failed to click on any action item.")
        edit_work_order.click_on_update()
        logger.info('click on update status')
    except Exception as e:
        capture_screenshot(browser, name="edit_work_order_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")


