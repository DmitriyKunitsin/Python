def split_num(string):
    numbers = []
    for num in string.split():
        if num == 'stop':
            break
        numbers.append(int(num))
    return numbers
def sum(numbers):
    sum = 0
    for num in numbers:
        sum += num
    return sum
def main():
    string = input('Введите числа через пробел\n')
    string = split_num(string)
    print(string)
    print(f'Сумма чисел = {sum(string)}')
if __name__ == '__main__':
    main()