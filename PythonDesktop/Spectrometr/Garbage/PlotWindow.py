from PyQt5.QtWidgets import QWidget , QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

 
time_plus = 'time_plus'
time_minus = 'time_minus'
value_plus = 'value_plus'
value_minus = 'value_minus'
class PlotSetting:
    '''
        **Markers**

        =============   ===============================
        character       description
        =============   ===============================
        ``'.'``         point marker
        ``','``         pixel marker
        ``'o'``         circle marker
        ``'v'``         triangle_down marker
        ``'^'``         triangle_up marker
        ``'<'``         triangle_left marker
        ``'>'``         triangle_right marker
        ``'1'``         tri_down marker
        ``'2'``         tri_up marker
        ``'3'``         tri_left marker
        ``'4'``         tri_right marker
        ``'8'``         octagon marker
        ``'s'``         square marker
        ``'p'``         pentagon marker
        ``'P'``         plus (filled) marker
        ``'*'``         star marker
        ``'h'``         hexagon1 marker
        ``'H'``         hexagon2 marker
        ``'+'``         plus marker
        ``'x'``         x marker
        ``'X'``         x (filled) marker
        ``'D'``         diamond marker
        ``'d'``         thin_diamond marker
        ``'|'``         vline marker
        ``'_'``         hline marker
        =============   ===============================

        **Line Styles**

        =============    ===============================
        character        description
        =============    ===============================
        ``'-'``          solid line style
        ``'--'``         dashed line style
        ``'-.'``         dash-dot line style
        ``':'``          dotted line style
        =============    ===============================

        Example format strings::

            'b'    # blue markers with default shape
            'or'   # red circles
            '-g'   # green solid line
            '--'   # dashed line with default color
            '^k:'  # black triangle_up markers connected by a dotted line

        **Colors**

        The supported color abbreviations are the single letter codes

        =============    ===============================
        character        color
        =============    ===============================
        ``'b'``          blue
        ``'g'``          green
        ``'r'``          red
        ``'c'``          cyan
        ``'m'``          magenta
        ``'y'``          yellow
        ``'k'``          black
        ``'w'``          white
        =============    ===============================
    '''
    def __init__(self, color='green', marker=',', linestyle='dashed'):
        self.color = color
        self.marker = marker
        self.linestyle = linestyle
    def get_plot_parag(self):
        """
        :return: Возвращает параметры графика в виде словаря.
        """

        return { # словарь с параметрами
        'color':self.color,
        'marker':self.marker,
        'linestyle':self.linestyle
    }
class PlotWindow(QWidget):
    """
    <h1>Класс <b>PlotWindow</b> предназначен для создания окна графика и оторбражения кнопок управления графиком.</h1>

    <h3>Атрибуты:</h3>
    my_id (int): Номер конктреного экземпляра класса.\n
    DataManager (): Экземпляр класса <b>DataManager</b> для обработки данных графика.\n
    PlotSetting (): Экземпляр класс <b>PlotSetting</b> для установки параметров графика
    Пример использования : PlotSetting(color='blue', marker='o', linestyle='solid'), если не указать, то применятся дефолтные настройки
    """
    def __init__(self, id):
        super().__init__()
        self.my_id = id
        self.setWindowTitle(f'График № {id}')
        self.setGeometry(300, 300, 800, 600)
        self.DataManager = DataManager()
        self.PlotSetting = PlotSetting() # PlotSetting(color='blue', marker='o', linestyle='solid')
        self.layout = QVBoxLayout(self)
        
        # Закрыть
        self.button_exit = QPushButton('Закрыть', self)
        self.button_exit.setStyleSheet('''
            QPushButton {
                background-color: red;
                color: white;
            }
            QPushButton:hover {
                background-color: darkred;  /* Цвет при наведении */
            }
            QPushButton:pressed {
                background-color: maroon;  /* Цвет при нажатии */
            }
        ''')
        self.button_exit.clicked.connect(self.close)

        self.layout.addWidget(self.button_exit)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Кнопка для увеличения графика
        self.button_open_graph = QPushButton(f'Открыть график {self.my_id}')
        self.button_open_graph.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: blue;
            }
            QPushButton:hover {
                background-color: darkgrey;  /* Цвет при наведении */
            }
            QPushButton:pressed {
                background-color: maroon;  /* Цвет при нажатии */
            }
        ''')
        self.button_open_graph.clicked.connect(self.increase_size)
        self.layout.addWidget(self.button_open_graph)

        self.button_horizont_layout = QHBoxLayout()
        # Увеличить график по значению
        self.button_value_plus = QPushButton(f'Увеличить чувствительность нижнего значения', self)
        self.button_value_plus.setStyleSheet('''
            QPushButton {
                background-color: green;
                color: white;
            }
            QPushButton:hover {
                background-color: darkgreen;  /* Цвет при наведении */
            }
            QPushButton:pressed {
                background-color: maroon;  /* Цвет при нажатии */
            }
        ''')
        self.button_value_plus.clicked.connect(lambda: self.change_plot(value_plus))
        # Уменьшить график по значению
        self.button_value_minus = QPushButton(f'Заглушка', self)
        self.button_value_minus.setStyleSheet('''
            QPushButton {
                background-color: blue;
                color: white;
            }
            QPushButton:hover {
                background-color: darkblue;  /* Цвет при наведении */
            }
            QPushButton:pressed {
                background-color: maroon;  /* Цвет при нажатии */
            }
        ''')
        self.button_value_minus.clicked.connect(self.message_None)

        self.button_horizont_layout.addWidget(self.button_value_plus)
        self.button_horizont_layout.addWidget(self.button_value_minus)

        # Увеличить график по Времени
        self.button_time_plus = QPushButton(f'Сжать значения квантов', self)
        self.button_time_plus.setStyleSheet('''
            QPushButton {
                background-color: green;
                color: white;
            }
            QPushButton:hover {
                background-color: darkgreen;  /* Цвет при наведении */
            }
            QPushButton:pressed {
                background-color: maroon;  /* Цвет при нажатии */
            }
        ''')
        self.button_time_plus.clicked.connect(lambda: self.change_plot(time_plus))

        # Уменьшить график по времени
        self.button_time_minus = QPushButton(f'Вернуть обратно значения квантов', self)
        self.button_time_minus.setStyleSheet('''
            QPushButton {
                background-color: blue;
                color: white;
            }
            QPushButton:hover {
                background-color: darkblue;  /* Цвет при наведении */
            }
            QPushButton:pressed {
                background-color: maroon;  /* Цвет при нажатии */
            }
        ''')
        self.button_time_minus.clicked.connect(lambda: self.change_plot(time_minus))

        self.button_horizont_layout.addWidget(self.button_time_plus)
        self.button_horizont_layout.addWidget(self.button_time_minus)

        self.layout.addLayout(self.button_horizont_layout)
    def message_None(self):
        """<h1>Отображает предупреждающее сообщение, если контент не найден.</h1>
        <h3>Эта функция вызывает диалоговое окно с предупреждением, информируя пользователя о том, что контент отсутствует. 
        В сообщении предлагается нажимать на другие кнопки.</h3>

        :return: None
        :raises: None
        """      
        QMessageBox.warning(self,'Not Found 404','Контент пока не подвезли и не придумали =(\n пока можете понажимать на другие кнопочки =)')
    def change_plot(self, action):
        """<h1>Изменяет график в зависимости от действия пользователя</h1>
        <h3>Эта функция обрабатывает действия пользователя (например, нажатия кнопок) и обновляет график в зависимости от выбранного действия. 
        Поддерживает увеличение и уменьшение временного диапазона и значений</h3>

        :param self: экземпляр класса, в котором определена функция.
        :param action: действие, которое пользователь хочет выполнить 
        """
        if action == time_plus:
            self.plot_update(time_plus)
        elif action == time_minus:
            self.plot_update(time_minus)
        elif action == value_plus:
            self.plot_update(value_plus)
        elif action == value_minus:
            self.plot_update(value_minus)
    def plot_update(self, action):
        """<h1>Обновляет график в зависимости от действия пользователя.</h1>
        <h3>Эта функция управляет обновлением данных в зависимости от действий пользователя. Она изменяет данные в <b>DataManager</b> 
        и вызывает соответствующие функции для обновления графика.</h3>
        
        :param self: экземпляр класса, в котором определена функция.
        :param action: действие, которое пользователь хочет выполнить <b>(например, time_minus, time_plus, value_minus, value_plus)</b>.
        """
        if self.DataManager.count_data >= 0:
            if action == time_minus and self.DataManager.count_data != 0:
                self.DataManager.remove_data()
                self.plot_print()
                
            elif action == time_plus and self.DataManager.count_data < 6: # plus time
                self.DataManager.sum_data()
                self.plot_print()
            elif action == value_minus:
                # TODO изменение по x-ксу уменьшаем
                print('Заглушка уменьшения порога')
            elif action == value_plus:
                self.plot_resize_count(self.DataManager.multiply_current_data())
                # изменения по y-ку увеличиваем, каждый раз *2, что меньше 50
        self.canvas.draw()
    def plot_resize_count(self, date):
        ''' <h1>Рисует новый график из буфера, увеличивая колличество счетов </h1>
        <h3>Эта функция очищает текущий график и рисует новый на основе переданных данных. Устанавливает метки осей и заголовок графика</h3>
        
        :param self: экземпляр класса, в котором определена функция.
        :param date: данные для построения графика.
        '''
        self.figure.clear()
        ax = self.figure.add_subplot()
        # ax.stem(range(len(self.DataManager.get_current_data())), self.DataManager.get_current_data())
        ax.plot(date, **self.PlotSetting.get_plot_parag())
        ax.set_xlabel('Значение кванта')
        ax.set_ylabel('Колличество квантов')
        ax.set_title(f'Spektr № {self.my_id}')
    def plot_print(self):
        ''' <h1>Рисует обновленный график </h1>
        <h3 style="color: blue;">Эта функция очищает текущий график и рисует его заново на основе текущих данных из <b>DataManager</b>. 
        Устанавливает метки осей и заголовок графика.</h3>
        
        :param self: экземпляр класса, в котором определена функция.
        '''
        self.figure.clear()
        ax = self.figure.add_subplot()
        # ax.stem(range(len(self.DataManager.get_current_data()), self.DataManager.get_current_data())
        ax.plot(self.DataManager.get_current_data(),**self.PlotSetting.get_plot_parag())
        ax.set_xlabel('Значение кванта')
        ax.set_ylabel('Колличество квантов')
        ax.set_title(f'Spektr № {self.my_id}')

    def plot_data(self,data):
        """<h1>Строит график на основе переданных данных.</h1>
        </h3>Эта функция очищает текущий график и строит новый на основе переданных данных. 
        Устанавливает метки осей и заголовок графика, а также обновляет данные в <b>DataManager</b>.</h3>

        :param self: экземпляр класса, в котором определена функция.
        :param data: данные для построения графика.
        """
        self.figure.clear()
        ax = self.figure.add_subplot()
        ax.plot(data, **self.PlotSetting.get_plot_parag())
        # ax.stem(range(len(data)), data)
        ax.set_xlabel('Значение кванта')
        ax.set_ylabel('Колличество квантов')
        ax.set_title(f'Spektr № {self.my_id}')
        # Обновление Canvas
        self.canvas.draw() 
        self.DataManager.init_data(data)

    def increase_size(self):
        """<h1>Увеличивает размер окна графика и отображает его.</h1>
        <h3>Эта функция создает новое окно графика с заданным размером, 
        удаляет кнопку открытия графика и отображает данные из <b>DataManager</b>.</h3>

        :param self:  экземпляр класса, в котором определена функция.
        """
        self.pl = PlotWindow(self.my_id)
        self.pl.button_open_graph.deleteLater()
        self.pl.resize(800,800)
        self.pl.plot_data(self.DataManager.all_data[0])
        self.pl.canvas.draw
        self.pl.show()

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
