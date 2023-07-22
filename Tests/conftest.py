import datetime
import os
import pytest
from selenium import webdriver
from Pages.MainPage import MainPage
from Utilities.AdditionalMethods import get_screenshot
from Utilities.Settings import Settings


@pytest.fixture()
def set_up():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(Settings.base_url)
    mpg = MainPage(driver)
    mpg.enter_login_modal()\
       .log_in_application(Settings.test_email, Settings.test_password)  # логин в систему с данными тестового пользователя
    yield driver
    get_screenshot(driver)                # делаем скриншот на случай, если тест упал
    driver.get(Settings.base_url)
    if mpg.get_number_of_products_in_cart() != '':       # проверка на наличие продуктов в корзине, оставшихся после прогона тестов
        mpg.enter_cart()\
           .clean_up_all_added_products()         # удаление продуктов в корзине
    driver.close()


@pytest.fixture(scope='session', autouse=True)
def teardown_session():
    """Зачистка устаревших скриншотов"""
    for filename in os.listdir(Settings.screenshot_folder):
        file_creation_date = os.path.getmtime(Settings.screenshot_folder+filename)
        file_creation_date_formatted = datetime.date.fromtimestamp(file_creation_date)
        if file_creation_date_formatted < datetime.date.today():
            os.remove(Settings.screenshot_folder+filename)

