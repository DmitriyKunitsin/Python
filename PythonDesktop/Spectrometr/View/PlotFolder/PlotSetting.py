class PlotSetting:
    markers = (
        ('.', 'Точки'),
        (',', 'Пиксель'),
        ('o', 'Круг'),
        ('v', 'Треугольник вниз'),
        ('^', 'Треугольник вверх'),
        ('<', 'Треугольник влево'),
        ('>', 'Треугольник вправо'),
        ('1', 'Малый треугольник вниз'),
        ('2', 'Малый треугольник вверх'),
        ('3', 'Малый треугольник влево'),
        ('4', 'Малый треугольник вправо'),
        ('8', 'Восьмиугольник'),
        ('s', 'Квадрат'),
        ('p', 'Пятиугольник'),
        ('P', 'Плюс залитый'),
        ('*', 'Звезда'),
        ('h', 'Шестиугольник 1'),
        ('H', 'Шестиугольник 2'),
        ('+', 'Плюс'),
        ('x', 'x'),
        ('X', 'x залитый'),
        ('D', 'Ромб'),
        ('d', 'Тонкий ромб'),
        ('|', 'Вертикальная линия'),
        ('_', 'Горизонтальная линия')
    )
    lines = (('-','Сплошная линия'), ('--','Пунктирная линия'), ('-.','штрих-пунктирная линия'), (':','точечная линия'))
    colors = (('blue', 'Синий'), ('green', 'Зеленый'), ('red', 'Красный'), ('cyan', 'Бирюзовый'), ('magenta', 'Пурпурный'), ('yellow', 'Желтый'), ('black', 'Черный'), ('white', 'Белый'))
    def __init__(self, color='green', marker=',', linestyle=':'):
        self.color = color
        self.marker = marker
        self.linestyle = linestyle
    def get_plot_parag(self, color=None, marker=None, linestyle=None):
        """
            :param color: Цвет графика (по умолчанию None).
            :param marker: Маркер графика (по умолчанию None).
            :param linestyle: Стиль линии графика (по умолчанию None).
            :return: Возвращает параметры графика в виде словаря.
        """
        plot_params = {
            'color': color if color is not None else self.color,
            'marker': marker if marker is not None else self.marker,
            'linestyle': linestyle if linestyle is not None else self.linestyle
        }
        return plot_params
    @classmethod
    def get_all_markers(cls):
        '''Список всех маркров
        
        :return: Возвращает весь кортеж доступных маркеров
        '''
        return [marker for marker in cls.markers]
    @classmethod
    def get_all_line(cls):
        '''Список всех линий
        
        :return: Возвращает весь кортеж доступных линий
        '''
        return [line for line in cls.lines]
    @classmethod
    def get_all_colors(cls):
        '''Список всех цветов
        
        :return: Возвращает весь кортеж доступных цветов
        '''
        return [color for color in cls.colors]