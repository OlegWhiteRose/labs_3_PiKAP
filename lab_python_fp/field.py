def field(items, *args):
    assert len(args) > 0

    for item in items:
        res = {}
        for arg in args:
            if arg in item and item[arg] is not None:
                res[arg] = item[arg]
        if res:
            yield res


def print_field(items):
    print(', '.join(map(str, items)))


def main():
    # Пример:
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
    ]
    print_field(field(goods, 'title'))  # Должен выдавать 'Ковер', 'Диван для отдыха'
    print_field(field(goods, 'title', 'price'))  # Должен выдавать {'title': 'Ковер', 'price': 2000}, {'title': 'Диван для отдыха', 'price': 5300}

    # Тест 1:
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'}
    ]
    print_field(field(goods, 'title', 'price'))  # Должен выдавать {'title': 'Ковер', 'price': 2000}, {'title': 'Диван для отдыха'}

    # Тест 2:
    goods = [
        {'title': 'Ковер', 'price': None, 'color': 'green'},
        {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
    ]
    print_field(field(goods, 'title', 'price'))  # Должен выдавать {'title': 'Ковер'}, {'title': 'Диван для отдыха', 'price': 5300}


if __name__ == '__main__':
    main()
