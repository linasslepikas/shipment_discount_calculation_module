import datetime


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


# 1. validating input format
def validate_input_format(data):
    extension = data.split(".")[1]
    print(extension)
    if extension != 'txt':
        print('Input file format not valid, only .txt files add expected.')
        exit(1)
    return True


# 2. Read input format
def read_data(data):
    with open(data) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


# 3. Order data by date in descending order
def order_data_asc(data):
    dates = []
    for item in data:
        row = item.split()
        dates.append(row[0])

    # Order dates in ASC order
    dates_in_asc_order = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    output = []
    # Looping via dates
    for date in dates_in_asc_order:
        # Looping via data provider
        for key in data:
            if date in key.split():
                # if that date is in the data provider, we add that data to output
                output.append(key)
                # since we found data map we remove this information from data ser to avoid duplication
                data.remove(key)
                break
    return output


def output_data(data):
    output = []
    for item in data:
        output.append(' '.join(item))
    for out in output:
        print(out)
    return True




data = read_data('input.txt')

ordered_data = order_data_asc(data)







def process_input_data(content):
    output_data = []
    l_discount = {}
    for item in content:
        if 'L' in item and 'LP'in item:
            month = datetime.datetime.strptime(item[0], '%Y-%m-%d').month
            try:
                l_discount[month].append(item[0])
            except KeyError:
                l_discount[month] = [item[0]]
                l_discount['discount_{}'.format(month)] = False

            if len(l_discount[month]) == 3 and not l_discount['discount_{}'.format(month)]:
                item.append('0.00')
                l_discount['discount_{}'.format(month)] = True

    for item in content:
        if len(item) < 3:
            item.append('Ignored')
        if "S" in item:
            item.append(lowest_price(DATA))
        output_data.append(item)

    return output_data


def lowest_price(provider_pricing, package_size='S'):
    small_price = []
    for key, value in provider_pricing.items():
        small_price.append(value[package_size])
    small_price.sort()
    return small_price[:1][0]


# processed_data = process_input_data(ordered_data)

output_data(ordered_data)


def add_smallest_price(*args):
    pass


class ShipmentValidator:

    @staticmethod
    def validate_provider(provider, data):
        for key, value in data.items():
            if key == provider:
                return True
        return False

    @staticmethod
    def validate_date(date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print('Incorrect data format, should be YYYY-MM-DD')
            return False
        return True

    @staticmethod
    def validate_package_size(data):
        return False


# print(ShipmentValidator.validate_provider('MR', DATA))
# process_input_data()