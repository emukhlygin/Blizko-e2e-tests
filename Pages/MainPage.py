from selenium.webdriver import ActionChains
from Base.BaseClass import BaseClass
from Pages.CartPage import CartPage
from Pages.LoginModal import LoginModal
from Pages.ProductsPage import ProductsPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BaseClass):
    """Класс, описывающий основную страницу приложения"""
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.action = ActionChains(driver)

    # locators
    catalog_button = "//button[@class='catalog__button catalog__button_catalog']"
    categories = "//li[starts-with(@class, 'catalog__list-item catalog__list')]"
    sub_categories_computer = "//*[@class='catalog__child-rubric-link']"
    cart_button = "//a[contains(@class, 'link_cart')]"
    product_counter = "//span[contains(@class, 'js-orders-cart-counter-value')]"
    login_button = "//span[contains(text(), 'Войти')]"

    # getters
    def get_catalog_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.catalog_button)))

    def get_catalog_categories(self, category_name):
        """Получение списка ссылок на категории и возврат нужной из них"""
        categories = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, self.categories)))
        category = list(filter(lambda x: x.text == category_name, categories))
        return category

    def get_catalog_sub_categories(self, sub_category_name):
        """Получение списка ссылок на подкатегории и возврат нужной из них"""
        sub_categories = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, self.sub_categories_computer)))
        category = list(filter(lambda x: x.text == sub_category_name, sub_categories))
        return category

    def get_cart_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.cart_button)))

    def get_product_counter(self):
        return self.driver.find_element(By.XPATH, self.product_counter)

    def get_login_button(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, self.login_button)))

    # actions
    def click_catalog_button(self):
        self.get_catalog_button().click()

    def click_category(self, category_name):
         for category in self.get_catalog_categories(category_name):
            category.click()

    def click_sub_category(self, sub_category_name):
        for sub_category in self.get_catalog_sub_categories(sub_category_name):
            sub_category.click()

    def click_cart_button(self):
        self.get_cart_button().click()

    def click_login_button(self):
        self.get_login_button().click()

    def get_number_of_products_in_cart(self):
        return self.get_product_counter().text

    # methods
    def open_product_page(self, category_name, sub_category_name):
        """Открытие страницы каталога нужных категории и подкатегории"""
        self.click_close_alert_button()          # закрытие приодически появляющейся нотификации
        self.click_close_region_confirmation_button()             # закрытие периодически появляющегося конфирмейшен диалога
        self.click_catalog_button()
        print("\nМеню каталога открыто")
        self.click_category(category_name)
        print(f"Выбрана категория {category_name}")
        self.click_sub_category(sub_category_name)
        print(f"Выбрана подкатегория {sub_category_name}")
        lp = ProductsPage(self.driver)
        return lp

    def enter_cart(self):
        """Переход в корзины из главной страницы"""
        self.click_cart_button()
        cp = CartPage(self.driver)
        return cp

    def enter_login_modal(self):
        """Открытие модала авторизации"""
        self.click_login_button()
        lp = LoginModal(self.driver)
        return lp
