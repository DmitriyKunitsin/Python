def check_palindrome(word):
    len_word = len(word)
    for i in  range(len_word // 2):
        if(word[i] != word[len_word - 1 - i]):
            return False
        len_word -= 1  
    return True  
def main():
    word = input('Введите слово \n')
    if check_palindrome(word):
        print('Палиндром')
    else:
        print('Не палиндром')
if __name__ == '__main__':
    main()