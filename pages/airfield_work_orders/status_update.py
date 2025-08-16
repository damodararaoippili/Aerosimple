from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
class Status_update:
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

    def work_order(self):
        work_order_number = (By.XPATH,"(//table//tr/td[1])[1]")
        maximum = 5
        for attempt in range(maximum+1):
            try:
                self.close_modal_if_present()
                element = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located(work_order_number))
                work_order_number = element.text.strip()
                return work_order_number
            except Exception as e:
                print(f"[Work Order number] Element not found: {str(e)}")
                return False

    def work_order_status(self, text):
        try:
            rows = self.browser.find_elements(By.XPATH, "//table//tbody//tr")
            for i in range(1, len(rows) + 1):
                try:
                    status_xpath = f"(//table//tbody//tr)[{i}]//td[4]//span"
                    status_element = self.browser.find_element(By.XPATH, status_xpath)
                    status_text = status_element.text.strip()
                    print(f"[i] Found status '{status_text}' in row {i}")

                    if status_text == text:
                        view_xpath = (By.XPATH, f"(//table//tbody//tr)[{i}]//td//a[span[normalize-space()='View']]")
                        view_link = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(view_xpath))
                        view_link.click()
                        print(f"[✓] Clicked 'View' on row {i} with status '{text}'")
                        return True

                except Exception as e:
                    print(f"[!] Error in row {i}: {e}")
            print(f"[x] No row found with status '{text}' and clickable View link.")
            return False
        except Exception as e:
            print(f"[!] Error in work_order_status(): {e}")
            return False

    def click_on_filters(self):
        locators = [
            (By.XPATH, "//span[@role='button' and contains(., 'Filters')]"),
            (By.XPATH, "//span[contains(@class, 'toolbar_actionsBtn') and span[text()='Filters']]"),
            (By.XPATH, "//span[text()='Filters']/ancestor::span[@role='button']"),
            (By.XPATH, "(//span[contains(text(),'Filters')])[1]/ancestor::span[@role='button']")]
        try:
            self.close_modal_if_present()
            element = self.find_element_with_fallback(locators)
            element.click()
        except Exception as e:
            print(f"[ERROR] failed to click on filters ': {e}")

    def click_on_clear_filters(self):
        clear_button_locators = [
            (By.XPATH, "//div[@role='button' and span[text()='Clear']]"),
            (By.XPATH, "//div[contains(@class, 'filteritem_cancel') and span[text()='Clear']]"),
            (By.XPATH, "//span[text()='Clear']/parent::div[@role='button']"),
            (By.XPATH, "(//div[@role='button']//span[text()='Clear'])[1]")]
        try:
            element = self.find_element_with_fallback(clear_button_locators)
            element.click()
        except Exception as e:
            print(f"[ERROR] failed to click on clear  filters ': {e}")

    def click_on_apply(self):
        apply_button_locators = [
            (By.XPATH, "//div[@class='filteritem_header__38PPg']//span[text()='Apply']/parent::button"),
            (By.XPATH,"//div[@class='filteritem_header__38PPg']//button[contains(@class, 'filteritem_btnPadding') and span[text()='Apply']]"),
            (By.XPATH, "//div[@class='filteritem_header__38PPg']//button[contains(., 'Apply')]"),
            (By.XPATH, "//div[@class='filteritem_header__38PPg']//span[text()='Apply']/..]")]

        try:
            element = self.find_element_with_fallback(apply_button_locators)
            element.click()
            self.close_modal_if_present()
            return True
        except Exception as e:
            print(f"[ERROR] failed to click on apply: {e}")
            return False

    def click_on_view(self, status):
        locators = [
            (By.XPATH,f"(//tr[.//span[text()='{status}']]//span[normalize-space()='View'])[1]"),
            (By.XPATH,f"//tr[.//span[text()='{status}']]//a[.//span[normalize-space()='View']]"),
            (By.XPATH,f"//a[contains(@href, '/workorders/airfield') and .//span[normalize-space()='View'] and ancestor::tr[.//span[text()='{status}']]]"),
            (By.XPATH,f"(//span[normalize-space()='{status}']/ancestor::tr//span[normalize-space()='View'])[1]")]
        try:
            element = self.find_element_with_fallback(locators)
            element.click()
            return True
        except Exception as e:
            print(f"[ERROR] View button not found for status '{status}': {e}")
            return False
    def click_on_update_status(self):
        locators = [
            (By.XPATH,"//span[text()='Update Status']/..]"),
            (By.XPATH,"//button[contains(@class, 'button_primary') and span[text()='Update Status']]"),
            (By.XPATH,"//button[@type='button' and @tabindex='0' and contains(@class, 'button_button') and span[text()='Update Status']]"),
            (By.XPATH,"(//button[span[text()='Update Status']])[1]")]
        try:
            self.close_modal_if_present()
            element = self.find_element_with_fallback(locators)
            element.click()
            print('click on update status')
        except Exception as e:
            print(f'failed to click on update status: {e}')
            return False
    def click_on_status(self,status):
        status_locator = [(By.XPATH,f"//span[text()='{status}']")]
        maximum = 5
        for attempt in range(maximum+1):
            try:
                self.close_modal_if_present()
                element = self.find_element_with_fallback(status_locator)
                element.click()
                print(f'click on status:{status}')
            except Exception as e:
                print(f'failed to click on status :{e}')
                return False