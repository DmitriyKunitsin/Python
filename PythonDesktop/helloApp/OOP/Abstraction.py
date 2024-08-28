# Абстрактный класс и метод
# Класс с объектом, который не создан, называется абстрактным классом
# Кроме того, метод, объявленый без реализации, называетися абстрактным методом
# Абстрактный класс может иметь или не иметь абстрактный метод
#

from abc import ABC, abstractclassmethod
## Чтобы сделать абстрактный класс явным, нам нужно получить его от встроеннго класса ABC
class Animal(ABC):
    @abstractclassmethod
    def move(self):
        pass
## Если надо явно абстрогировать метод класса, нуэно использовать метод Decorator@abstract с методом, который нужно сделать абстрактным
class Human(Animal):
    def move(self):
        print('I Walk.')
class Snake(Animal):
    def move(self):
        print('I Crawl.')

class AccesMod():
    def __init__(self):
        self.a = 'Public'
        self._b = "Internal use"
        self.__c = 'Искажении имени, так не стоит'

def main():
    a = Human()
    b = Snake()
    a.move()
    b.move()
    x = AccesMod()
    print(x.a)
    print(x._b)
    print(x._AccesMod__c)
if __name__ == "__main__":
    main()