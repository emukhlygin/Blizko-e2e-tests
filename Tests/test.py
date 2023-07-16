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
from Utilities.AdditionalMethods import get_total_sum_for_product
from Utilities.TestData import TestData


@pytest.mark.parametrize('data_set', TestData.data_sets) #TestData.random_data_set(2))
def test_select_product(set_up, data_set):
    """Тест-кейс: выбор продукта, добавление его в корзину"""
    main_page = MainPage(driver=set_up)

    main_page.open_product_page(category_name=data_set["category"],
                                sub_category_name=data_set["sub_category"],
                                product_id=data_set["product_id"])\
        .assert_category_name_is_correct(data_set["sub_category"])\
        .aplly_all_filters(price_low=data_set["price_low"],
                           price_high=data_set["price_high"],
                           additional_filters=data_set["additional_filters"])\
        .add_product_to_cart()\
        .add_more_units_of_product(data_set["times"])\
        .assert_product_and_sum_in_modal_is_correct()\
        .go_to_cart_from_modal()\
        .assert_product_and_price_in_cart_is_correct()\
        .go_to_final_buy_page()\
        .assert_product_and_price_in_final_page_is_correct()


# def test_select_two_products(set_up, data_sets=TestData.random_data_set(2)):
#     """Тест-кейс: выбор продукта, добавление его в корзину"""
#     driver = set_up
#     main_page = MainPage(driver=driver)
#
#     products_details = {}
#
#     for data_set in data_sets:
#         main_page.open_product_page(category_name=data_set["category"],
#                                     sub_category_name=data_set["sub_category"],
#                                     product_id=data_set["product_id"])\
#             .assert_category_name_is_correct(data_set["sub_category"])\
#             .aplly_all_filters(price_low=data_set["price_low"],
#                                price_high=data_set["price_high"],
#                                additional_filters=data_set["additional_filters"])\
#             .add_product_to_cart()\
#             .add_more_units_of_product(data_set["times"])\
#             .assert_product_and_sum_in_modal_is_correct()\
#             .close_modal_and_go_to_main_page()
#
#         products_details[data_set["product_name"]] = get_total_sum_for_product(data_set["product_price"], data_set["times"])
#
#     main_page.enter_cart()\
#         .assert_total_prices_for_all_products_are_correct(products_details)




