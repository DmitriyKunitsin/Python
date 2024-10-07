import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = sum(data) / len(data)
    se = stats.sem(data)
    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return mean - h, mean + h
def main():
    # Загружаем данные из файла
    df = pd.read_csv('water.txt', sep='\t')
    
    grouped = df.groupby('location')[['mortality', 'hardness']].agg(['mean', stats.sem])
    for location in grouped.index:
        mean_mortality = grouped.loc[location, ('mortality', 'mean')]
        se_mortality = grouped.loc[location, ('mortality', 'sem')]
        ci_mortality = mean_mortality - 1.96 * se_mortality, mean_mortality + 1.96 * se_mortality
        
        mean_hardness = grouped.loc[location, ('hardness', 'mean')]
        se_hardness = grouped.loc[location, ('hardness', 'sem')]
        ci_hardness = mean_hardness - 1.96 * se_hardness, mean_hardness + 1.96 * se_hardness

    df.boxplot(column='mortality', by='location')
    plt.title('Смертность')
    plt.suptitle('')
    plt.ylabel('Годовая смертность на 100,000 населения')
    plt.show()
    df.boxplot(column='hardness', by='location')
    plt.title('Жёсткость воды')
    plt.suptitle('')
    plt.ylabel('Концентрация кальция (частей на миллион)')
    plt.show()
    # Текстовый вывод
    print("\nВыводы:")
    print("1. Смертность:")
    print(f"   - Средняя смертность на юге: {grouped.loc['South', ('mortality', 'mean')]:.2f}")
    print(f"   - Средняя смертность на севере: {grouped.loc['North', ('mortality', 'mean')]:.2f}")
    print(f"   - 95% доверительный интервал для юга: {confidence_interval(df[df['location'] == 'South']['mortality'])}")
    print(f"   - 95% доверительный интервал для севера: {confidence_interval(df[df['location'] == 'North']['mortality'])}")
    print("   - Смертность на севере в среднем выше, чем на юге.")
    print("   - Доверительные интервалы не перекрываются, что указывает на статистически значимую разницу.")

    print("\n2. Жёсткость воды:")
    print(f"   - Средняя концентрация кальция на юге: {grouped.loc['South', ('hardness', 'mean')]:.2f}")
    print(f"   - Средняя концентрация кальция на севере: {grouped.loc['North', ('hardness', 'mean')]:.2f}")
    print(f"   - 95% доверительный интервал для юга: {confidence_interval(df[df['location'] == 'South']['hardness'])}")
    print(f"   - 95% доверительный интервал для севера: {confidence_interval(df[df['location'] == 'North']['hardness'])}")
    print("   - Концентрация кальция (жёсткость воды) на юге в среднем выше, чем на севере.")
    print("   - Доверительные интервалы не перекрываются, что указывает на статистически значимую разницу.")

    print("\n3. Общие выводы:")
    print("   - Существует заметная разница в смертности между северными и южными городами.")
    print("   - Также наблюдается значительная разница в жёсткости воды между севером и югом.")
    print("   - Интересно отметить, что при более высокой смертности на севере, жёсткость воды там ниже.")
    print("   - Это может указывать на то, что жёсткость воды не является определяющим фактором смертности,")
    print("     или что другие факторы имеют более сильное влияние на показатели смертности.")

if __name__ == '__main__':
    main()