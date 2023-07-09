class BaseClass():

    def __init__(self, driver):
        self.driver = driver

    def AssertProductIsPresent(self, elements, product_name):
        element = list(filter(lambda x: x.text == product_name, elements))
        assert len(element) == 1, "No such product is found"

    def AssertElementName(self, element, expected_result):
        actual_result = element.text
        assert expected_result == actual_result, "There is no element with such text"


