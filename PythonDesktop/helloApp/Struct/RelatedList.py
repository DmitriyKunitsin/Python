#
# Односвязный список
# #
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkendList:
    def __init__(self):
        self.head = None
    def printList(self):
        try:
            temp = self.head
            while(temp):
                print(temp.data)
                temp = temp.next
        except Exception as err:
            print("Error {0}".format(err))
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node
    def appened(self, new_data):
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while(last.next):
            last = last.next

        last.next = new_node

    def deleteNode(self, key):
        temp = self.head
        if (temp is not None):
            if(temp.data == key):
                self.head = temp.next
                temp = None
                return
        while(temp is not None):
            if temp.data == key:
                break
            prev = temp
            temp = temp.next
        if(temp == None):
            return
        prev.next = temp.next
        temp = None
    def deleteList(self):
        current = self.head
        while current:
            prev = current.next
            del current.data
            current = prev
    def findLenght(self):
        temp = self.head
        count = 0
        while(temp):
            count += 1
            temp = temp.next
        return count
    def fintLengthRec(self, node):
        if (not node):
            return 0
        else :
            return 1 + self.fintLengthRec(node.next)
    def search(self, x):
        current = self.head
        while current != None:
            if (current.data == x):
                return True
            current = current.next
        return False
def main():
    llist = LinkendList()
    llist.head = Node(1)
    second = Node(2)
    third = Node(3)
    llist.head.next = second
    second.next = third
    llist.push(0)
    llist.appened(4)
    llist.deleteNode(2)
    llist.printList()
    print("len list : ", llist.findLenght())
    print("len rec list : ", llist.fintLengthRec(llist.head))
    print(llist.search(2))
    print(llist.search(0))
    llist.deleteList()
    llist.printList()

if __name__ == '__main__':
    main()