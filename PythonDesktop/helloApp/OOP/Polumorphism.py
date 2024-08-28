#
# Перегрузка метода
# 
class A:

    def method01(self, i = None):
        if i is None:
            print("Sequence 01")
        else:
            print("Sequence 02")

#
# Перегрузка оператора
# 
    '''
    Специальные функции, необходимые для реализации двоичных операций
    Operator    Special Function
    +           object.add(self, other)
    -           bject.sub(self, other)
    *           object.mul(self, other)
    //          object.floordiv(self, other)
    /           object.truediv(self, other)
    %           object.mod(self, other)
    **          object.pow(self, other[, modulo])
    <<          object.lshift(self, other)
    >>          object.rshift(self, other)
    &           object.and(self, other)
    ˆ           object.xor(self, other)
    |           object.or(self, other)
    +               object.pos(self)
    -               object.neg(self)
    abs()           object.abs(self)
    ~               object.invert(self)
    complex()       object.complex(self)
    int()           object.int(self)
    long()          object.long(self)
    float()         object.float(self)
    oct()           object.oct(self)
    hex()           object.hex(self)
    <           object.lt(self, other)
    <=          object.le(self, other)
    ==          object.eq(self, other)
    !=          object.ne(self, other)
    >=          object.ge(self, other)
    >           object.gt(self, other)
    '''
class Point:
    def __init__(self, x, y, z):
        self.assing(x,y,z)
        
    def assing(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def printPoint(self):
        print(self.x,self.y, self.z)


    def __add__(self, other):
        '''
            Когда мы выполняем в коде операцию p1 + p2, 
            Python вызывает p1.__add__(p2), который в свою очередь вызывает
            Point.__add__(p1,p2). Точно так же можно переоределить другие операторы

        '''
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x,y,z)
    def __mul__(self, other):
        '''
            Точно так же, как ( + )
            переопределеное умножение
        '''
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        return Point(x,y,z)
    def __str__(self):
        return ("({0}, {1}, {2})".format(self.x,self.y,self.z))
def main():
    obj1 = A()
    obj1.method01()
    obj1.method01(5)
    p1 = Point(1,2,3)
    p2 = Point(4,5,6)
    print(p1 + p2)
    print(p1 * p2)

if __name__ == '__main__':
    main()