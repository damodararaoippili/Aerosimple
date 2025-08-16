from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Login:
    def __init__(self, browser):
        self.browser = browser

        self.email_locators = [
            (By.XPATH, "//input[@type='email']"),
            (By.XPATH, "//input[contains(@name, 'email')]"),
            (By.XPATH, "//input[contains(@placeholder, 'email') or contains(@placeholder, 'Email')]"),
            (By.XPATH, "//label[contains(text(), 'Email')]/following-sibling::input"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.NAME, "email")]

        self.password_input_locators = [
            (By.XPATH, "//input[@type='password']"),
            (By.XPATH, "//input[contains(@name, 'password')]"),
            (By.XPATH, "//input[contains(@placeholder, 'password') or contains(@placeholder, 'Password')]"),
            (By.XPATH, "//label[contains(text(), 'Password')]/following-sibling::input"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.NAME, "loginPassword")]

        self.next_locators = [
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Next')]"),
            (By.XPATH, "//button[contains(., 'Login') or contains(., 'Continue')]"),
            (By.XPATH, "//form//button"),
            (By.CSS_SELECTOR, "button[type='submit']")]

        self.validation_locators = [
            (By.XPATH, "//span[text()='This field cannot be empty']"),
            (By.XPATH, "//span[normalize-space()='This field cannot be empty']"),
            (By.XPATH, "//small[contains(@class, 'login_error')]/span"),
            (By.XPATH, "//div/small/span[contains(text(), 'cannot be empty')]"),
            (By.CSS_SELECTOR, "small[class*='login_error'] span")]

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
            WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "modal"))
            )
            self.browser.find_element(By.XPATH, "//div[@class='modal']//button[text()='Close']").click()
            WebDriverWait(self.browser, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "modal"))
            )
        except:
            print("Modal not found or already closed.")

    def enter_email(self, Email):
        try:
            email = self.find_element_with_fallback(self.email_locators)
            email.clear()
            email.send_keys(Email)
        except Exception as e:
            assert False, f"Failed to enter email: {e}"

    def click_on_next(self):
        try:
            next_btn = self.find_element_with_fallback(self.next_locators)
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(next_btn)
            )
            next_btn.click()
        except Exception as e:
            assert False, f"Failed to click on Next button: {e}"

    def enter_password(self, Password):
        try:
            password = self.find_element_with_fallback(self.password_input_locators)
            password.clear()
            password.send_keys(Password)
        except Exception as e:
            assert False, f"Failed to enter password: {e}"

    def check_validation(self):
        try:
            expected_message = "This field cannot be empty"
            validation = self.find_element_with_fallback(self.validation_locators)
            actual_message = validation.text.strip()
            assert actual_message == expected_message, f"Expected '{expected_message}' but got '{actual_message}'"
        except Exception as e:
            assert False, f"Failed to check validation message: {e}"
