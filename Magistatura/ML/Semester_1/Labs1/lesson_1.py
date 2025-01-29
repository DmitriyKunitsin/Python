def swap_word(string):
    words = string.split()
    if len(words) < 2:
        return -1
    else:
        words[0], words[1] = words[1] , words[0]
    return " ".join(words)
def main():
    string = input('Введите строку из двух слов\n')
    string = swap_word(string)
    if(string == -1):
        print('строка имеет не верный формат, введите больше 2 слов с пробелом')
    else:
        print(string)
if __name__ == '__main__':
    main()