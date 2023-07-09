import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import Tests.conftest
from Tests.conftest import *
from Pages.ProductsPage import ProductsPage
from Pages.MainPage import MainPage
from Pages.AddedToCartModal import AddedToCartModal
from Utilities.TestData import TestData


@pytest.mark.parametrize('data_set', TestData.data_sets)
def test_select_product(set_up, data_set):
    """Тест-кейс: выбор продукта, добавление его в корзину"""
    main_page = MainPage(driver=set_up, product_id=data_set["product_id"])

    main_page.open_pumps_page(category_name=data_set["category"],
                              sub_category_name=data_set["sub_category"])\
        .assert_category_name_is_correct(data_set["sub_category"])\
        .aplly_all_filters(price_low=data_set["price_low"],
                           price_high=data_set["price_high"])\
        .add_product_to_cart()\
        .add_more_units_of_product(data_set["times"])\
        .assert_product_and_sum_in_modal_is_correct()\
        .go_to_cart_from_modal()\
        .assert_product_and_price_in_cart_is_correct()\
        .go_to_final_buy_page()\
        .assert_product_and_price_in_final_page_is_correct()


