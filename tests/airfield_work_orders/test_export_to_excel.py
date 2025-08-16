import pytest
from pages.airfield_work_orders.export_to_excel import Export_to_Excel, wait_without_sleep
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot

def test_export_excel(login_page):
    browser = login_page
    export_excel = Export_to_Excel(browser)
    logger = get_logger("export to excel")
    try:
        test_data = read_test_case_data('AWO', 'TC_ID_002')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')

        export_excel.click_on_apps()
        logger.info("Clicked on Apps.")

        export_excel.click_on_module(module)
        logger.info(f"Clicked on Module: {module}")

        export_excel.click_on_sub_module(sub_module)
        logger.info(f"Clicked on Sub Module: {sub_module}")

        wait_without_sleep(browser, 5)

        export_excel.click_on_Actions()
        logger.info('click on Actions')

        export_excel.click_on_export_to_excel()
        logger.info('click on export to excel')

        export_excel.click_on_selected_columns()
        logger.info('click on Export Selected Columns')

        wait_without_sleep(browser, 5)

        export_excel.click_on_Export_all()
        logger.info('click on Export All Columns')

        wait_without_sleep(browser, 5)

    except Exception as e:
        capture_screenshot(browser, name="update_status_failure")
        logger.exception(f"Test failed due to unexpected error: {e}")
        pytest.fail(f"Test failed due to unexpected error: {e}")
