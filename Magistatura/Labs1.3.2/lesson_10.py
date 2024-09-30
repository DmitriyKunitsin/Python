import pandas as pd

def add_new_col( df ):
    df['col3'] = df['col1'] * df['col2']
    print(df)

def main():
    df = pd.DataFrame(data= [[1, 2], [5, 3], [3.7, 4.8]], columns=['col1', 'col2'])
    print(df)
    add_new_col(df)

if __name__ == '__main__':
    main()