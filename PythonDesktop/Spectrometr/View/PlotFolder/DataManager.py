class DataManager:
    """
    <h1>Класс <b>DataManager</b> предназначен для управления данными, их суммирования и умножения.</h1>

    <h3>Атрибуты:</h3>
    \nall_data (list): Список, содержащий все данные.\n
    count_data (int): Индекс текущего элемента данных.\n
    temp_data (any): Временное значение для хранения промежуточных данных.
    """
    def __init__(self):
        """
        <h1>Инициализирует новый экземпляр <b>DataManager</b>.</h1>
        
        Создает пустой список all_data, устанавливает count_data в 0 и temp_data в None.
        """
        self.all_data = []
        self.count_data = 0
        self.temp_data = None

    def sum_pairs(self,data):
        """<h1>Суммирует пары элементов в списке.</h1>
        
        :param data: Список чисел, элементы которого будут суммироваться попарно.

        :return: Список, содержащий суммы пар элементов.
        """
        temp = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):  # Проверка на наличие следующего элемента
                temp.append(data[i] + data[i + 1])
            else:
                temp.append(data[i])
        return temp
    def sum_data(self):
        """<h1>Суммирует текущие данные и добавляет результат в <b>all_data</b>.</h1>
        Этот метод вызывает <b>sum_pairs</b> для суммирования текущих данных и 
        обновляет счетчик <b>count_data</b>.
        """
        self.all_data.append(self.sum_pairs(self.all_data[self.count_data]))
        self.count_data += 1
        self.temp_data = None
    def init_data(self, data):
        """
        <h1>Инициализирует данные, добавляя их в all_data.</h1>

        :param data: Данные для инициализации, которые будут добавлены в all_data.
        """
        self.all_data.append(data)
        self.temp_data = None

    def remove_data(self):
        """<h1>Удаляет последние данные из <b>all_data</b>.</h1>

        Если count_data больше 0, удаляет последний элемент из <b>all_data</b> и 
        уменьшает счетчик <b>count_data</b> на 1
        
        """
        if self.count_data > 0:
            self.all_data.pop()
            self.count_data -= 1

    def get_current_data(self):
        """
        <h1>Получает текущие данные.</h1>

        :return: Текущие данные из <b>all_data</b> или <b>None</b>, если данных нет.
        """
        return self.all_data[self.count_data] if self.count_data < len(self.all_data) else None

    def multiply_current_data(self):
        """
        <h1>Умножает текущие данные на 2.</h1>
        
        Если <b>temp_data</b> равно <b>None</b>, умножает текущие данные. В противном случае 
        умножает временные данные на 2.
        
        :return: Результат умножения текущих или временных данных.
        """
        if self.temp_data is None:
            self.temp_data = self.multiply_pairs(self.get_current_data())
        else:
            self.temp_data = self.multiply_pairs(self.temp_data)
        return self.temp_data

    def multiply_pairs(self, data):
        """
        <h1>Умножает элементы списка на 2, если они меньше 50.</h1>

        :param data: Список чисел для умножения.
        :return: Список, содержащий элементы, умноженные на 2.
        """
        return [x * 2 for x in data if x < 50]  

    def get_all_data_length(self):
        """
        <h1>Получает длину списка <b>all_data</b>.</h1>

        :return: Количество элементов в <b>all_data</b>.
        """
        return len(self.all_data)
