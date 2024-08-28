class Class01:

    def __init__(self):
        print('Создался только объекта класса 01..')

class Class02:

    def __init__(self):
        print('Создался только объект класса 02...')

def main():
    o1 = Class01()
    o2 = Class02()


if __name__ == "__main__":
    print("Основной модуль запущен")
    main()
else:
    print("Модуль 2 был запущен из основного")