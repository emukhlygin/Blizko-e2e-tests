import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from Base.BaseClass import BaseClass
from Pages.AddedToCartModal import AddedToCartModal


class ProductsPage(BaseClass):
    """Класс, описывающий страницу 'Насосы' категории 'Строительство и ремонт'"""
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.action = ActionChains(driver)

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
    chat_button = "[id=supportTrigger]"

    # getters
    def get_category_name(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.category_name)))

    def get_price_from(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.price_from)))

    def get_price_to(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.price_to)))

    def get_apply_filter_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.apply_filter_button)))

    def get_product_add_to_cart_button(self, product_id):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.product_add_to_cart_button.replace("product_id", product_id))))

    def get_product_name(self, product_id):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.product_name.replace("product_id", product_id))))

    def get_product_price(self, product_id):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.product_price.replace("product_id", product_id))))

    def get_expand_filter_list_buttons(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, self.expand_filter_list_buttons)))

    def get_filter_check(self, filter_name):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.filter_check.replace("filter_name", filter_name))))
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.filter_check.replace("filter_name", filter_name))))

    def get_chat_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.chat_button)))

    # actions
    def set_price_from(self, price_low):
        self.get_price_from().send_keys(price_low)

    def set_price_to(self, price_high):
        self.get_price_to().send_keys(price_high)

    def click_apply_filters_button(self):
        self.action.move_to_element(self.get_apply_filter_button()).click().perform()

    def click_product_add_to_cart_button(self, product_id):
        self.action.move_to_element(self.get_product_add_to_cart_button(product_id)).click().perform()

    def click_expand_filter_list_buttons(self):
        for button in self.get_expand_filter_list_buttons():
            self.action.move_to_element(button).click().perform()

    def click_filter_check(self, filter_name):
        element = self.get_filter_check(filter_name)
        self.action.scroll_to_element(element).move_to_element(element).click().perform()

    def delete_chat_button(self):
        self.get_chat_button()
        self.driver.execute_script(f"$('{self.chat_button}').remove()")

        # methods
    def aplly_all_filters(self, price_low, price_high, additional_filters):
        """Применение нужных фильтраций на список товаров"""
        self.set_price_from(price_low)
        self.set_price_to(price_high)
        if additional_filters:
            self.click_expand_filter_list_buttons()          # раскрытие всех списков фильтров
            for filter in additional_filters:
              self.click_filter_check(filter)
              time.sleep(0.5)                  # не удалось обойтись одними только ожиданиями для стабильного выбора фильтров
        self.click_apply_filters_button()
        print("Проведена фильтрация товаров")
        self.action.move_to_element(self.get_category_name()).perform()  # хак для того, чтобы избежать всплывающих селекторов бокового меню
        return self

    def add_product_to_cart(self, product_id):
        """Нажатие на кнопку добавления товара в корзину, сохранение его значений и открытие промежуточного модала"""
        self.delete_chat_button()                                       # удаление кнопки чата, чтобы она не мешала добавлять товар в корзину
        product_name = self.get_product_name(product_id).text
        product_price = self.get_product_price(product_id).text
        print(f"Выбран продукт {product_name} c ценой {product_price}")
        self.click_product_add_to_cart_button(product_id)
        print("Продукт добавлен в корзину")
        atc = AddedToCartModal(self.driver, product_name=product_name, product_price=product_price)
        return atc

    # asserts
    def assert_category_name_is_correct(self, sub_category_name):
        """Проверка того, что открылась страница нужной подкатегории товаров"""
        self.assert_element_name_is_correct(self.get_category_name(), sub_category_name)
        print(f"Открылась нужная страница подкатегории {sub_category_name}")
        return self


