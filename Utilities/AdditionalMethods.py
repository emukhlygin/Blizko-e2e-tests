def get_total_sum_for_product(product_price, additional_products):
    product_sum = product_price * (1+additional_products)
    formated_sum = '{0:,}'.format(product_sum).replace(',', ' ').replace(".0", '') + " руб."
    return formated_sum