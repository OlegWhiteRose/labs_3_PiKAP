from main import *

# Тесты
    
import unittest

class TestSyntaxFunctions(unittest.TestCase):
    def test_get_sorted_syntax_by_language(self):
        result = get_sorted_syntax_by_language()
        expected = [
            ('Класс', 0.05, 'Java'), 
            ('Условный оператор if', 0.01, 'C++'), 
            ('Функция', 0.04, 'Python'), 
            ('Цикл do while', 0.01, 'C++'), 
            ('Цикл for', 0.02, 'C')
        ]

        self.assertEqual(result, expected)

    def test_get_languages_by_execution_time(self):
        result = get_languages_by_execution_time()
        expected = [
            ('Java', 0.05),
            ('Python', 0.04),
            ('C++', 0.02),
            ('C', 0.02)
        ]
        self.assertEqual(result, expected)

    def test_get_languages_with_c_and_syntax(self):
        result = get_languages_with_c_and_syntax()
        expected = {
            'C++': ['Функция', 'Цикл do while', 'Условный оператор if', 'Цикл for', 'Класс'],
            'C': ['Функция', 'Цикл do while', 'Условный оператор if', 'Цикл for']
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
