#
# Циклическая очередь или кольцевой буфер
# #
class CircularQueue():
    def __init__(self, size):
        self.size = size
        self.queue = [None for i in range(size)]
        self.front = self.rear = -1

    def enqueue(self, data):

        if((self.rear + 1) % self.size == self.front):
            print('Кольцовой буфер(очередь) полон')
        elif (self.front == -1):
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = data
        else:
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = data

    def dequeue(self):
        if(self.front == -1):
            print('Кольцовой буфер(очередь) пуст')
        elif(self.front == self.rear):
            temp = self.queue[self.front]
            self.front = -1
            self.rear = -1
            return temp
        else:
            temp = self.queue[self.front]
            self.front = (self.front + 1) % self.size
            return temp
        
    def show(self):
        if(self.front == -1):
            print('Кольцовой буфер(очередь) пуст')
        elif (self.rear >= self.front):
            print('Элементы кольцевого буфера являются')
            for i in range(self.front, self.rear + 1):
                print(self.queue[i])
            print()
        else:
            print('Элементы кольцевого буфера являются')
            for i in range(self.front, self.size):
                print(self.queue[i])
        for i in range(0, self.rear + 1):
            print(self.queue[i])
        if ((self.rear + 1) % self.size == self.front):
            print('Кольцовой буфер(очередь) полон')

def main():
    cq = CircularQueue(5)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    cq.enqueue(4)
    cq.show()
    print ("Dequed value = ", cq.dequeue())
    cq.show()
    cq.enqueue(5)
    cq.enqueue(6)
    cq.enqueue(7)
    print ("Dequed value = ", cq.dequeue())
    cq.show()
    
if __name__ == '__main__':
    main()