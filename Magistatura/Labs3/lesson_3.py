import pandas as pd

def main():
    s_1 = pd.Series(data=range(1,6),index=['a', 'b', 'c', 'd', 'e'])
    # доступ по позиционному индексу, который указывает на третий элемент (индекс 2).
    print(s_1.iloc[1])
if __name__ == '__main__':
    main()