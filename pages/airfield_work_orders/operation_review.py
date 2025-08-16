from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
class Operation_review:
    def __init__(self,browser):
        self.browser = browser

    def page_refresh(self):
        self.browser.refresh()

    def find_element_with_fallback(self, locators, wait_time=10):
        for by, value in locators:
            try:
                element = WebDriverWait(self.browser, wait_time).until(EC.presence_of_element_located((by, value)))
                print(f"[Self-Healing] Found using: ({by}, {value})")
                return element
            except:
                print(f"[Self-Healing] Failed: ({by}, {value})")
        raise Exception("Element not found with any locator.")

    def wait_until_element_visible(self, by, value, timeout=20):
        try:
            WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((by, value)))
            print(f"[Wait] Element ({by}, {value}) is now visible.")
        except Exception as e:
            raise Exception(f"[Timeout] Element ({by}, {value}) not visible after {timeout} seconds: {str(e)}")


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

    def close_feedback_modal_if_present(self):
        try:
            close_button = self.browser.find_element(By.XPATH,"//div[contains(@class, 'modal_content')]//button[normalize-space()='×']")
            close_button.click()
            print("Modal found and closed.")
        except NoSuchElementException:
            print("Modal not present, skipping.")

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

    def work_order_status(self, status):
        locator = [
            (By.XPATH, f"(//tr//span[text()='{status}']/../..)[1]")]
        try:
            status = self.find_element_with_fallback(locator)
            current_status = status.text.strip()
            return True
        except Exception as e:
            print(f"[Work Order Status] Element not found: {str(e)}")
            return False

    def click_on_view(self, status):
        locators = [
            (By.XPATH, f"(//tr[.//span[text()='{status}']]//span[normalize-space()='View'])[1]"),
            (By.XPATH, f"//tr[.//span[text()='{status}']]//a[.//span[normalize-space()='View']]"),
            (By.XPATH,
             f"//a[contains(@href, '/workorders/airfield') and .//span[normalize-space()='View'] and ancestor::tr[.//span[text()='{status}']]]"),
            (By.XPATH, f"(//span[normalize-space()='{status}']/ancestor::tr//span[normalize-space()='View'])[1]")
        ]
        try:
            element = self.find_element_with_fallback(locators)
            element.click()
            return True
        except Exception as e:
            print(f"[ERROR] View button not found for status '{status}': {e}")
            return False

    def click_on_review_report(self, text):
        locators = [
            (By.XPATH, "//textarea[@name='string-field-work_description']"),
            (By.XPATH, "//textarea[@class='pulpo-textarea undefined']"),
            (By.XPATH, "//div[@class='fields_field__1V1fp fixedFields_fullInput__tH-0L']//textarea"),
            (By.TAG_NAME, "textarea")
        ]
        try:
            element = self.find_element_with_fallback(locators)
            element.clear()
            element.send_keys(text)
            print("Review report filled successfully.")
        except Exception as e:
            print(f"[ERROR] Review report field not found: {e}")

    def click_on_close_work_order(self):
        locators = [(By.XPATH, "//span[text()='Close Work Order']/..")]
        try:
            element = self.find_element_with_fallback(locators)
            element.click()
            print("Clicked on 'Close Work Order' successfully.")
        except Exception as e:
            print(f"[ERROR] 'Close Work Order' button not found: {e}")


