import unittest

from helper import ShipmentHelper


class TestShippingMethods(unittest.TestCase):
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

    PROVIDERS_COUNT = len(DATA)

    def test_get_providers(self):
        providers = ShipmentHelper.get_providers(self.DATA)
        self.assertEqual(len(providers), self.PROVIDERS_COUNT)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
