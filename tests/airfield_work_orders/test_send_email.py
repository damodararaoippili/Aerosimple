import pytest
from pages.airfield_work_orders.send_email import Send_email
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot

def test_send_email(login_page):
    browser = login_page
    send_email = Send_email(browser)
    logger = get_logger("send_email")

    try:
        test_data = read_test_case_data('AWO', 'TC_ID_002')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')
        logger.info(f"Navigating to module: {module}, sub-module: {sub_module}")

        send_email.close_feedback_modal_if_present()
        logger.info("Closed feedback modal if present.")

        send_email.click_on_apps()
        logger.info("Clicked on Apps.")

        send_email.click_on_module(module)
        logger.info(f"Clicked on module: {module}")

        send_email.click_on_sub_module(sub_module)
        logger.info(f"Clicked on sub-module: {sub_module}")

        current_status = send_email.work_order_status()
        logger.info(f"Current Work Order status: {current_status}")

        all_status = ['Maintenance Review', 'In Progress', 'On Hold', 'Monitor Mode', 'Awaiting Parts']
        for status in all_status:
            if status == current_status:
                logger.info(f"Found matching status: {status}, proceeding to view.")
                send_email.click_on_view(status)
                break
            else:
                logger.info(f"Status '{status}' does not match current status.")

        send_email.click_on_Actions()
        logger.info("Clicked on Actions.")

        send_email.click_on_action_items('Send Email')
        logger.info("click on 'Send Email' option under action.")

        send_email.Email_Recipients()
        logger.info("Opened Email Recipients dropdown.")

        user = 'Prasad QA'
        send_email.select_user_and_role(user)
        logger.info(f"Selected user or role: {user}")

        external_email = "damodar@aerosimple.in"
        send_email.External_Emails(external_email)
        logger.info(f"Entered external email: {external_email}")

        send_email.click_on_send_button()
        logger.info("Clicked on Send button to submit email.")

    except Exception as e:
        capture_screenshot(browser, name="send_email_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
