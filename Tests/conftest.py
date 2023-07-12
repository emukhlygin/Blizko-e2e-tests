import json
import time

import pytest
from selenium import webdriver

from Pages.LoginModal import LoginModal
from Pages.MainPage import MainPage
from Utilities.Settings import Settings
from Utilities.TestData import TestData


@pytest.fixture()
def set_up():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(Settings.base_url)
    mpg = MainPage(driver)
    mpg.enter_login_modal()\
      .log_in_application(Settings.test_email, Settings.test_password)  # логин в систему с данными тестового пользователя
    yield driver
    # driver.get(Settings.base_url)
    # if mpg.get_number_of_products_in_cart() != '':       # проверка на наличие продуктов в корзине, оставшихся после прогона тестов
    #      mpg.enter_cart()\
    #        .clean_up_all_added_products()         # удаление продуктов в корзине
    driver.close()

