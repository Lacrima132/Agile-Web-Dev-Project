import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestSelenium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/google-chrome"  # Adjust this path if necessary
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)
        cls.driver.get("http://127.0.0.1:5000/")  # URL for the Flask app

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_title(self):
        self.assertEqual("Bountify", self.driver.title)

    def test_homepage_login_button(self):
        try:
            login_button = self.driver.find_element(By.CLASS_NAME, "btn-prominent")
            self.assertIsNotNone(login_button)
        except Exception as e:
            self.fail(f"Homepage redirect button not found: {e}")

    def test_login_page_elements(self):
        self.driver.get("http://127.0.0.1:5000/login")
        try:
            email_input = self.driver.find_element(By.ID, "email")
            password_input = self.driver.find_element(By.ID, "password")
            submit_button = self.driver.find_element(By.CLASS_NAME, "btn-submit")

            self.assertIsNotNone(email_input)
            self.assertIsNotNone(password_input)
            self.assertIsNotNone(submit_button)
        except Exception as e:
            self.fail(f"Login page elements not found: {e}")

if __name__ == "__main__":
    unittest.main()
