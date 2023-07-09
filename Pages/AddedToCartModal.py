import time

from selenium import *
from Base.BaseClass import BaseClass
from Pages.CartPage import CartPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class AddedToCartModal(BaseClass):
    """Класс, описывающий модал, который открывается после нажатия кнопки добавления продукта в корзину"""
    def __init__(self, driver, product_price, product_name):
        super().__init__(driver)
        self.product_price = product_price
        self.product_name = product_name
        self.driver = driver
        self.final_price = ''

    # Locators
    add_more_product_button = "//*[@class='ui-icon ui-icon-triangle-1-n']"
    go_to_cart_button = "//*[contains(text(), 'Перейти к оформлению')]"
    product_name_in_modal = "//*[@class='orders-item-description-container']/p"
    product_total_price = "//*[@class='orders-item-total js-orders-item-total']"

    # getters
    def get_add_more_product_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add_more_product_button)))

    def get_go_to_cart_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.go_to_cart_button)))

    def get_product_name(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.product_name_in_modal)))

    def get_product_price(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.product_total_price)))

    # actions
    def click_add_more_product_button(self):
        self.get_add_more_product_button().click()

    def click_go_to_cart_button(self):
        self.get_go_to_cart_button().click()

    # methods
    def count_final_price(self, times):
        """Цена товара умножается на его количество и преобразуется в значение, которое будет сравниваться"""
        #self.final_price = str(float(self.product_price)*(times+1)).replace(".0", '')+" руб."
        sum = float(self.product_price)*(times+1)
        formated_sum = '{0:,}'.format(sum).replace(',', ' ').replace(".0", '')
        self.final_price = formated_sum +" руб."

        print(f"Итогая стоимость выбранного количества товара - {self.final_price}")

    def add_more_units_of_product(self, times):
        """Добавление дополнительных единиц товара times раз"""
        for _time in range(times):
            self.click_add_more_product_button()
        print(f"Добавлено дополнительно еще {times} единиц товара")
        self.count_final_price(times)
        return self

    def go_to_cart_from_modal(self):
        """Переход из промежуточного модала в корзину"""
        self.click_go_to_cart_button()
        cp = CartPage(self.driver, product_price=self.final_price, product_name=self.product_name)
        print("Переход в корзину")
        return cp

    def wait_until_correct_price_is_displayed(self):
        """Ожидание правильного отображения итоговой суммы"""
        try:
            WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element(locator=(By.XPATH, self.product_total_price), text_=self.final_price))
        except:
            exception = Exception("PriceIsWrong")
            raise exception

    # asserts
    def assert_product_and_sum_in_modal_is_correct(self):
        """Проверка правильности товара и корректной стоимости выбранного количества единиц товара"""
        assert self.product_name == self.get_product_name().text
        self.wait_until_correct_price_is_displayed()
        print("Наименование товара и стоимость отображаются корректно в промежуточном модале")
        return self
