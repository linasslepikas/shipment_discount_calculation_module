DATA = {
    "LP": {
        "S": "1.50",
        "M": "4.90",
        "L": "6.90"
    },
    "MR": {
        "S": "2",
        "M": "3",
        "L": "4"
    }
}


def process_input_data(data='input.txt'):
    input_data = {}
    with open(data) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for item in content:
        data = item.split()
        if "S" in data:
            data.append(lowest_price(DATA))
        print(data)
        # input_data.append(item)

    return input_data


def lowest_price(provider_pricing, package_size='S'):
    small_price = []
    for key, value in provider_pricing.items():
        small_price.append(value[package_size])
    small_price.sort()
    return small_price[:1][0]


def add_smallest_price(*args):
    pass


def validate_provider(provider, data):
    for key, value in data.items():
        if key == provider:
            return True
    return False


def validate_date(date):
    return False


def validate_package_size(data):
    return False
