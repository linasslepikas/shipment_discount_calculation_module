PRICING = {
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
    input_data = []
    with open(data) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    # print(content)
    for item in content:
        input_data.append(item)

    print(input_data)


def lowest_price(provider_pricing, package_size='S'):
    small_price = []
    for key, value in provider_pricing.items():
        small_price.append(value[package_size])
    small_price.sort()
    return small_price[:1][0]
