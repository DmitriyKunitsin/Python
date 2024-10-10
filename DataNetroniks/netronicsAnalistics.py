import pandas as pd
import lasio
import seaborn as sb
from matplotlib import pyplot as plt

def main():
    las =lasio.read('dayThree.las')
    df = las.df()
    print(df.head())
    print(df.dtypes)
    
    # df['TIME'] = pd.to_datetime(df['TIME'], unit='s')
    # df.set_index('TIME', inplace=True)
    print(df.index)
    step = 10
    df['group'] = (df.index // step).astype(int)

    mean_values = df.groupby('group').mean()

    print(mean_values.head())

    # sb.scatterplot(x='TIME', y='NTNC', data=df) 
    # plt.show()
if __name__ == '__main__':
    main()