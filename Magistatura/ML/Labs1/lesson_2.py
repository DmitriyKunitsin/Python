def split_num(string):
    return [int(num) for num in string.split()]
def search_rand_num(numbers):
    unique_value = 0
    ignor_val = []
    for num in numbers:
        if num is not ignor_val:
            if numbers.count(num) > 1:
                unique_value += 1
                ignor_val.append(num)
    return unique_value  
def main():
    string = input('Введите числа через пробел\n')
    numbers = split_num(string)
    print('Всего ввели чисел :\t', len(numbers))
    print('Одинаковых чисел :\t', search_rand_num(numbers))
    print('Разных чисел :\t', len(numbers) - search_rand_num(numbers))
if __name__ == '__main__':
    main()