class Unique:
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.used = set()
        self.items = iter(items) 


    def __next__(self):
        for item in self.items:
            if isinstance(item, str) and self.ignore_case:
                item = item.lower()

            if item not in self.used:
                self.used.add(item)
                return item

        raise StopIteration


    def __iter__(self):
        return self


def print_iter(items):
    print(', '.join(map(str, items)))


def main():
    # Тест 1:
    data = [1, 1, 1, 1, 2, 2, 3, 3]
    print_iter(Unique(data)) # Должен выдавать: 1, 2, 3

    # Тест 2:
    from gen_random import gen_random
    data = gen_random(10, 1, 3)
    print_iter(Unique(data)) 

    # Тест 3:
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    print_iter(Unique(data, ignore_case = True)) # Должен выдавать: a, b

    # Тест 4:
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    print_iter(Unique(data)) # Должен выдавать: a, A, b, B


if __name__ == '__main__':
    main()