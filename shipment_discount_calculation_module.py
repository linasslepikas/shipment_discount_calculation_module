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


def process_input_data(data='input.txt'):
    input_data = {}
    output_data = []
    with open(data) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    # counting L discount
    print(content)
    dates = []
    for item in content:
        row = item.split()
        dates.append(row[0])

    sorted_dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

    dates_list = []

    for item in sorted_dates:
        row = item.split()
        dates_list.append(row)
    # print(dates_list)

    for item in content:
        for date in dates_list:
            if item.split(" ")[0] in date:
                for a in item.split(" ")[1:]:
                    date.append(a)

    print(dates_list)



    l_discount = {}
    for item in content:
        row = item.split()
        if 'L' in row and 'LP'in row:
            month = datetime.datetime.strptime(row[0], '%Y-%m-%d').month
            try:
                l_discount[month].append(row[0])
            except KeyError:
                l_discount[month] = [row[0]]
                l_discount['discount_{}'.format(month)] = False

            if len(l_discount[month]) == 3 and not l_discount['discount_{}'.format(month)]:
                row.append('0.00')
                l_discount['discount_{}'.format(month)] = True
        # print(row)

    # print(l_discount)

    # datetime_object = datetime.datetime.strptime('2012-09-22', '%Y-%m-%d')
    # print(datetime_object.month)

    for item in content:
        data = item.split()
        # print(data)
        if len(data) != 3:
            data.append('Ignored')
        if "S" in data:
            data.append(lowest_price(DATA))
        output_data.append(data)
        # input_data.append(item)
    # for output in output_data:
    #     print(' '.join(output))


def lowest_price(provider_pricing, package_size='S'):
    small_price = []
    for key, value in provider_pricing.items():
        small_price.append(value[package_size])
    small_price.sort()
    return small_price[:1][0]


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
process_input_data()