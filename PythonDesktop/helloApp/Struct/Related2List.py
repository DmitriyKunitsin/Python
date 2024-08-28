class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkendList:
    def __init__(self):
        self.head = None
    def push(self , new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node
    def appened(self, new_data):
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last
        return
    def printList(seelf, node):
        print("Движение в прямом направлении")
        while node:
            print(node.data)
            last = node
            node = node.next
        print("Движение в обратном направлении")
        while last:
            print(last.data)
            last = last.prev

def main():
    llist = DoublyLinkendList()
    llist.push(1)
    llist.appened(2)
    llist.appened(3)
    llist.printList(llist.head)

if __name__ == "__main__":
    main()