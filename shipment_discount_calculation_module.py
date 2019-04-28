import datetime


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

DISCOUNT_LIMIT = 10


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
            return False
        return True

    @staticmethod
    def validate_package_size(size, data):
        for key, value in data.items():
            for val in value:
                if size == val:
                    return True
        return False

    @classmethod
    def validate_line_format(cls, line, data):
        valid = True
        validated_data = {}

        for item in line:
            if cls.validate_date(item):
                validated_data['date'] = True
            if cls.validate_provider(item, data):
                validated_data['provider'] = True
            if cls.validate_package_size(item, data):
                validated_data['size'] = True
        if len(validated_data) < 3:
            valid = False
        return valid


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


def get_package_sizes(data):
    sizes = []
    for key, value in data.items():
        for size, price in value.items():
            if size not in sizes:
                sizes.append(size)
    return sizes


def get_providers(data):
    return [key for key, value in data.items()]


def get_price(provider, size, data):
    return data[provider][size]


def output_data(data):
    for out in data:
        print(' '.join(out))
    return True


data = read_data('input.txt')


ordered_data = order_data_asc(data)


def process_input_data(content):
    accumulated_discounts = {}
    result = []
    l_discount = {}
    for item in content:
        item = item.split()
        if not ShipmentValidator.validate_line_format(item, DATA):
            item.append('Ignored')
        if "S" in item and 'Ignored' not in item:
            item.append(lowest_price(DATA))

        result.append(item)

    for item in result:
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
            else:
                for size in get_package_sizes(DATA):
                    if size in item:
                        for provider in get_providers(DATA):
                            if provider in item:
                                price = get_price(provider, size, DATA)
                                item.append(price)
        else:
            for size in get_package_sizes(DATA):
                if size != 'S' and size in item:
                    for provider in get_providers(DATA):
                        if provider in item:
                            item.append(get_price(provider, size, DATA))
    result = append_discount(result, DATA)
    return result


def lowest_price(provider_pricing, package_size='S'):
    small_price = []
    for key, value in provider_pricing.items():
        small_price.append(value[package_size])
    small_price.sort()
    return small_price[:1][0]


def append_discount(query, data):
    accumulated_discounts = {}
    accumulation = False
    accumulation_applied = False
    discount_left = 0
    result = []
    for item in query:
        if 'Ignored' not in item:
            month = datetime.datetime.strptime(item[0], '%Y-%m-%d').month
            size = item[1]
            provider = item[2]
            price = item[3]

            original_price = get_price(provider, size, data)
            if float(price) < float(original_price):
                reduction = (float(original_price) - float(price))
                if month in accumulated_discounts:
                    if accumulated_discounts[month] + reduction < DISCOUNT_LIMIT:
                        accumulated_discounts[month] += reduction
                    else:
                        accumulation = True
                        discount_left = round(DISCOUNT_LIMIT - accumulated_discounts[month], 2)
                        accumulated_discounts[month] = DISCOUNT_LIMIT
                else:
                    if reduction > DISCOUNT_LIMIT:
                        accumulated_discounts[month] = DISCOUNT_LIMIT
                    else:
                        accumulated_discounts[month] = reduction
            if not accumulation:
                discount = float(original_price) - float(price)
                discount = '-' if discount <= 0 else "%.2f" % discount
                item.append(discount)
            elif not accumulation_applied:
                actual_price = float(get_price(provider, size, data))
                item[3] = ("%.2f" % (actual_price - discount_left))
                item.append("%.2f" % discount_left)
                accumulation = False
        result.append(item)
    return result


# processed_data = process_input_data(ordered_data)

# output_data(ordered_data)

linas = process_input_data(ordered_data)

output_data(linas)

# print(get_providers(DATA))



# print(ShipmentValidator.validate_provider('MR', DATA))
# process_input_data()

# veikia = ShipmentValidator.validate_line_format('2015-02-01 S MR', DATA)
