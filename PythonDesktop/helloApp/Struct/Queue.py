
class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = self.rear = None
    def isEmpty(self):
        return self.front == None
    def EnQueue(self, item):
        temp = Node(item)
        if self.rear == None:
            self.front = self.rear = temp
            return
        self.rear.next = temp
        self.rear = temp

    def DeQueue(self):
        if self.isEmpty():
            return
        temp = self.front
        self.front = temp.next

        if(self.front == None):
            self.rear = None


def main():
    q = Queue()
    q.EnQueue(1)
    q.EnQueue(2)
    q.DeQueue()
    q.DeQueue()
    q.EnQueue(3)
    q.EnQueue(4)
    q.EnQueue(5)
    q.DeQueue()
    print("\nThe front of the Queue : " + str(q.front.data))
    print("\nThe rear of the Queue : " + str(q.rear.data))

if __name__ == '__main__':
    main()