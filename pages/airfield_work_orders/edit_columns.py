from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class AlwaysTrue:
    def __call__(self, driver):
        return True

def wait_without_sleep(browser, seconds=10):
    WebDriverWait(browser, seconds).until(AlwaysTrue())

class Edit_columns:
    def __init__(self, browser):
        self.browser = browser

    def find_element_with_fallback(self,locators,wait_time=10):
        for by,value in locators:
            try:
                element = WebDriverWait(self.browser,wait_time).until(EC.presence_of_element_located((by,value)))
                print(f"[Self-Healing] Found using: ({by}, {value})")
                return element
            except:
                print(f"[Self-Healing] Failed: ({by}, {value})")
        raise Exception("Element not found with any locator.")
    def close_modal_if_present(self):
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
            close_button = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='modal']//button[text()='Close']")))
            close_button.click()
            WebDriverWait(self.browser, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
            print("Modal closed successfully.")
        except Exception:
            print("Modal not found or already closed.")

    def click_on_apps(self):
        try:
            locators = [
                (By.XPATH, "//div[@class='topbar_menu__3MEY5']//button[span[text()='apps']]"),
                (By.XPATH, "//button[span[text()='apps']]"),
                (By.XPATH, "//button[.//span[contains(text(),'apps')]]"),
                (By.XPATH, "//span[text()='apps']/parent::button"),
                (By.XPATH, "//img[@alt='menu']/following-sibling::span[text()='apps']/parent::button")]

            apps_button = self.find_element_with_fallback(locators)
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
            (By.XPATH, f"//*[text()='{module_text}']/ancestor::*[contains(@class,'menu')]"), ]
        module = self.find_element_with_fallback(locators)
        module.click()

    def click_on_sub_module(self, sub_module_text):
        locators = [
            (By.XPATH, f"//span[text()='{sub_module_text}']/ancestor::a"),
            (By.XPATH, f"//a[span[text()='{sub_module_text}']]"),
            (By.XPATH, f"//span[text()='{sub_module_text}']/.."),
            (By.XPATH, f"//*[text()='{sub_module_text}']/ancestor::li"), ]
        sub_module = self.find_element_with_fallback(locators)
        sub_module.click()

    def click_on_Actions(self):
        locators = [
            (By.XPATH, "//div[@class='toolbar_actionsBtn__3AJbv' and @role='button']//span[text()='Actions']"),
            (By.XPATH, "//div[@class='toolbar_actionsBtn__3AJbv' and @role='button']"),
            (By.XPATH, "//span[text()='Actions']/ancestor::div[@role='button']"),
            (By.XPATH, "//div[@tabindex='0' and @role='button' and .//span[text()='Actions']]"),
            (By.XPATH, "//div[contains(@class, 'toolbar_actionsBtn') and @role='button']//span[text()='Actions']"),
            (By.XPATH, "//div[@role='button' and .//span[text()='Actions']]"),
        ]
        try:
            self.close_modal_if_present()
            self.find_element_with_fallback(locators).click()
        except Exception as e:
            print('failed to click on Action button')

    def click_on_edit_columns(self):
        locators = [(By.XPATH,"//span[text()='Edit Columns']/..")]
        try:
            self.find_element_with_fallback(locators).click()
        except Exception as e:
            print('failed to click on edit column')

    def click_on_edit_column_search(self, text):
        locators = [(By.XPATH, "//input[@placeholder='Search Columns']")]
        try:
            search_input = self.find_element_with_fallback(locators)
            search_input.click()
            search_input.send_keys(text)
        except Exception as e:
            print('Failed to click on search and enter:', str(e))

    def click_on_select_edit_columns(self, text):
        locators = [(By.XPATH, f"//label[normalize-space(text())='{text}']/..//input")]
        try:
            checkbox = self.find_element_with_fallback(locators)
            checkbox.click()
        except Exception as e:
            print(f"Failed to select edit column checkbox for '{text}': {e}")

    def click_on_Apply(self):
        locators = [(By.XPATH,"//div[@class='columnCustomizer_modalBtnGroup__Mdx3l']//span[normalize-space(text())='Apply']/..")]
        try:
            self.find_element_with_fallback(locators).click()
        except Exception as e:
            print(f'Failed to click on Apply button: {e}')

    def header_edit_columns(self):
        xpath = "//tr[@class='general_nonAirfieldRow__3q1Nl']/th//span"
        header_elements = self.browser.find_elements(By.XPATH, xpath)

        headers = []

        for element in header_elements:
            text = element.text.strip()
            headers.append(text if text else "(no header)")
        print(headers)
        return headers