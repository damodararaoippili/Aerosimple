import pytest
from pages.airfield_work_orders.send_back import Send_Back
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot
from utils.logger import get_logger

def test_send_back_maintenance(login_page):
    browser = login_page
    send_back = Send_Back(browser)
    logger = get_logger("send_back_to_maintenance")

    try:
        test_data = read_test_case_data('AWO', 'TC_ID_003')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        send_back.close_modal_if_present()
        logger.info("Closed modal if present.")

        send_back.close_feedback_modal_if_present()

        send_back.click_on_apps()
        logger.info("Clicked on Apps.")

        send_back.click_on_module(module)
        logger.info(f"Clicked on module: {module}")

        send_back.click_on_sub_module(sub_module)
        logger.info(f"Clicked on sub module: {sub_module}")

        status = 'Operations Review'
        if send_back.work_order_status(status):
            logger.info(f"Work order with status '{status}' found.")

            send_back.click_on_view(status)
            logger.info("Clicked on View.")

            send_back.click_on_actions()
            logger.info("Clicked on Actions.")

            send_back.click_on_send_back()
            logger.info("Clicked on Send Back.")

            send_back.verify_send_back_model()
            logger.info("Send back modal verified.")

            send_back.send_back_description('need to check the checklist properly')
            logger.info("Entered send back description.")

            send_back.click_on_send_back_button()
            logger.info("Clicked on Send Back button.")
        else:
            logger.warning(f"Work order with status '{status}' not found.")
            pytest.skip(f"Skipping test — Work order with status '{status}' not found.")

    except Exception as e:
        capture_screenshot(browser, name="send_back_to_maintenance_failure")
        logger.exception(f"Test failed due to unexpected error: {str(e)}")
        pytest.fail(str(e))
