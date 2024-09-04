#
# Команда для компиляции
# python -m unittest .\unittest.py
from math import sqrt
import unittest
# Формат кода в unittest

# По формату написания тестов она сильно напоминает библиотеку JUnit, используемую  в языке Java для написания тестов:

    # тесты должны быть написаны в классе;
    # класс должен быть отнаследован от базового класса unittest.TestCase;
    # имена всех функций, являющихся тестами, должны начинаться с ключевого слова test;
    # внутри функций должны быть вызовы операторов сравнения (assertX) — именно они будут проверять наши полученные значения на соответствие заявленным.

def square_eq_solver(a, b, c):
   result = []
   discriminant = b * b - 4 * a * c

   if discriminant == 0:
       result.append(-b / (2 * a))
   elif discriminant > 0:  # <--- изменили условие, теперь
                           # при нулевом дискриминанте
                           # не будут вычисляться корни
       result.append((-b + sqrt(discriminant)) / (2 * a))
       result.append((-b - sqrt(discriminant)) / (2 * a))

   return result
class SquareEqSolverTestCase(unittest.TestCase):
    def test_no_root(self):
        res = square_eq_solver(10,0,2)
        self.assertEqual(len(res),0)

    def test_signle_root(self):
        res = square_eq_solver(10,0,0)
        self.assertEqual(len(res),1)
        self.assertEqual(res, [0])

    def test_muptiple_root(self):
        res = square_eq_solver(2,5,-3)
        self.assertEqual(len(res),2)
        self.assertEqual(res, [0.5, -3])

# Unittest: аргументы “за”

#     Является частью стандартной библиотеки языка Python: не нужно устанавливать ничего дополнительно;
#     Гибкая структура и условия запуска тестов. Для каждого теста можно назначить теги, в соответствии с которыми будем запускаться либо одна, либо другая группа тестов;
#     Быстрая генерация отчетов о проведенном тестировании, как в формате plaintext, так и в формате XML.

# Unittest: аргументы “против”

#     Для проведения тестирования придётся написать достаточно большое количество кода (по сравнению с другими библиотеками);
#     Из-за того, что разработчики вдохновлялись форматом библиотеки JUnit, названия основных функций написаны в стиле camelCase (например setUp и assertEqual);
#     В языке python согласно рекомендациям pep8 должен использоваться формат названий snake_case (например set_up и assert_equal).

