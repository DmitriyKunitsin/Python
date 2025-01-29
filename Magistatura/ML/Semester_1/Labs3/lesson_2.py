import pandas as pd

def main():
    s_1 = pd.Series(data=range(1,6),index=['a', 'b', 'c', 'd', 'e'])
    #  доступ по строковому индексу.
    print(s_1.get('d'))
if __name__ == '__main__':
    main()