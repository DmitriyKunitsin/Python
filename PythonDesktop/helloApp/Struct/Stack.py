from queue import LifoQueue
from collections import deque
#
# Стек линейная структура данных, открытая с одного конца и закрытая с другого
# Это означает, что доступ к нему возможен только с одного конца

class Stack:

    def __init__(self):
        self.stack = deque()
    def isEmpty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False
    def lenght(self):
        return len(self.stack)
    def top(self):
        return self.stack[-1]
    def push(self, x):
        self.x = x
        self.stack.append(x)
    def pop(self):
        return self.stack.pop()
def main():
    #
    # from queue import LifoQueue
    # 
    stack = []
    stack.append('a')
    print(stack)
    stack.append('b')
    stack.append('c')
    print(stack)
    print(stack.pop())
    print(stack.pop())
    print(stack.pop())
    print(stack)

    print("NEXT \n")

    stack = LifoQueue(maxsize= 5)

    print("текущий номер элемента : ",(stack.qsize))

    for i in range(0,5):
        stack.put(i)
        print("Элемент вставлен : ", str(i))

    print("\nтекущий номер элемента : ",(stack.qsize))
    print('\nFull: ', stack.full())
    print("Empty:", stack.empty())
    print('\nElements popped from the stack')
    for i in range(0,5):
        print(stack.get())
    
    print("\nEmpty: ", stack.empty())
    print("Full: ", stack.full())
    #
    # from collections import deque
    # 
    str1 = 'Test_String'
    n = len(str1)
    stack_ = Stack()
    for i in range(0,n):
        stack_.push(str1[i])
    reverse = ""
    while not stack_.isEmpty():
        reverse = reverse + stack_.pop()
    print(reverse)

if __name__ == "__main__":
    main()