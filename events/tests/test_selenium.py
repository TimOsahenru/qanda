import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.django_db
def test_home_page(browser):
    browser.get('http://localhost:8000/')

    title_section = browser.find_element(By.TAG_NAME, 'title')
    title_name = title_section.get_attribute('textContent')
    assert title_name == 'qanda | home', f"Expected title to be 'qanda | home' but {title_name}"

    form_section = browser.find_element(By.TAG_NAME, 'form') 
    # test event form
    # test for redirect
    # test title
    # test button name
    # test taglines in hero section