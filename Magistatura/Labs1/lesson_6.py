
def search_ABC( string, symbol ):
    temp_symbol = symbol
    temp_start_index = 0
    temp_index = 0
    answer = ""
    while temp_index < len(string):
        temp_start_index = string.find(temp_symbol)
        temp_index = string.rfind(temp_symbol)
        count_symbol = temp_index - temp_start_index
        answer +=  f'{count_symbol + 1}{string[temp_index]}'
        temp_index += 1
        if temp_index + 1 > len(string):
            break
        temp_symbol = string[temp_index]

    return answer

def main():
    string = input('Введите строку состоящую из заглавных букв\n')
    if string.isupper():
      answer =  search_ABC(string, string[0])
      print(answer)
    else:
        print('Строка должна состоять из всех заглвных букв')

if __name__ == '__main__':
    main()