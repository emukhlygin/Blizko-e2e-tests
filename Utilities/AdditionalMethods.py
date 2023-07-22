def get_total_sum_for_product(product_price, additional_products):
    """Вычисление итоговой суммы по товару и форматирование ее в тот вид, который отображается на странице"""
    product_sum = product_price * (1+additional_products)
    formated_sum = '{0:,}'.format(product_sum).replace(',', ' ').replace(".0", '') + " руб."
    return formated_sum
