import datetime


class ShipmentValidator:

    @staticmethod
    def validate_input_format(file_name, allowed_formats):
        """ Validates if provided data file is in valid format.
        :param file_name:
        :param allowed_formats:
        :return: bool:
        """
        extension = file_name.split(".")[1]
        print()
        if extension not in allowed_formats:
            print('Input file format not valid, only {} files add expected.'.format(allowed_formats))
            exit(1)
        return True

    @staticmethod
    def validate_provider(provider, data):
        """Validates if provider is in data set.
        :param provider:
        :param data:
        :return: bool:
        """
        for key, value in data.items():
            if key == provider:
                return True
        return False

    @staticmethod
    def validate_date(date):
        """Validated if date is in right format.
        :param date:
        :return: bool:
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False
        return True

    @staticmethod
    def validate_package_size(size, data):
        """Validates if size is in data set.
        :param size:
        :param data:
        :return: bool:
        """
        for key, value in data.items():
            for val in value:
                if size == val:
                    return True
        return False

    @classmethod
    def validate_line_format(cls, line, data):
        """Validates if data row is in right format.
        :param line:
        :param data:
        :return: bool:
        """
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
