# На основе информации о сотрудниках (файл с данными прикреплен к заданию) 
# выполните кластеризацию и охарактеризуйте полученные группы сотрудников. 
# Цель - определить причины текучести кадров. Удачи! 
import pandas as pd

def main():
    # Загружаю данные
    data = pd.read_csv('HR.csv')

    # Подготавлювиваю данные

    print(data.isnull().sum())

    data.drop_duplicates(inplace=True)

    print(f'Всего осталось записей {len(data)}')

    data = pd.get_dummies(data, columns=['department','salary'], drop_first=True)

    # Нормализую данные 
    from sklearn.preprocessing import StandardScaler
    features = ['satisfaction_level', 'last_evaluation', 'number_project',
                'average_montly_hours', 'time_spend_company', 'Work_accident',
                'left', 'promotion_last_5years'] + list(data.columns[data.columns.str.startswith('department_')]) + list(data.columns[data.columns.str.startswith('salary_')])
    
    X = data[features]
    scaler = StandardScaler()
    X_scaler = scaler.fit_transform(X)

    # Класетиризую
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    result_means = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, n_init='auto', random_state=42)
        kmeans.fit(X_scaler)
        result_means.append(kmeans.inertia_)
    plt.plot(range(1, 11), result_means)
    plt.xlabel('Количество кластеров')
    plt.ylabel('Inertia')
    plt.title('Опрделение оптимального колличества кластеров')
    plt.show()

    optimal_clusters = 3 
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(X)


    cluster_summary = data.groupby('cluster').mean()
    print(cluster_summary)

    cluster_counts = data['cluster'].value_counts()
    print(cluster_counts)

    # Кластер 0 :
    # Уровень удовлетворенности : 0.604
    # Последняя оценка : 0.665
    # Колличество проектов 3.4
    # Среднее колличество часов в месяц 147.24
    # Процент сотрудников в этом класетре : 4361 ( наибольшее )#

    # К данному кластеру относится наибольшее колличество сотрудников, у них наименьший уровень удовлетворенности и последняя оценка.
    # Сотрудники выполняются умеренное колличество проектов и работают меньше часов по сравнению с коллегами.
    # Возможно сотрудники относящиеся к данному кластеру не совсем довольны своей нагрузкой и перспективами в компании

    # Кластер 1 :
    # Уровень удовлетворенности : 0.675
    # Последняя оценка : 0.727
    # Колличество проектов 3.8
    # Среднее колличество часов в месяц 202.96
    # Процент сотрудников в этом класетре : 3704 ( наименьшее )#

    #   Данный кластер самый удовлетворенный и имеет среднию оценку, выполняют среднее колличество проектов и работают часов
    #   К данному кластеру относится наименьшее колличество сотрудников
    #   В связи с высокой последней оценкой сотрудников, их работа удовлетворяет руководство, так же высокий уровень личной удовлетворенности
    #   Говорит о том, что сотрудники относятся к своим проектам внимательно и работают на совесть. 

    # Кластер 2 :
    # Уровень удовлетворенности : 0.614
    # Последняя оценка : 0.764
    # Колличество проектов 4.2
    # Среднее колличество часов в месяц 257.26
    # Процент сотрудников в этом класетре : 3926 ( среднее )

    # К данному кластеру относится среднее колличество сотрудников, у них средняя удовлетворенность, но близится к низкой, 
    # но высокая последняя оценка, данные специалисты ведут наибольшее колличество проект и проводят на работе больше всех часов
    # Может говорить, что специалистов ценят, если дают столько проектов, но удовлетворенность данного кластера говорит о том, 
    # что сотрудники находятся в стрессе от переработок , возможно профессиональное выгорание 
     
    # Возможные причины текучки
    # 1. 0 кластеру добавить интересных задач или проектов, чтобы персонал был более нагруженный, так же появилась удовлетворенность
    # от выполняемых задач, чтобы избежать самостоятельного обесценивания сотрудников
    # 2. 2 кластер разгрузить по проектам, дабы избежать выгорания и переработок сотрудников      
if __name__ == "__main__":
    main()