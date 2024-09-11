def squares(numbers):
    sum_square = 0
    for num in numbers:
        if  num.isdigit() and int(num) % 2 != 0:
            sum_square += int(num) ** 2
    return sum_square
def main():
    string = input('Введите числа через пробел\n')
    result = squares(string)
    print("Сумма квадратов нечетных цифр:", result)
if __name__ == '__main__':
    main()