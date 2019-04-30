import unittest

from helper import ShipmentHelper
from processor import ShipmentProcessor

DATA = {
        "LP": {
            "S": "1.50",
            "M": "4.90",
            "L": "6.90"
        },
        "MR": {
            "S": "2.00",
            "M": "3.00",
            "L": "4.00"
        }
    }

ALLOWED_SIZES = ['S', 'M', 'L']
LOWEST_PRICE = "1.50"
MOCK = 'mock.txt'
PROVIDERS_COUNT = len(DATA)


class TestShipmentHelper(unittest.TestCase):

    def test_get_providers(self):
        providers = ShipmentHelper.get_providers(DATA)
        self.assertEqual(len(providers), PROVIDERS_COUNT)

    def test_get_providers_fail(self):
        success = True
        try:
            ShipmentHelper.get_providers('some data')
        except AttributeError:
            success = False
        self.assertFalse(success)
        self.assertRaises(AttributeError)

    def test_get_lowest_price(self):
        price = ShipmentHelper.get_lowest_price(DATA)
        self.assertEqual(LOWEST_PRICE, price)
        self.assertNotEqual(LOWEST_PRICE, "0.00")

    def test_get_price(self):
        price = ShipmentHelper.get_price("LP", "L", DATA)
        self.assertEqual("6.90", price)
        self.assertNotEqual("4.90", price)

    def test_read_file(self):
        price = ShipmentHelper.read_file(MOCK)
        self.assertGreater(len(price), 1)

    def test_get_package_sizes(self):
        sizes = ShipmentHelper.get_package_sizes(DATA)
        all_sizes = True
        for size in sizes:
            if size not in ALLOWED_SIZES:
                all_sizes = False
        self.assertEqual(len(sizes), 3)
        self.assertTrue(all_sizes)


class TestShipmentProcessor(unittest.TestCase):

    def test_order_data_asc(self):
        original = ShipmentHelper.read_file(MOCK)
        data = ShipmentProcessor.order_data_asc(ShipmentHelper.read_file(MOCK))
        self.assertEqual(len(original), len(data))
        self.assertNotEqual(original, data)

    def test_output_data(self):
        output = ShipmentProcessor.output_data(ShipmentHelper.read_file(MOCK))
        ordered_output = ShipmentProcessor.order_data_asc(ShipmentHelper.read_file(MOCK))
        self.assertTrue(output)
        self.assertTrue(ordered_output)

    def test_process_data(self):
        content = ShipmentProcessor.order_data_asc(ShipmentHelper.read_file(MOCK))
        data = ShipmentProcessor.process_data(content, DATA, 'S', 'L', 'Ignore', 'LP', '0.00', 10)
        self.assertEqual(len(content), len(data))


if __name__ == '__main__':
    unittest.main()
