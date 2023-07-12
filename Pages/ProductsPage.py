import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from Base.BaseClass import BaseClass
from Pages.AddedToCartModal import AddedToCartModal


class ProductsPage(BaseClass):
    """Класс, описывающий страницу 'Насосы' категории 'Строительство и ремонт'"""
    def __init__(self, driver, product_id):
        super().__init__(driver)
        self.driver = driver
        self.action = ActionChains(driver)
        self.product_id = product_id

    # locators
    category_name = "//ul[@class='breadcrumbs']/li[2]/a"
    price_from = "//input[@aria-label='Цена  от']"
    price_to = "//input[@aria-label='Цена до']"
    apply_filter_button = '//button[@class="b-order-button js-b-order-button-facet"]'
    product_add_to_cart_button = f"//button[contains(@data-add-orders-item-data, 'product_id')]"
    product_name = f"//*[contains(@class, 'cp-title js-balloon-title')]/a[@data-event-item='product_id']"
    product_price = f"//*[@data-product-id='product_id']//i[contains(@class, 'price')]"
    expand_filter_list_buttons = "//span[contains(text(), 'Посмотреть все')]"
    filter_check = "//*[contains(text(), 'filter_name')]/../input"

    # getters
    def get_category_name(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.category_name)))

    def get_price_from(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.price_from)))

    def get_price_to(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.price_to)))

    def get_apply_filter_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.apply_filter_button)))

    def get_product_add_to_cart_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.product_add_to_cart_button.replace("product_id", self.product_id))))

    def get_product_name(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.product_name.replace("product_id", self.product_id))))

    def get_product_price(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.product_price.replace("product_id", self.product_id))))

    def get_expand_filter_list_buttons(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, self.expand_filter_list_buttons)))

    def get_filter_check(self, filter_name):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.filter_check.replace("filter_name", filter_name))))

    # actions
    def set_price_from(self, price_low):
        self.get_price_from().send_keys(price_low)

    def set_price_to(self, price_high):
        self.get_price_to().send_keys(price_high)

    def click_apply_filters_button(self):
        self.action.move_to_element(self.get_apply_filter_button()).click().perform()

    def click_product_add_to_cart_button(self):
        self.action.move_to_element(self.get_product_add_to_cart_button()).click().perform()
        # self.get_product_add_to_cart_button().click()

    def click_expand_filter_list_buttons(self):
        for button in self.get_expand_filter_list_buttons():
            self.action.move_to_element(button).click().perform()

    def click_filter_check(self, filter_name):
        element = self.get_filter_check(filter_name)
        self.action.scroll_to_element(element).move_to_element(element).click().perform()

    # methods
    def aplly_all_filters(self, price_low, price_high, additional_filters):
        """Применение нужных фильтраций на список товаров"""
        if additional_filters:
            self.click_expand_filter_list_buttons()
            for filter in additional_filters:
                self.click_filter_check(filter)
                time.sleep(1)
        self.set_price_from(price_low)
        self.set_price_to(price_high)
        self.click_apply_filters_button()
        print("Проведена фильтрация товаров")
        self.action.move_to_element(self.get_category_name()).perform()  # хак для того, чтобы избежать всплывающих селекторов
        return self

    def add_product_to_cart(self):
        """Нажатие на кнопку добавления товара в корзину, сохранение его значений и открытие промежуточного модала"""
        product_name = self.get_product_name().text
        product_price = self.get_product_price().text
        print(f"Выбран продукт {product_name} c ценой {product_price}")
        self.click_product_add_to_cart_button()
        print("Продукт добавлен в корзину")
        atc = AddedToCartModal(self.driver, product_name=product_name, product_price=product_price)
        return atc

    # asserts
    def assert_category_name_is_correct(self, sub_category_name):
        """Проверка того, что открылась страница нужной подкатегории товаров"""
        self.AssertElementName(self.get_category_name(), sub_category_name)
        print(f"Открылась нужная страница подкатегории {sub_category_name}")
        return self


