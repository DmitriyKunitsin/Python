import pandas as pd

def main():
    df = pd.DataFrame(data= [[1, 2], [5, 3], [3.7, 4.8]], columns=['col1', 'col2'])
    print(df)

if __name__ == '__main__':
    main()