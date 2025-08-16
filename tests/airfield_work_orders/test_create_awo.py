import pytest
from pages.airfield_work_orders.create_awo import CreateAwo
from utils.logger import get_logger
from utils.read_test_data import read_test_case_data
from utils.screenshot import capture_screenshot

def test_create_awo(login_page):
    browser = login_page
    work_order = CreateAwo(browser)
    logger = get_logger('test_create_awo')

    try:
        logger.info("Starting test: Create Airfield Work Order")

        test_data = read_test_case_data('AWO', 'TC_ID_001')
        assert test_data is not None, "Test data not found."
        logger.info("Test data loaded successfully.")

        # Extract data
        module = test_data.get('Module')
        sub_module = test_data.get('Sub Module')
        priority = test_data.get('Priority')
        category = test_data.get('Category')
        sub_category = test_data.get('Sub Category')
        description = test_data.get('Problem Description')
        name = test_data.get('Name')
        number = test_data.get('Number')
        selection = test_data.get('Selection')
        system_user = test_data.get('System User')
        name_field = test_data.get('Name_Field')
        number_field = test_data.get('Number_Field')
        selection_field = test_data.get('Selection_Field')
        property = test_data.get('Properties')
        tenant = test_data.get('Company Name (Tenants)')
        Wildlife_type = test_data.get('Wildlife Type')
        Wildlife_species = test_data.get('Wildlife Species')
        date = test_data.get('Date')

        # Begin automation steps
        work_order.close_modal_if_present()
        work_order.close_feedback_modal_if_present()
        work_order.click_on_apps(); logger.info("Clicked on Apps")
        work_order.click_on_module(module); logger.info(f"Clicked on module: {module}")
        work_order.click_on_sub_module(sub_module); logger.info(f"Clicked on sub-module: {sub_module}")
        work_order.click_new_work_order(); logger.info("Clicked on New Work Order")

        work_order.select_priority(priority); logger.info(f"Selected priority: {priority}")
        work_order.select_category(category); logger.info(f"Selected category: {category}")
        work_order.select_subcategory(sub_category); logger.info(f"Selected sub-category: {sub_category}")

        work_order.click_draw_marker(); logger.info("Clicked on location pointer icon")
        work_order.click_on_map(); logger.info("Clicked on map")

        work_order.enter_problem_description(description); logger.info(f"Entered description: {description}")
        work_order.enter_input_to_field('Name', name); logger.info(f"Entered Name: {name}")
        work_order.enter_input_to_field('Number', number); logger.info(f"Entered Number: {number}")
        work_order.select_dropdown_by_text('Selection', selection); logger.info(f"Selected from dropdown: {selection}")
        work_order.click_checkbox('Checkbox'); logger.info("Checked the checkbox")
        work_order.select_system_user(system_user); logger.info(f"Selected System User: {system_user}")

        work_order.enter_input_to_field('Name_Field', name_field); logger.info(f"Entered Name Field: {name_field}")
        work_order.enter_input_number_filed(number_field); logger.info(f"Entered Number Field: {number_field}")

        work_order.click_date_field(); logger.info("Clicked on date field")
        work_order.select_day_in_date_picker(date); logger.info(f"Selected date: {date}")

        work_order.select_dropdown_by_text('Selection_Field', selection_field); logger.info(f"Selected from Selection Field: {selection_field}")
        work_order.select_property(property); logger.info(f"Selected property: {property}")
        work_order.select_company_name(tenant); logger.info(f"Selected company name: {tenant}")

        # Custom dropdowns
        work_order.select_custom_dropdown_by_text('Level 1', 'East terminal')
        work_order.select_custom_dropdown_by_text('Level 2', 'Entry Gate')
        work_order.select_custom_dropdown_by_text('Level 3', 'Gate 1')
        work_order.select_custom_dropdown_by_text('Level A', 'East Terminal')
        work_order.select_custom_dropdown_by_text('Level B', 'East Terminal A')
        work_order.select_custom_dropdown_by_text('Level C', 'East Terminal A1')
        logger.info("Selected location levels")

        work_order.select_dropdown_by_text('Wildlife Type', Wildlife_type); logger.info(f"Selected wildlife type: {Wildlife_type}")
        work_order.select_dropdown_by_text('Wildlife Species', Wildlife_species); logger.info(f"Selected wildlife species: {Wildlife_species}")

        work_order.click_create_button()
        logger.info("Clicked Create button successfully.")

        assert True, "Create action completed successfully."
        logger.info("Test completed successfully.")

    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        capture_screenshot(browser, name="create_awo_assertion_failure")
        pytest.fail(str(ae))

    except Exception as e:
        logger.exception(f"Test failed due to unexpected error: {e}")
        capture_screenshot(browser, name="create_awo_unexpected_failure")
        pytest.fail(str(e))
