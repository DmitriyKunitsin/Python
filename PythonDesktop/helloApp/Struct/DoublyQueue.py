import collections
#
# Двухстроння очередь
# В данную очередь можно вставлять и удалять данные с обоих концов
# #

def main():
    deq = collections.deque([10,20,30])
    print(deq)
    ''' Добавление элемента с правого конца'''
    deq.append(40)
    print(deq)
    ''' Добавление элемента с левого конца'''
    deq.appendleft(0)
    print(deq)
    ''' Удаление элемента с правого конца'''
    deq.pop()
    print(deq)
    ''' Удаление элемента с левого конца'''
    deq.popleft()
    print(deq)
    

if __name__ == '__main__':
    main()