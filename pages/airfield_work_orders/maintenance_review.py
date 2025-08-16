from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
class WO_Maintenance:
    def __init__(self,browser):
        self.browser = browser

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

    def work_order_status(self,status):
        locator = [
            (By.XPATH, f"(//tr//span[text()='{status}']/../..)[1]")]
        try:
            status = self.find_element_with_fallback(locator)
            current_status = status.text.strip()
            return True
        except Exception as e:
            print(f"[Work Order Status] Element not found: {str(e)}")
            return False

    def click_on_view(self):
        locators = [
            (By.XPATH, "(//tr[.//span[text()='Maintenance Review']]//span[normalize-space()='View'])[1]"),
            (By.XPATH, "//tr[.//span[text()='Maintenance Review']]//a[.//span[normalize-space()='View']]"),
            (By.XPATH,"//a[contains(@href, '/workorders/airfield') and .//span[normalize-space()='View'] and ancestor::tr[.//span[text()='Maintenance Review']]]"),
            (By.XPATH,"(//span[normalize-space()='Maintenance Review']/ancestor::tr//span[normalize-space()='View'])[1]")
        ]
        try:
            element = self.find_element_with_fallback(locators)
            element.click()
            return True
        except Exception as e:
            print(f"[ERROR] View button for 'Maintenance Review' not found: {e}")
            return False

    def enter_description_of_work_done(self,text):
        locators = [
            (By.XPATH,"//textarea[@name='string-field-work_description']"),
            (By.XPATH,"//div[contains(@class, 'field')]//span[contains(., 'Description of work done')]/following-sibling::textarea"),
            (By.XPATH,"//span[contains(text(), 'Description of work done')]/ancestor::div[contains(@class, 'field')]//textarea"),
            (By.XPATH,"//textarea[contains(@class, 'pulpo-textarea')]"),
            (By.XPATH,"(//textarea)[1]")]
        description = self.find_element_with_fallback(locators)
        description.clear()
        description.send_keys(text)

    def click_on_resolve(self):
        locators = [
            (By.XPATH, "//button[span[normalize-space()='Resolve']]"),
            (By.XPATH, "//button[.//span[text()='Resolve']]"),
            (By.XPATH, "//button[contains(@class,'button_button') and .//span[text()='Resolve']]"),
            (By.XPATH, "//span[normalize-space()='Resolve']/ancestor::button"),
            (By.XPATH, "//button[contains(text(),'Resolve') or .//span[contains(text(),'Resolve')]]"),
            (By.XPATH, "(//button[.//span[normalize-space()='Resolve']])[1]")]
        resolve = self.find_element_with_fallback(locators)
        resolve.click()
        self.close_modal_if_present()

    def validate_message(self):
        locators = [
            (By.XPATH, "//div[contains(@class, 'modal_content')]//span[contains(text(), 'review data')]"),
            (By.XPATH, "(//div[contains(@class, 'modal') or contains(@class, 'confirmContent')]//span)[1]"),
        ]
        try:
            message = self.find_element_with_fallback(locators, wait_time=5)
            print(f"Validation message found: {message.text.strip()}")
            return True
        except:
            print("Validation message not found.")
            return False

    def click_on_OK(self):
        locators = [
            (By.XPATH, "//button[.//span[normalize-space()='OK']]"),
            (By.XPATH, "//div[contains(@class, 'btn')]//button[.//span[text()='OK']]"),
            (By.XPATH, "//button[contains(@class,'button_primary') and .//span[text()='OK']]"),
            (By.XPATH, "//div[contains(@class,'modal_content')]//button[.//span[text()='OK']]"),
            (By.XPATH, "(//span[normalize-space()='OK']/ancestor::button)[1]"),]
        OK = self.find_element_with_fallback(locators)
        OK.click()

    def enter_input_time(self, time_value):
        locators = [
            (By.XPATH, "//input[@placeholder='Enter time e.g. 3:30 (OR) 3.5']"),
            (By.XPATH, "//span[contains(text(), 'Input Time')]/following::input[1]"),
            (By.XPATH, "//label[contains(text(), 'Input Time')]/following-sibling::input"),
            (By.XPATH, "//div[contains(@class,'back_popupOrderTime')]//input[@type='text']"),
            (By.XPATH, "(//input[@type='text'])[1]"),]

        input_element = self.find_element_with_fallback(locators)
        input_element.click()
        input_element.clear()
        input_element.send_keys(time_value)

    def click_add_button(self):
        locators = [
            (By.XPATH, "//button[normalize-space()='+ Add']"),
            (By.XPATH, "//button[contains(text(),'+ Add')]"),
            (By.XPATH, "//button[contains(@class, 'back_addTimeBtn')]"),
            (By.XPATH, "(//button[contains(text(),'Add')])[1]"),]
        add = self.find_element_with_fallback(locators)
        add.click()

    def click_on_save(self):
        locators = [
            (By.XPATH, "//button[normalize-space()='Save']"),
            (By.XPATH, "//button[contains(@class, 'back_footerSavebtn')]"),
            (By.XPATH, "//div[contains(@class, 'back_popupFooter')]//button[normalize-space()='Save']"),
            (By.XPATH, "(//div[contains(@class, 'back_popupFooter')]//button)[2]"),]
        save = self.find_element_with_fallback(locators)
        save.click()
        self.close_modal_if_present()


