from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert

from Base.BaseClass import BaseClass
from Pages.ProductsPage import ProductsPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BaseClass):
    """Класс, описывающий основную страницу приложения"""
    def __init__(self, driver, product_id):
        super().__init__(driver)
        self.driver = driver
        self.action = ActionChains(driver)
        self.product_id = product_id

    # locators
    catalog_button = "//button[@class='catalog__button catalog__button_catalog']"
    categories = "//li[starts-with(@class, 'catalog__list-item catalog__list')]"
    sub_categories_computer = "//*[@class='catalog__child-rubric-link']"
    close_region_confirmation_button = '//*[@class="js-cr-close cr-close"]'

    # getters
    def get_catalog_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.catalog_button)))

    def get_catalog_categories(self, category_name):
        """Получение списка ссылок на категории и возврат нужной из них"""
        categories = WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, self.categories)))
        category = list(filter(lambda x: x.text == category_name, categories))
        return category

    def get_catalog_sub_categories(self, sub_category_name):
        """Получение списка ссылок на подкатегории и возврат нужной из них"""
        sub_categories = WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, self.sub_categories_computer)))
        category = list(filter(lambda x: x.text == sub_category_name, sub_categories))
        return category

    def get_close_region_confirmation_button(self):
        return self.driver.find_element(By.XPATH, self.close_region_confirmation_button)
        #return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.close_region_confirmation_button)))

    # actions
    def click_catalog_button(self):
        self.get_catalog_button().click()

    def click_category(self, category_name):
         for category in self.get_catalog_categories(category_name):
            category.click()

    def click_sub_category(self, sub_category_name):
        for sub_category in self.get_catalog_sub_categories(sub_category_name):
            sub_category.click()

    def click_close_region_confirmation_button(self):
        try:
            if self.get_close_region_confirmation_button().is_displayed():
                self.get_close_region_confirmation_button().click()
        except:
            pass

    # methods
    def open_pumps_page(self, category_name, sub_category_name):
        """Открытие страницы каталога нужных категории и подкатегории"""
        self.click_catalog_button()
        print("\nМеню каталога открыто")
        self.click_close_region_confirmation_button()
        self.click_category(category_name)
        print(f"Выбрана категория {category_name}")
        self.click_sub_category(sub_category_name)
        print(f"Выбрана подкатегория {sub_category_name}")
        lp = ProductsPage(self.driver, self.product_id)
        return lp
