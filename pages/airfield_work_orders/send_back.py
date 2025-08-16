from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
class Send_Back:
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

    def click_on_view(self,status):
        locators = [
            (By.XPATH, f"(//tr[.//span[text()='{status}']]//span[normalize-space()='View'])[1]"),
            (By.XPATH, f"//tr[.//span[text()='{status}']]//a[.//span[normalize-space()='View']]"),
            (By.XPATH, f"//a[contains(@href, '/workorders/airfield') and .//span[normalize-space()='View'] and ancestor::tr[.//span[text()='{status}']]]"),
            (By.XPATH, f"(//span[normalize-space()='{status}']/ancestor::tr//span[normalize-space()='View'])[1]")]
        try:
            element = self.find_element_with_fallback(locators)
            element.click()
            return True
        except Exception as e:
            print(f"[ERROR] View button for 'Maintenance Review' not found: {e}")
            return False
    def click_on_actions(self):
        locators = [
            (By.XPATH,"//span[text()='Actions']"),
            (By.XPATH,"//span[@role='button']"),
            (By.XPATH,"//span[@class='workOrderDetail_actionsBtn__1kMIv']")]
        try:
            element = self.find_element_with_fallback(locators)
            actions = ActionChains(self.browser)
            actions.move_to_element(element).perform()
            element.click()
        except Exception as e:
            print(f"[ERROR] Failed to click on Actions button: {str(e)}")

    def click_on_send_back(self):
        locators = [
            ("xpath", "//span[@translationid='Workorders.detail.sendback']"),
            ("xpath", "//span[@defaulttext='Send back to Maintenance']"),
            ("xpath", "//span[@action='secondary' and normalize-space()='Send back to maintenance']"),
            ("xpath", "//li[contains(@class, 'workOrderDetail_item')]//span[text()='Send back to maintenance']"),
            ("css selector", "li.workOrderDetail_item__3RKaa > span[translationid='Workorders.detail.sendback']"),
            ("css selector", "li.workOrderDetail_item__3RKaa span:has-text('Send back to maintenance')"),]
        try:
            element = self.find_element_with_fallback(locators)
            actions = ActionChains(self.browser)
            actions.move_to_element(element).perform()
            element.click()
        except Exception as e:
            print(f"[ERROR] Failed to click on send back button: {str(e)}")

    def verify_send_back_model(self):
        locators = [("css selector", "div.modal_content__1tL7m"),("xpath", "//div[contains(@class, 'modal_content')]")]
        try:
            element = self.find_element_with_fallback(locators)
            if element.is_displayed():
                print("[INFO] Send Back modal is visible.")
                return True
            else:
                print("[WARNING] Modal element found but not visible.")
        except Exception as e:
            print("[ERROR] Send Back modal did not appear:", str(e))
            return False
    def send_back_description(self,text):
        locators = [
            ("css selector", "textarea#description"),  # Most stable: uses ID
            ("css selector", "textarea[name='description']"),
            ("css selector", "textarea.submitComment_commentInput__2TgEf"),
            ("xpath", "//textarea[@id='description']"),
            ("xpath", "//textarea[@placeholder='Leave your comment here...']"),
            ("xpath", "//textarea[contains(@class, 'submitComment_commentInput')]"),
            ("xpath", "//textarea[@name='description']"),]
        description = self.find_element_with_fallback(locators)
        description.send_keys(text)

    def click_on_send_back_button(self):
        locators = [
            ("xpath", "//button[@type='submit']//span[normalize-space()='Send Back']"),
            ("xpath", "//button[@type='submit']//span[contains(text(), 'Send Back')]"),
            ("xpath", "//button[@type='submit' and .//span[text()='Send Back']]"),
            ("css selector", "button.button_button__H5057.button_secondary__1yQBY[type='submit']"),
            ("xpath", "//button[contains(@class, 'button_secondary') and @type='submit']"),]
        send_back_button = self.find_element_with_fallback(locators)
        send_back_button.click()
        self.close_modal_if_present()



