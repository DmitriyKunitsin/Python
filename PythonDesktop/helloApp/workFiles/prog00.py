


name_file = 'test.txt'


try:
    file1 = open(name_file, mode='rt', encoding='utf-8')
    for each in file1:
            print(each)
    print(file1.read(10))
except Exception as e:
    print(e)
finally:
    file1.close()