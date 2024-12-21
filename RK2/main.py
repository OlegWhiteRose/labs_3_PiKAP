from operator import itemgetter


class Syntax:
    """Синтаксическая конструкция"""
    def __init__(self, id, name, execution_time, lang_id):
        self.id = id
        self.name = name
        self.execution_time = execution_time
        self.lang_id = lang_id


class Language:
    """Язык программирования"""
    def __init__(self, id, name):
        self.id = id
        self.name = name


class SyntaxLang:
    """Связь синтаксических конструкций и языков программирования для отношения многие-ко-многим"""
    def __init__(self, lang_id, syntax_id):
        self.lang_id = lang_id
        self.syntax_id = syntax_id


# Языки программирования
langs = [
    Language(1, 'Python'),
    Language(2, 'Java'),
    Language(3, 'C++'),
    Language(4, 'C')
]

# Синтаксические конструкции
syntaxes = [
    Syntax(1, 'Функция', 0.04, 1),
    Syntax(2, 'Цикл do while', 0.01, 3),
    Syntax(3, 'Условный оператор if', 0.01, 3),
    Syntax(4, 'Цикл for', 0.02, 4),
    Syntax(5, 'Класс', 0.05, 2)
]

# Связи многие-ко-многим
syntax_langs = [
    SyntaxLang(1, 1),
    SyntaxLang(1, 3),
    SyntaxLang(1, 4),
    SyntaxLang(1, 5),
    SyntaxLang(2, 1),
    SyntaxLang(2, 2),
    SyntaxLang(2, 3),
    SyntaxLang(2, 4),
    SyntaxLang(2, 5),
    SyntaxLang(3, 1),
    SyntaxLang(3, 2),
    SyntaxLang(3, 3),
    SyntaxLang(3, 4),
    SyntaxLang(3, 5),
    SyntaxLang(4, 1),
    SyntaxLang(4, 2),
    SyntaxLang(4, 3),
    SyntaxLang(4, 4)
]

# Функции

def get_sorted_syntax_by_language():
    """Задание A1: список связанных конструкций и языков, отсортированный по конструкциям"""
    one_to_many = [(s.name, s.execution_time, l.name) for l in langs for s in syntaxes if s.lang_id == l.id]
    return sorted(one_to_many, key=itemgetter(0))


def get_languages_by_execution_time():
    """Задание A2: список языков с суммарным временем выполнения конструкций, отсортированный по времени"""
    one_to_many = [(s.name, s.execution_time, l.name) for l in langs for s in syntaxes if s.lang_id == l.id]
    result = []
    for l in langs:
        l_syntaxes = list(filter(lambda i: i[2] == l.name, one_to_many))
        if l_syntaxes:
            l_execution_times = [time for _, time, _ in l_syntaxes]
            result.append((l.name, sum(l_execution_times)))
    return sorted(result, key=itemgetter(1), reverse=True)


def get_languages_with_c_and_syntax():
    """Задание A3: список всех языков с "C" в названии и их синтаксических конструкций"""
    many_to_many_temp = [(l.name, sl.lang_id, sl.syntax_id) for l in langs for sl in syntax_langs if l.id == sl.lang_id]
    many_to_many = [(s.name, s.execution_time, lang_name)
                    for lang_name, lang_id, syntax_id in many_to_many_temp
                    for s in syntaxes if s.id == syntax_id]
    result = {}
    for l in langs:
        if 'C' in l.name:
            l_syntaxes = list(filter(lambda i: i[2] == l.name, many_to_many))
            result[l.name] = [x for x, _, _ in l_syntaxes]
    return result
