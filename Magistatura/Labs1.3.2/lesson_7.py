import pandas as pd

def main():
    df = pd.DataFrame(data= [[1, 2], [5, 3], [3.7, 4.8]], columns=['col1', 'col2'])
    print(df['col1'][2])

if __name__ == '__main__':
    main()