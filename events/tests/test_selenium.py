import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestHomePage:
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup that runs before each test"""
        self.browser = browser
        self.wait = WebDriverWait(browser, 4)
        self.base_url = "http://localhost:8000/"
        self.browser.get(self.base_url)

    def test_page_load(self):
        """Test that the page loads correctly with expected elements"""
        # Verify page title contains "home"
        assert "home" in self.browser.title.lower()
        
        # Verify main heading text
        heading = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert heading.text == ("Smartest way to collect questions from your audience.").upper()

    def test_form_elements_visible(self):
        """Test that form elements are present and visible"""
        # Input field assertions
        input_field = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "input-field"))
        )
        assert input_field.get_attribute("placeholder") == "E.g: Chat with Osahenru"
        assert input_field.get_attribute("required") == "true"
        
        # Submit button assertions
        submit_button = self.browser.find_element(By.CLASS_NAME, "btn1")
        assert submit_button.is_displayed()
        assert submit_button.text == "Generate event link"

    def test_form_validation(self):
        """Test form validation behavior"""
        submit_button = self.browser.find_element(By.CLASS_NAME, "btn1")
        submit_button.click()

    def test_successful_form_submission(self):
        """Test successful form submission"""
        input_field = self.browser.find_element(By.CLASS_NAME, "input-field")
        input_field.clear()
        input_field.send_keys("Test Event")
        
        submit_button = self.browser.find_element(By.CLASS_NAME, "btn1")
        submit_button.click()

        if '/event/test-event/' in self.browser.current_url:
            redirect_url = 'http://localhost:8000/event/test-event/'
            assert self.browser.current_url == redirect_url
        else:
            error = self.browser.find_element(By.CSS_SELECTOR, ".error-messages")
            assert "already exists" in error.text
        

    @pytest.mark.parametrize("width,height,is_mobile", [
        (375, 812, True),  # Mobile
        (1200, 800, False) # Desktop
    ])
    def test_responsive_layout(self, width, height, is_mobile):
        """Test responsive layout at different screen sizes"""
        self.browser.set_window_size(width, height)
        
        if is_mobile:
            # Mobile assertions
            steps = self.wait.until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "mobile-step"))
            )
            assert len(steps) == 3
            assert not self.browser.find_element(By.CLASS_NAME, "img-box").is_displayed()
        else:
            # Desktop assertions
            assert self.browser.find_element(By.CLASS_NAME, "img-box").is_displayed()
            mobile_container = self.browser.find_element(By.CLASS_NAME, "mobile-how-to-container")
            assert mobile_container.value_of_css_property("display") == "none"