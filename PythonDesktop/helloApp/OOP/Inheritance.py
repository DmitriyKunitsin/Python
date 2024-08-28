class Person:
    def __init__(self, first, last, age):
        self.firstname = first
        self.lastname = last
        self.age = age

    def __str__(self):
        return self.firstname + " " + self.lastname + ", " + str(self.age)
class Empolye(Person):
    def __init__(self, first, last, age, empno):
        self.firstname = first
        self.lastname = last
        self.age = age
        self.empno = empno
    def __str__(self):
        return (self.firstname + " "
                + self.lastname + ", "
                + str(self.age) + ", "
                + str(self.empno))
    
class Studies(Empolye):
    def __init__(self, first, last, age, empno, group):
        super().__init__(first, last, age, empno)
        self.group = group

    def __str__(self):## Метод super специальный метод который возвращает объект как экземпляр базового класса
        return (super().__str__() + ", "
                + str(self.group))
    
def main():
    print(issubclass(Empolye, Person))
    print(issubclass(Person, object))
    print(issubclass(Empolye, object))
    x = Person("Dima", 'Kunitsin', 28)
    print(x)
    y = Empolye("Vovan", 'Dubin', 5, 0x007)
    print(y)
    z = Studies("Strudent", 'Studentivich', 16, 777, "ZIP-19")
    print(z)
## issubclass возвращает true, если класс упомянутый в первом аргумента является подклассом класс упомянутого во втором аргументе

if __name__ == "__main__":
    main()
