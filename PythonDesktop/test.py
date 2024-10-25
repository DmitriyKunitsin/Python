import pandas as pd
import numpy as np

def main():
    df = pd.DataFrame(

    {

        "col1": ["a", "a", "b", "b", "a"],

        "col2": [1.0, 2.0, 3.0, np.nan, 5.0],

        "col3": [1.0, 2.0, 3.0, 4.0, 5.0]

    },

    columns=["col1", "col2", "col3"],

)
    print(df)
    df2 = df.copy()
    df2.loc[0, 'col1'] = 'c'
    df2.loc[2, 'col3'] = 4.0
    print('->\n',df2)
    
    print('->\n',df.compare(df2))
    
    

if __name__ == '__main__':
    main()