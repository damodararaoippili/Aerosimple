import pytest
from pages.airfield_work_orders.operation_review import Operation_review
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot
from utils.logger import get_logger

def test_operation_review(login_page):
    browser = login_page
    op_review = Operation_review(browser)
    logger = get_logger("operation_review")

    try:
        test_data = read_test_case_data('AWO', 'TC_ID_004')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')
        status = test_data.get('Status')
        review_report = test_data.get('Review Report')

        op_review.close_modal_if_present()
        logger.info("Closed modal if present.")

        op_review.close_feedback_modal_if_present()

        op_review.click_on_apps()
        logger.info("Clicked on Apps.")

        op_review.click_on_module(module)
        logger.info(f"Clicked on module: {module}")

        op_review.click_on_sub_module(sub_module)
        logger.info(f"Clicked on sub module: {sub_module}")

        if op_review.work_order_status(status):
            logger.info(f"Found work order with status: {status}")

            op_review.click_on_view(status)
            logger.info("Clicked on view.")

            op_review.page_refresh()
            logger.info("Page refreshed.")

            op_review.click_on_review_report(review_report)
            logger.info(f"Selected review report: {review_report}")

            op_review.click_on_close_work_order()
            logger.info("Clicked on close work order.")

        else:
            logger.warning(f"No work order found with status: {status}")
            pytest.skip(f"Skipping test — Work order with status '{status}' not found.")

    except Exception as e:
        capture_screenshot(browser, name="operation_review_failure")
        logger.exception(f"Test failed due to unexpected error: {str(e)}")
        pytest.fail(str(e))
