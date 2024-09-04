# Pytest
# Написание тестов здесь намного проще, нежели в unittest. Вам нужно просто написать несколько функций, удовлетворяющих следующим условиям:

    # Название функции должно начинаться с ключевого слова test;
    # Внутри функции должно проверяться логическое выражение при помощи оператора assert.

# Команда для компиляции  
# pytest .\lesson_pytest.py
import pytest
from math import sqrt
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
def test_no_root():
    res = square_eq_solver(10, 0, 2)
    assert len(res) == 0

def test_single_root():
    res = square_eq_solver(10, 0, 0)
    assert len(res) == 1
    assert res == [0]

def test_multiple_root():
    res = square_eq_solver(2, 5, -3)
    assert len(res) == 2
    assert res == [0.5,-3]

# Pytest: аргументы “за”

#     Позволяет писать компактные (по сравнению с unittest) наборы тестов;
#     В случае возникновения ошибок выводится гораздо больше информации о них;
#     Позволяет запускать тесты, написанные для других тестирующих систем;
#     Имеет систему плагинов (и сотни этих самых плагинов), расширяющую возможности фреймворка. Примеры таких плагинов: pytest-cov, pytest-django, pytest-bdd;
#     Позволяет запускать тесты в параллели (при помощи плагина pytest-xdist).

# Pytest: аргументы “против”

#     pytest не входит в стандартную библиотеку языка Python. Поэтому его придётся устанавливать отдельно при помощи команды pip install pytest;
#     совместимость кода с другими фреймворками отсутствует. Так что, если напишете код под pytest, запустить его при помощи встроенного unittest не получится