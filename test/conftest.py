
from selenium import webdriver

import pytest

@pytest.fixture
def webPage():
    driver = webdriver.Chrome()
    driver.get("https://www.lambdatest.com/automation-demos")
    return driver.title

@pytest.fixture
def titleString():
    return "Selenium"