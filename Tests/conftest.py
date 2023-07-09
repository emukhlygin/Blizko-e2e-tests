import json

import pytest
from selenium import webdriver

from Utilities.TestData import TestData


@pytest.fixture()
def set_up():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(r"https://spb.blizko.ru/")
    yield driver
    driver.close()


