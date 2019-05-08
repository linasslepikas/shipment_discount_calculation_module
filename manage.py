import sys

from helper import ShipmentHelper
from validator import ShipmentValidator
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
ALLOWED_FORMATS = ['txt']
DISCOUNT_LIMIT = 10
DEFAULT_FILE_PATH = 'input.txt'
IGNORE_INVALID = 'Ignored'
FREE_SHIPMENT = '0.00'
FREE_PROVIDER = 'LP'

SMALL = 'S'
LARGE = 'L'

try:
    INPUT_FILE_PATH = sys.argv[1]
except IndexError:
    INPUT_FILE_PATH = DEFAULT_FILE_PATH

ShipmentValidator.validate_input_format(INPUT_FILE_PATH, ALLOWED_FORMATS)

processor = ShipmentProcessor(DATA, INPUT_FILE_PATH)

processor.output_data(
    processor.process_data(
        processor.order_data_asc(),
        DATA, SMALL, LARGE, IGNORE_INVALID, FREE_PROVIDER, FREE_SHIPMENT, DISCOUNT_LIMIT))
