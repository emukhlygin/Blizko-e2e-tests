import time

from selenium import *
from Base.BaseClass import BaseClass
from Pages.FinalBuyPage import FinalBuyPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class CartPage(BaseClass):
    """Класс, описывающий страницу корзины"""
    def __init__(self, driver, product_price, product_name):
        super().__init__(driver)
        self.product_price = product_price
        self.product_name = product_name
        self.driver = driver

    # locators
    go_to_buy_page_button = "//button[contains(text(), 'Перейти к оформлению')]"
    cart_page_product_price = "//p[@class='orders-item__total js-orders-item__total']"
    cart_page_product_name = "//a[@class='orders-item__title']"

    # getters
    def get_go_to_buy_page_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.go_to_buy_page_button)))

    def get_cart_page_product_price(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.cart_page_product_price)))

    def get_cart_page_product_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.cart_page_product_name)))

    # actions
    def click_go_to_buy_page_button(self):
        self.get_go_to_buy_page_button().click()

    # methods
    def go_to_final_buy_page(self):
        """Переход на страницу оформления заказа"""
        self.click_go_to_buy_page_button()
        print("Переход на страницу оформления заказа")
        fbp = FinalBuyPage(self.driver, product_price=self.product_price, product_name=self.product_name)
        return fbp

    # asserts
    def assert_product_and_price_in_cart_is_correct(self):
        """Проверка правильности товара и корректной стоимости выбранного количества единиц товара"""
        assert self.product_price == self.get_cart_page_product_price().text
        assert self.product_name == self.get_cart_page_product_name().text
        print("Товар и его стоимость отображаются в корзине корректно")
        return self


