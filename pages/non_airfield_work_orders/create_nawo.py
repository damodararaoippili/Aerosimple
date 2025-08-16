from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Create_NAWO:
    def __init__(self, browser):
        self.browser = browser

        self.apps_locators = [
            (By.XPATH, "//div[@class='topbar_menu__3MEY5']//button[span[text()='apps']]"),
            (By.XPATH, "//button[span[text()='apps']]"),
            (By.XPATH, "//button[.//span[contains(text(),'apps')]]"),
            (By.XPATH, "//span[text()='apps']/parent::button"),
            (By.XPATH, "//img[@alt='menu']/following-sibling::span[text()='apps']/parent::button")]

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
