data = [4, -30, 100, -100, 123, 1, 0, -1, -4]

if __name__ == '__main__':
    # Без lambda
    result = [x[1] for x in sorted([(abs(x), x) for x in data])[::-1]]
    print(result)

    # С помощью lambda
    result_with_lambda = sorted(data, key=lambda x: (abs(x), x < 0))[::-1]
    print(result_with_lambda)