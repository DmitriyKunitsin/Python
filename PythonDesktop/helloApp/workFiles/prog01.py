
name_file = 'test.txt'

try:
    file1 = open(name_file, mode='w', encoding='utf-8')
    file1.write("Привет мир!")
except Exception as e:
    print(e)