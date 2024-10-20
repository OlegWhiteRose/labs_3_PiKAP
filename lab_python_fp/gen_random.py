def gen_random(num_count, begin, end):
    import random
    for _ in range(num_count): yield random.randint(begin, end)


def print_gen(items):
    print(', '.join(map(str, items)))


def main():
    # Тест 1:
    print_gen(gen_random(5, 1, 3))
    # Тест 2:
    print_gen(gen_random(3, 4, 10))
    # Тест 3:
    print_gen(gen_random(3, 5, 5))


if __name__ == '__main__':
    main()
