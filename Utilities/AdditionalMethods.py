def get_total_sum(products_details):
    total_sum = sum(products_details.values())
    formated_sum = '{0:,}'.format(total_sum).replace(',', ' ').replace(".0", '') + " руб."
    return formated_sum