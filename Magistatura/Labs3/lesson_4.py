import pandas as pd

def main():
    s_1 = pd.Series(data=range(1,6),index=['a', 'b', 'c', 'd', 'e'])
    s_1['f'] = 6
    print(s_1)
if __name__ == '__main__':
    main()