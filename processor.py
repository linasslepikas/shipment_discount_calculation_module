import datetime

from helper import ShipmentHelper
from validator import ShipmentValidator


class ShipmentProcessor:

    @staticmethod
    def order_data_asc(data):
        """
        Order data by date in descending order
        :param data:
        :return: list:
        """
        dates = []
        for item in data:
            row = item.split()
            dates.append(row[0])

        # Checking for invalid dates and adding them to blacklist.
        blacklist = {}
        for date in dates:
            if not ShipmentValidator.validate_date(date):
                index = dates.index(date)
                dates.remove(date)
                blacklist[index] = date

        # Order dates in ASC order
        dates_in_asc_order = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

        # If there were invalid dates, we put them back were we found them, it will be processed later.
        if len(blacklist) > 0:
            for key, value in blacklist.items():
                dates_in_asc_order.insert(key, value)

        result = []
        # Mapping data back to the dates.
        for date in dates_in_asc_order:
            for key in data:
                if date in key.split():
                    # If that date is in the data, we add that data to result
                    result.append(key)
                    # We found data map. Remove this information from data set to avoid duplication and break this loop.
                    data.remove(key)
                    break
        return result

    @staticmethod
    def output_data(data):
        """Prints data to the console as STDOUT.
        :param data:
        :return: bool:
        """
        for out in data:
            print(' '.join(out))
        return True

    @staticmethod
    def append_discount(query, data, ignore, discount_limit):
        """ Appends discount to the data set.
        :param query:
        :param data:
        :param ignore:
        :param discount_limit:
        :return: list:
        """
        accumulated_discounts = {}
        accumulation = False
        accumulation_applied = False
        discount_left = 0
        result = []
        for item in query:
            if ignore not in item:
                month = datetime.datetime.strptime(item[0], '%Y-%m-%d').month
                size = item[1]
                provider = item[2]
                price = float(item[3])

                original_price = float(ShipmentHelper.get_price(provider, size, data))
                if price < original_price:
                    reduction = (original_price - price)
                    if month in accumulated_discounts:
                        if accumulated_discounts[month] + reduction < discount_limit:
                            accumulated_discounts[month] += reduction
                        else:
                            accumulation = True
                            discount_left = round(discount_limit - accumulated_discounts[month], 2)
                            accumulated_discounts[month] = discount_limit
                    else:
                        if reduction > discount_limit:
                            accumulated_discounts[month] = discount_limit
                        else:
                            accumulated_discounts[month] = reduction
                if not accumulation:
                    difference = original_price - price
                    discount = '-' if difference <= 0 else "%.2f" % difference
                    item.append(discount)
                elif not accumulation_applied:
                    actual_price = float(ShipmentHelper.get_price(provider, size, data))
                    item[3] = ("%.2f" % (actual_price - discount_left))
                    left = "%.2f" % discount_left if discount_left < 0 else '-'
                    item.append(left)
                    accumulation = False
            result.append(item)
        return result

    @classmethod
    def process_data(cls, content, data, small, large, ignore, free_provider, free_shipment, discount_limit):
        """Processes all data set and applies necessary logic.
        :param content:
        :param data:
        :param small:
        :param large:
        :param ignore:
        :param free_provider:
        :param free_shipment:
        :param discount_limit:
        :return:list:
        """
        result = []
        l_discount = {}
        for item in content:
            item = item.split()
            if not ShipmentValidator.validate_line_format(item, data):
                item.append(ignore)
            if small in item and ignore not in item:
                item.append(ShipmentHelper.get_lowest_price(data))

            result.append(item)

        for item in result:
            if large in item and free_provider in item:
                month = datetime.datetime.strptime(item[0], '%Y-%m-%d').month
                try:
                    l_discount[month].append(item[0])
                except KeyError:
                    l_discount[month] = [item[0]]
                    l_discount['discount_{}'.format(month)] = False

                if len(l_discount[month]) == 3 and not l_discount['discount_{}'.format(month)]:
                    item.append(free_shipment)
                    l_discount['discount_{}'.format(month)] = True
                else:
                    for size in ShipmentHelper.get_package_sizes(data):
                        if size in item:
                            for provider in ShipmentHelper.get_providers(data):
                                if provider in item:
                                    price = ShipmentHelper.get_price(provider, size, data)
                                    item.append(price)
            else:
                for size in ShipmentHelper.get_package_sizes(data):
                    if size != small and size in item:
                        for provider in ShipmentHelper.get_providers(data):
                            if provider in item:
                                item.append(ShipmentHelper.get_price(provider, size, data))

        result = cls.append_discount(result, data, ignore, discount_limit)

        return result
