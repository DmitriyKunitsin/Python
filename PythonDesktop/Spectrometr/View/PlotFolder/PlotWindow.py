from PyQt5.QtWidgets import QWidget , QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from View.PlotFolder.PlotSetting import PlotSetting
from View.PlotFolder.DataManager import DataManager

time_plus = 'time_plus'
time_minus = 'time_minus'
value_plus = 'value_plus'
value_minus = 'value_minus'

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
        self.plot_color = None
        self.plot_line = None
        self.plot_marker = None
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
        #### НАСТРОЙКИ ГРАФИКА
        self.setting_plot_widget = QWidget()
        self.setting_plot_layout = QHBoxLayout(self.setting_plot_widget)
        ## Цвета
        self.combo_colors_selector = QComboBox()
        self.add_all_colors()
        self.combo_colors_selector.currentTextChanged.connect(self.selected_color)
        ## Линии
        self.combo_lines_selector = QComboBox()
        self.add_all_lines()
        ## Маркеры
        self.combo_markers_selector = QComboBox()
        self.add_all_markers()

        self.setting_plot_layout.addWidget(self.combo_colors_selector)
        self.setting_plot_layout.addWidget(self.combo_lines_selector)
        self.setting_plot_layout.addWidget(self.combo_markers_selector)

        self.layout.addWidget(self.setting_plot_widget)


        ####
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
    #############################################################
    # 1. написать доку
    # 2. дописать выбор
    def add_all_colors(self):
        colors = PlotSetting.get_all_colors()
        default_text = 'Выберите...'
        self.combo_colors_selector.addItem(default_text)
        self.combo_colors_selector.addItems(color for color in colors)
    def add_all_lines(self):
        lines = PlotSetting.get_all_line()
        default_text = 'Выберите...'
        self.combo_lines_selector.addItem(default_text)
        self.combo_lines_selector.addItems(line for line in lines)
    def add_all_markers(self):
        merkers = PlotSetting.get_all_markers()
        default_text = 'Выберите...'
        self.combo_markers_selector.addItem(default_text)
        self.combo_markers_selector.addItems(distrip for marker, distrip in merkers)
    def selected_color(self):
        index = self.combo_colors_selector.currentIndex()
        if index is not 0:
            color = self.combo_colors_selector.itemText(index)
            print(f'Выбранный цвет {color}')
            self.plot_color = color
    #################################################################
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