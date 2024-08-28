name_file = 'test.txt'

try:
    file1 = open(name_file, mode='a', encoding='utf-8')
    file1.write('That fought with us upon Saint Crispin\'s day.')
except Exception as e:
    print(e)
finally:
    file1.close()