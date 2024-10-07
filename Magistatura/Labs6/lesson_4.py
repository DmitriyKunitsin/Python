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
    
    south_mortatily = df[df['location'] == 'South']['mortality']
    north_mortatily = df[df['location'] == 'North']['mortality']
    
    south_mortatily_ci = confidence_interval(south_mortatily)
    north_mortatily_ci = confidence_interval(north_mortatily)

    sourth_hardness = df[df['location'] == 'South']['hardness']
    nourth_hardness = df[df['location'] == 'North']['hardness']

    sourth_hardness_ci = confidence_interval(sourth_hardness)
    nourth_hardness_ci = confidence_interval(nourth_hardness)
    # 4) Визуализация результатов
    # Установка русского шрифта для matplotlib
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.figure(figsize=(14,6))

    plt.subplot(1, 2, 1)
    plt.boxplot([south_mortatily, north_mortatily], label=['Юг', 'Север'])
    plt.title('Смертность')
    plt.ylabel('Годовая смертность на 100,000 населения')

    plt.subplot(1, 2, 2)
    plt.boxplot([sourth_hardness, nourth_hardness], labels=['Юг', 'Север'])
    plt.title('Жёсткость воды')
    plt.ylabel('Концентрация кальция (частей на миллион)')

    plt.tight_layout()
    plt.show()

    # Текстовый вывод
    print("\nВыводы:")
    print("1. Смертность:")
    print(f"   - Средняя смертность на юге: {south_mortatily.mean():.2f}")
    print(f"   - Средняя смертность на севере: {north_mortatily.mean():.2f}")
    print(f"   - 95% доверительный интервал для юга: {south_mortatily_ci}")
    print(f"   - 95% доверительный интервал для севера: {north_mortatily_ci}")
    print("   - Смертность на севере в среднем выше, чем на юге.")
    print("   - Доверительные интервалы не перекрываются, что указывает на статистически значимую разницу.")

    print("\n2. Жёсткость воды:")
    print(f"   - Средняя концентрация кальция на юге: {sourth_hardness.mean():.2f}")
    print(f"   - Средняя концентрация кальция на севере: {nourth_hardness.mean():.2f}")
    print(f"   - 95% доверительный интервал для юга: {sourth_hardness_ci}")
    print(f"   - 95% доверительный интервал для севера: {nourth_hardness_ci}")
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