from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class CreateAwo:
    def __init__(self, browser):
        self.browser = browser

        self.apps_locators = [
            (By.XPATH, "//div[@class='topbar_menu__3MEY5']//button[span[text()='apps']]"),
            (By.XPATH, "//button[span[text()='apps']]"),
            (By.XPATH, "//button[.//span[contains(text(),'apps')]]"),
            (By.XPATH, "//span[text()='apps']/parent::button"),
            (By.XPATH, "//img[@alt='menu']/following-sibling::span[text()='apps']/parent::button")
        ]

        self.asset_dropdown = (By.NAME, "select-field-asset")
        self.checkbox = (By.XPATH,"//span[text()='Checkbox']/../..//input")
        self.system_user =(By.XPATH,"//span[text()='System User']/../..//div[@class=' css-1hwfws3']")

    def find_element_with_fallback(self, locators, wait_time=10):
        for by, value in locators:
            try:
                element = WebDriverWait(self.browser, wait_time).until(EC.presence_of_element_located((by, value)))
                print(f"[Self-Healing] Found using: ({by}, {value})")
                return element
            except:
                print(f"[Self-Healing] Failed: ({by}, {value})")
        raise Exception("Element not found with any locator.")

    def close_modal_if_present(self):
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
            close_button = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal']//button[text()='Close']")))
            close_button.click()
            WebDriverWait(self.browser, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
            print("Modal closed successfully.")
        except Exception:
            print("Modal not found or already closed.")

    def close_feedback_modal_if_present(self):
        try:
            close_button = self.browser.find_element(By.XPATH,"//div[contains(@class, 'modal_content')]//button[normalize-space()='×']")
            close_button.click()
            print("Modal found and closed.")
        except NoSuchElementException:
            print("Modal not present, skipping.")

    def click_on_apps(self):
        try:
            apps_button = self.find_element_with_fallback(self.apps_locators)
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(apps_button))
            apps_button.click()
            print("Clicked on 'apps' button successfully.")
        except Exception as e:
            assert False, f"Failed to click on 'apps' button: {e}"

    def click_on_module(self, module_text):
        locators = [
            (By.XPATH, f"//div[@class='menu1_first__30gkj']//span[text()='{module_text}']/../../../.."),
            (By.XPATH, f"//span[text()='{module_text}']/ancestor::div[contains(@class, 'menu')]"),
            (By.XPATH, f"//span[text()='{module_text}']/ancestor::button"),
            (By.XPATH, f"//*[text()='{module_text}']/ancestor::*[contains(@class,'menu')]"),]
        module = self.find_element_with_fallback(locators)
        module.click()

    def click_on_sub_module(self, sub_module_text):
        locators = [
            (By.XPATH, f"//span[text()='{sub_module_text}']/ancestor::a"),
            (By.XPATH, f"//a[span[text()='{sub_module_text}']]"),
            (By.XPATH, f"//span[text()='{sub_module_text}']/.."),
            (By.XPATH, f"//*[text()='{sub_module_text}']/ancestor::li"),]
        sub_module = self.find_element_with_fallback(locators)
        sub_module.click()

    def click_new_work_order(self):
        self.close_modal_if_present()
        locators = [
            (By.XPATH, "//button[span[text()='New Work Order']]"),
            (By.XPATH, "//button[contains(., 'New Work Order')]"),
            (By.XPATH, "//span[text()='New Work Order']/ancestor::button"),
            (By.XPATH, "//button[@type='button' and .//span[text()='New Work Order']]"),]
        button = self.find_element_with_fallback(locators)
        button.click()

    def select_priority(self, priority_text):
        locators = [
            (By.NAME, "select-field-priority"),
            (By.XPATH, "//select[@name='select-field-priority']"),
            (By.CSS_SELECTOR, "select.pulpo-dropdown"),]
        dropdown_element = self.find_element_with_fallback(locators)
        select = Select(dropdown_element)
        select.select_by_visible_text(priority_text)

    def select_category(self, category_text):
        locators = [
            (By.NAME, "select-field-category"),
            (By.XPATH, "//select[@name='select-field-category']"),
            (By.CSS_SELECTOR, "select.pulpo-dropdown"),]
        dropdown_element = self.find_element_with_fallback(locators)
        select = Select(dropdown_element)
        select.select_by_visible_text(category_text)

    def select_subcategory(self, subcategory_text):
        locators = [
            (By.NAME, "select-field-subcategory"),
            (By.XPATH,
             "//span[normalize-space()='Subcategory']/ancestor::div[contains(@class, 'fields_field')]//select"),
            (By.CSS_SELECTOR, "select.pulpo-dropdown"),]
        dropdown_element = self.find_element_with_fallback(locators)
        select = Select(dropdown_element)
        select.select_by_visible_text(subcategory_text)

    def enter_problem_description(self, description_text):
        locators = [
            (By.NAME, "string-field-problem_description"),
            (By.XPATH,"//span[normalize-space()='Problem Description']/ancestor::div[contains(@class, 'fields_field')]//textarea"),
            (By.CSS_SELECTOR, "textarea.pulpo-textarea"),]
        textarea_element = self.find_element_with_fallback(locators)
        textarea_element.clear()
        textarea_element.send_keys(description_text)

    def click_draw_marker(self):
        locators = [
            (By.CLASS_NAME, "leaflet-draw-draw-marker"),
            (By.XPATH, "//a[@title='Draw a marker']"),
            (By.XPATH, "//a[contains(@class, 'leaflet-draw-draw-marker') and @href='#']"),
            (By.XPATH, "//a[span[text()='Draw a marker']]"),]
        element = self.find_element_with_fallback(locators)
        element.click()

    def click_on_map(self, x_offset=10, y_offset=10):
        locators = [
            (By.ID, "map"),
            (By.CLASS_NAME, "leaflet-container"),
            (By.XPATH, "//div[contains(@class, 'leaflet-container')]"),
            (By.XPATH, "//div[contains(@class, 'leaflet') and contains(@class, 'container')]"),]
        map_element = self.find_element_with_fallback(locators)
        map_element.click()

    def enter_input_to_field(self, field_name, text):
        locators = [
            (By.XPATH, f"//span[text()='{field_name}']/../..//input[@type='text']"),
            (By.XPATH,
             f"//span[normalize-space()='{field_name}']/ancestor::div[contains(@class,'fields_field')]//input"),
            (By.XPATH, f"//label[contains(text(),'{field_name}')]/following-sibling::input"),
            (By.XPATH, f"//*[contains(text(),'{field_name}')]/ancestor::div//input"),]
        input_field = self.find_element_with_fallback(locators)
        input_field.send_keys(text)

    def select_dropdown_by_text(self, field_name, visible_text):
        locators = [
            (By.XPATH, f"//span[text()='{field_name}']/../..//select"),
            (By.XPATH,f"//span[normalize-space()='{field_name}']/ancestor::div[contains(@class,'fields_field')]//select"),
            (By.XPATH, f"//label[contains(text(),'{field_name}')]/following-sibling::select"),
            (By.XPATH, f"//*[contains(text(),'{field_name}')]/ancestor::div//select"),]
        dropdown_element = self.find_element_with_fallback(locators)
        select = Select(dropdown_element)
        select.select_by_visible_text(str(visible_text))
        print(f"Selected '{visible_text}' from '{field_name}' dropdown.")

    def click_checkbox(self, field_name):
        locators = [
            (By.XPATH, f"//span[text()='{field_name}']/preceding-sibling::input[@type='checkbox']"),
            (By.XPATH, f"//span[normalize-space()='{field_name}']/ancestor::span//input[@type='checkbox']"),
            (By.XPATH, f"//label[contains(text(),'{field_name}')]/preceding-sibling::input[@type='checkbox']"),
            (By.XPATH, f"//*[contains(text(),'{field_name}')]/ancestor::div//input[@type='checkbox']"),]
        self.find_element_with_fallback(locators).click()

    def select_system_user(self, text):
        input_locators = [
            (By.XPATH,
             "//span[normalize-space()='System User']/ancestor::div[contains(@class,'fields_field')]//input[@type='text']"),
            (By.XPATH, "//label[contains(text(),'System User')]/following::input[@type='text'][1]"),
            (By.XPATH, "//input[@aria-autocomplete='list' and contains(@id, 'react-select')]")]

        option_locators = [
            (By.XPATH, f"//div[contains(@class,'option') and normalize-space()='{text}']"),
            (By.XPATH, f"//div[@id and contains(@id,'option') and normalize-space()='{text}']")]

        self.find_element_with_fallback(input_locators).click()
        self.find_element_with_fallback(option_locators).click()
        print(f" Selected System User: {text}")

    def select_property(self, text):
        dropdown_locators = [
            (By.XPATH,"//span[contains(text(),'Properties')]/ancestor::div[contains(@class,'fields_field')]//input[@type='text']"),
            (By.XPATH, "//div[contains(@class,'css-1g6gooi')]//input[@type='text' and contains(@id, 'react-select')]"),
            (By.XPATH, "//span[normalize-space()='Properties']/following::input[@type='text'][1]")]

        option_locators = [
            (By.XPATH, f"//div[contains(@class, 'css-11unzgr')]//div[text()='{text}']"),
            (By.XPATH, f"//div[contains(@class,'menu')]//div[text()='{text}']")]

        self.find_element_with_fallback(dropdown_locators).click()
        self.find_element_with_fallback(option_locators).click()

    def select_company_name(self, company_text):
        input_locators = [
            (By.XPATH,"//span[contains(.,'Company Name')]/ancestor::div[contains(@class,'fields_field')]//input[@type='text']"),
            (By.XPATH, "//input[@type='text' and contains(@id, 'react-select') and @aria-autocomplete='list']"),
            (By.XPATH, "//div[contains(@class,'css-1hwfws3')]//input[@type='text']"),]
        option_locators = [
            (By.XPATH, f"//div[@class='css-26l3qy-menu']//div[text()='{company_text}']"),
            (By.XPATH, f"//div[contains(@class,'option') and text()='{company_text}']"),]

        self.find_element_with_fallback(input_locators).click()
        self.find_element_with_fallback(option_locators).click()

    def enter_input_number_filed(self,text):
        locators = [
            (By.XPATH, "//span[contains(text(),'Number_Field')]/following::input[@type='number'][1]"),
            (By.XPATH, "//input[@name='number-field-field_1']"),
            (By.XPATH, "//input[@type='number' and contains(@class,'pulpo-numberfield')]"),
            (By.CSS_SELECTOR, "input[name='number-field-field_1']")]
        self.find_element_with_fallback(locators).send_keys(text)

    def click_date_field(self):
        locators = [
            (By.XPATH, "//span[contains(text(), 'Date_Field')]/following::input[@type='text'][1]"),
            (By.XPATH, "//span[normalize-space()='Date_Field']/following::div[contains(@class, 'rdt')][1]//input"),
            (By.XPATH, "//input[contains(@class, 'pulpo-datepicker')]"),
            (By.XPATH, "//input[contains(@placeholder, 'Date') or contains(@name, 'date')]"),
            (By.XPATH, "//div[contains(@class, 'fields_field') and .//span[contains(., 'Date')]]//input"),]
        date_input = self.find_element_with_fallback(locators)
        date_input.click()

    def select_day_in_date_picker(self, date):
        locators = [
            (By.XPATH,f"(//span[text()='Date_Field']/..//tbody//tr//td[contains(@class,'rdtDay') and not(contains(@class,'rdtOld') or contains(@class,'rdtDisabled') or contains(@class,'rdtNew')) and normalize-space(text())='{date}'])[1]"),
            (By.XPATH,f"//td[contains(@class, 'rdtDay') and not(contains(@class, 'rdtOld')) and not(contains(@class, 'rdtNew')) and normalize-space(text())='{date}']"),
            (By.XPATH, f"//td[contains(@class, 'rdtDay') and normalize-space(text())='{date}']"),
            (By.XPATH, f"//div[contains(@class, 'rdtPicker')]//td[normalize-space(text())='{date}']"),]
        self.find_element_with_fallback(locators).click()

    def select_custom_dropdown_by_text(self, field_name, visible_text):
        locators = [(By.XPATH,f"//span[contains(text(),'{field_name}')]/ancestor::div[contains(@class,'fields_multiLoc')]//input[contains(@id,'react-select')]"),
            (By.XPATH,f"//span[contains(text(),'{field_name}')]/ancestor::div[contains(@class,'fields_multiLoc')]//div[contains(@class,'indicatorContainer')]")]

        input_element = self.find_element_with_fallback(locators)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_element)
        WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, locators[0][1])))
        try:
            input_element.click()
        except Exception:
            ActionChains(self.browser).move_to_element(input_element).click().perform()
        input_element.send_keys(visible_text)

        option_xpath = f"//div[contains(@class, 'option') and normalize-space(text())='{visible_text}']"
        option_element = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option_element.click()

        print(f"Selected '{visible_text}' from '{field_name}' dropdown.")

    def click_create_button(self):
        locators = [
            (By.XPATH, "//button[.//span[text()='Create']]"),
            (By.XPATH, "//button[normalize-space()='Create']"),
            (By.XPATH, "//button[contains(@class,'createBtn')]"),
            (By.XPATH,"//button[contains(@class,'button_button__H5057') and contains(@class,'workOrderCreate_createBtn__9ZhoB')]"),
            (By.XPATH, "//span[text()='Create']/parent::button"),]
        create_button = self.find_element_with_fallback(locators)
        create_button.click()
        self.close_modal_if_present()
        print("Clicked the 'Create' button.")









