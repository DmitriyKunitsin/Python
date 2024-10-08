import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
import numpy as np

def sinplot(flip = 1):
    x = np.linspace(0, 14,100)
    for i in range(1,5):
        plt.plot(x, np.sin(x + i *.5)* (7 - i) * flip)

def main():
    data = sb.load_dataset('iris')
    print(data.head())
    sb.set_style('darkgrid', {'axes.axisbelow' : False})
    sinplot()
    sb.despine(top=True, right=True)
    plt.show()
    print(sb.axes_style())

    current_palette = sb.color_palette()
    sb.palplot(current_palette)
    plt.show()

    current_palette = sb.color_palette()
    sb.palplot(sb.color_palette('Greens'))
    plt.show()

    current_palette = sb.color_palette()
    sb.palplot(sb.color_palette('Blues'))
    plt.show()

    current_palette = sb.color_palette()
    sb.palplot(sb.color_palette("BrBG", 7))
    plt.show()

    sb.set_palette('husl')
    plt.show()

    tips = sb.load_dataset('tips')
    ax = sb.scatterplot(x= 'total_bill', y='tip', data=tips)
    plt.show()
    
    df = sb.load_dataset('iris')
    df.head()
    sb.displot(df['petal_length'], kde = False)
    plt.show()

    sb.jointplot(x = 'petal_length', y= 'petal_width', data= df)
    plt.show()

    sb.set_style('ticks')
    sb.pairplot(df, hue='species', diag_kind='kde', kind= 'scatter', palette='husl')
    plt.show()

if __name__ == '__main__':
    main()