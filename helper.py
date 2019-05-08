class ShipmentHelper:

    @staticmethod
    def get_lowest_price(provider_pricing, package_size='S'):
        """ Gets smallest price from price list according to package size.
        :param provider_pricing:
        :param package_size:
        :return: string:
        """
        prices = []
        for key, value in provider_pricing.items():
            for size, price in value.items():
                if size == package_size:
                    prices.append(price)
        prices.sort()
        return prices[:1][0]

    @staticmethod
    def get_price(provider, size, data):
        """
        Gets price from price list according to selected provider and package size.
        :param provider:
        :param size:
        :param data:
        :return: string:
        """
        return data[provider][size]

    @staticmethod
    def read_file(file_path):
        """Loops overs rows of data in file and puts each row to the list.
        :param file_path:
        :return: list:
        """
        with open(file_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content

    @staticmethod
    def get_package_sizes(data):
        """Gets all available package sizes
        :param data:
        :return: list:
        """
        sizes = []
        for key, value in data.items():
            for size, price in value.items():
                if size not in sizes:
                    sizes.append(size)
        return sizes

    @staticmethod
    def get_providers(data):
        """Gets all providers. In this context we do not care if they unique.
        :param data:
        :return: list:
        """
        return [key for key, value in data.items()]

