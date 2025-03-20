import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.django_db
def test_home_page(browser):
    browser.get('http://localhost:8000/')

    # title_section = browser.find_element(By.TAG_NAME, 'title')
    # title_name = title_section.get_attribute('textContent')
    # assert title_name == 'qanda | home', f"Expected title to be 'qanda | home' but {title_name}"

    # hero_section = browser.find_element(By.CSS_SELECTOR, 'div.detail-box h1')
    # hero_title = hero_section.get_attribute('textContent').strip()
    # assert hero_title == 'Smartest way to collect questions from your audience.'

    # hero_section = browser.find_element(By.CSS_SELECTOR, 'div.detail-box p')
    # hero_title = hero_section.get_attribute('textContent').strip()
    # assert hero_title == 'Streamline your Q&A in advance. Just share the link with your audience'

    # form_section = browser.find_element(By.TAG_NAME, 'form') 

    # event_name_input = browser.find_element(By.CSS_SELECTOR, '.input-field')
    # event_name_input.send_keys('PyConGh 2025')
    # submit_button = browser.find_element(By.CSS_SELECTOR, '.btn1')

    event_name_input = browser.find_element(By.ID, 'id_name')
    event_name_input.send_keys('PyconAfrica 2025')

    submit_button = browser.find_element(By.CSS_SELECTOR, '.btn1')
    submit_button.click()
    redirect_url = 'http://localhost:8000/event/pyconafrica-2025/'
    assert browser.current_url == redirect_url