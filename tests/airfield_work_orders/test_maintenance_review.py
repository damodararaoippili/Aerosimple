import pytest
from utils.read_test_data import read_test_case_data
from pages.airfield_work_orders.maintenance_review import WO_Maintenance
from utils.screenshot import capture_screenshot
from utils.logger import get_logger

def test_maintenance_review(login_page):
    browser = login_page
    wo_maintenance = WO_Maintenance(browser)
    logger = get_logger("maintenance_review")

    try:
        test_data = read_test_case_data('AWO', 'TC_ID_002')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')
        time = test_data.get('Time')
        status = test_data.get('Status')

        wo_maintenance.close_feedback_modal_if_present()

        wo_maintenance.click_on_apps()
        logger.info("Clicked on Apps button.")

        wo_maintenance.click_on_module(module)
        logger.info(f"Clicked on module: {module}")

        wo_maintenance.click_on_sub_module(sub_module)
        logger.info(f"Clicked on sub module: {sub_module}")

        if wo_maintenance.work_order_status(status):
            logger.info(f"Found work order with status: {status}")
            wo_maintenance.click_on_view()
            logger.info("Clicked on View button")

            wo_maintenance.enter_description_of_work_done('Dead bird on runway is removed')
            logger.info("Entered description of work done.")

            wo_maintenance.click_on_resolve()
            logger.info("Clicked on Resolve")

            if wo_maintenance.validate_message():
                logger.info("Validation message received.")
                wo_maintenance.click_on_OK()
                logger.info("Clicked OK after validation")

                wo_maintenance.enter_input_time('3')
                logger.info("Entered time: 3")

                wo_maintenance.click_add_button()
                logger.info("Clicked Add button")

                wo_maintenance.click_on_save()
                logger.info("Clicked Save button")

                wo_maintenance.click_on_resolve()
                logger.info("Final resolve clicked.")
            else:
                logger.warning("Validation message not shown after resolve.")
        else:
            logger.warning(f"No work order found with status: {status}")
            pytest.skip(f"Skipping test — No work order found with status: {status}")

    except Exception as e:
        capture_screenshot(browser, name="maintenance_review_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(str(e))
