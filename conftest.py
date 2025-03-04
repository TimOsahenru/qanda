import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def browser():
    # Initialize the Chrome browser
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    # Teardown: Close the browser after tests
    driver.quit()