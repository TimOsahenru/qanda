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
        (375, 812, True),
        (1200, 800, False)
    ])
    def test_responsive_layout(self, width, height, is_mobile):
        """Test responsive layout at different screen sizes"""
        self.browser.set_window_size(width, height)
        
        if is_mobile:
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


class TestEventPage:
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup that runs before each test"""
        self.browser = browser
        self.wait = WebDriverWait(browser, 4)
        self.event_slug = 'test-event'
        self.event_url = f"http://localhost:8000/event/{self.event_slug}/"
        self.browser.get(self.event_url)

    def test_page_load(self):
        """Test that the event page loads correctly"""
        assert "event" in self.browser.title.lower()
        
        event_title = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-title"))
        )
        assert event_title.is_displayed()

    def test_page_elements(self):
        """Test that all key elements are present"""
        event_image = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "event-image"))
        )
        assert event_image.is_displayed()
        
        
        url_input = self.browser.find_element(By.ID, "urlInput")
        assert url_input.is_displayed()
        assert url_input.get_attribute("readonly") == "true"
        assert f"ask/{self.event_slug}" in url_input.get_attribute("value")
        
        copy_button = self.browser.find_element(By.CLASS_NAME, "copy-btn-inside")
        assert copy_button.is_displayed()
        
        proceed_button = self.browser.find_element(By.CLASS_NAME, "goto-btn")
        assert proceed_button.is_displayed()
        assert "Proceed to event" in proceed_button.text

    def test_copy_url_functionality(self):
        """Test that the copy URL functionality works"""
        copy_button = self.browser.find_element(By.CLASS_NAME, "copy-btn-inside")
        copy_button.click()

    def test_proceed_button(self):
        """Test that the proceed button redirects correctly"""
        proceed_button = self.browser.find_element(By.CLASS_NAME, "goto-btn")
        proceed_button.click()
        
        self.wait.until(
            EC.url_contains(f"/ask/{self.event_slug}")
        )
        assert f"ask/{self.event_slug}" in self.browser.current_url

    @pytest.mark.parametrize("width,height", [
        (375, 812),
        (1200, 800)
    ])

    def test_responsive_layout(self, width, height):
        """Test responsive layout at different screen sizes"""
        self.browser.set_window_size(width, height)
        
        event_content = self.browser.find_element(By.CLASS_NAME, "event-content")
        if width == 375:
            assert "column" in event_content.value_of_css_property("flex-direction")
        else:
            assert "row" in event_content.value_of_css_property("flex-direction")


class TestAskPage:
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup that runs before each test"""
        self.browser = browser
        self.wait = WebDriverWait(browser, 4)
        self.event_slug = 'test-event'
        self.ask_url = f"http://localhost:8000/ask/{self.event_slug}/"
        self.browser.get(self.ask_url)

    def test_page_load(self):
        """Test that the ask page loads correctly"""
        assert "ask" in self.browser.title.lower()
        
        event_header = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "event-header"))
        )
        assert event_header.is_displayed()

    def test_page_elements(self):
        """Test that all key elements are present"""
        event_title = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".event-header h2"))
        )
        assert event_title.is_displayed()
        
        questions_count = self.browser.find_element(By.CLASS_NAME, "questions-count")
        assert questions_count.is_displayed()
        
        chat_container = self.browser.find_element(By.CLASS_NAME, "chat-container")
        assert chat_container.is_displayed()
        
        input_container = self.browser.find_element(By.CLASS_NAME, "fixed-input-container")
        assert input_container.is_displayed()
        assert input_container.value_of_css_property("position") == "fixed"

    def test_questions_display(self):
        """Test questions display (both empty and populated states)"""
        try:
            questions = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "question"))
            )
            
            assert len(questions) > 0
            
            for question in questions:
                assert question.find_element(By.TAG_NAME, "div").is_displayed()
                like_btn = question.find_element(By.CLASS_NAME, "like-btn")
                assert like_btn.is_displayed()
                assert like_btn.text == "❤"
                assert question.find_element(By.CLASS_NAME, "like-count").is_displayed()
                
        except:
            empty_state = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "empty-state"))
            )
            assert empty_state.is_displayed()
            assert "No Questions Yet" in empty_state.text
            assert "Be the first to ask" in empty_state.text

    def test_question_submission(self):
        """Test question submission functionality"""
        input_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "id_text"))
        )
        submit_button = self.browser.find_element(By.ID, "submit")
        
        input_field.send_keys("Test question")
        submit_button.click()
        redirect_url = f'http://localhost:8000/ask/{self.event_slug}/'
        assert self.browser.current_url == redirect_url
        
      

    def test_like_functionality(self):
        """Test question like functionality"""
        questions = self.browser.find_elements(By.CLASS_NAME, "question")
        
        like_btn = questions[0].find_element(By.CLASS_NAME, "like-btn")
        like_count = questions[0].find_element(By.CLASS_NAME, "like-count")
        initial_count = int(like_count.text)
        
        like_btn.click()
        self.wait.until(
            lambda d: int(like_count.text) == initial_count + 1
        )
        assert "liked" in like_btn.get_attribute("class")
        

    @pytest.mark.parametrize("width,height", [
        (375, 812),
        (1200, 800)
    ])
    def test_responsive_layout(self, width, height):
        """Test responsive layout at different screen sizes"""
        self.browser.set_window_size(width, height)
        
        input_container = self.browser.find_element(By.CLASS_NAME, "fixed-input-container")
        if width == 375:
            assert input_container.value_of_css_property("padding") == "15px 0px"
        else:
            assert input_container.value_of_css_property("padding") == "15px 0px"