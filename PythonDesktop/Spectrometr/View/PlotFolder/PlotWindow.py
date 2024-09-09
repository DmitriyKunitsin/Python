from PyQt5.QtWidgets import QWidget , QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QComboBox, QAction, QMenuBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from View.PlotFolder.PlotSetting import PlotSetting
from View.PlotFolder.DataManager import DataManager
from View.PlotFolder.PlotFile import PlotFile

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
        self.combo_lines_selector.currentTextChanged.connect(self.selected_line)
        ## Маркеры
        self.combo_markers_selector = QComboBox()
        self.add_all_markers()
        self.combo_markers_selector.currentTextChanged.connect(self.selected_marker)

        self.setting_plot_layout.addWidget(self.combo_colors_selector)
        self.setting_plot_layout.addWidget(self.combo_lines_selector)
        self.setting_plot_layout.addWidget(self.combo_markers_selector)

        self.layout.addWidget(self.setting_plot_widget)

        # self.button_update_plot = QPushButton('Обновить настройки графика')
        # self.button_update_plot.setStyleSheet('''
        #     QPushButton {
        #         background-color: white;
        #         color: blue;
        #     }
        #     QPushButton:hover {
        #         background-color: darkgrey;  /* Цвет при наведении */
        #     }
        #     QPushButton:pressed {
        #         background-color: maroon;  /* Цвет при нажатии */
        #     }
        # ''')
        # self.button_update_plot.clicked.connect(self.update_setting_plot)
        # self.layout.addWidget(self.button_update_plot)
        self.layout.addWidget(self.button_exit)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        #########################################
        # МЕНЮ ГРАФИКА
        menubar = QMenuBar()
        file_menu = menubar.addMenu('График')

        save_action = QAction('Сохранить изображение графика', self)
        save_action.triggered.connect(lambda: PlotFile.save_plot(self.figure))
        file_menu.addAction(save_action)

        self.layout.addWidget(menubar)
        #########################################
        
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
    def add_all_colors(self):
        """Добавляет все доступные <b>цвета</b> в выпадающий список.

        Этот метод получает все доступные цвета из настройки графика и добавляет их в 
        выпадающий список выбора цветов. Также добавляется текст по умолчанию.

        :return: None
        """
        colors = PlotSetting.get_all_colors()
        default_text = 'Выберите цвет...'
        self.combo_colors_selector.addItem(default_text)
        self.combo_colors_selector.addItems(distrip for color, distrip in colors)
    def add_all_lines(self):
        """Добавляет все доступные <b>линии</b> в выпадающий список.

        Этот метод получает все доступные линии из настройки графика и добавляет их в 
        выпадающий список выбора линий. Также добавляется текст по умолчанию.

        :return: None
        """
        lines = PlotSetting.get_all_line()
        default_text = 'Выберите линию...'
        self.combo_lines_selector.addItem(default_text)
        self.combo_lines_selector.addItems(distrip for line, distrip in lines)
    def add_all_markers(self):
        """Добавляет все доступные <b>маркеры</b> в выпадающий список.

        Этот метод получает все доступные маркеры из настройки графика и добавляет их в 
        выпадающий список выбора маркеров. Также добавляется текст по умолчанию.

        :return: None
        """
        merkers = PlotSetting.get_all_markers()
        default_text = 'Выберите маркер...'
        self.combo_markers_selector.addItem(default_text)
        self.combo_markers_selector.addItems(distrip for marker, distrip in merkers)
    def selected_color(self):
        """Передает выбранный <b>цвет</b> переменной класса и обновляет график.

        Этот метод проверяет выбранный цвет в выпадающем списке и обновляет 
        соответствующую переменную класса. Если выбранный индекс не равен 0,
        вызывается метод для обновления графика.

        :return: None
        :raises ValueError: Если выбранный цвет недоступен.
        """
        index = self.combo_colors_selector.currentIndex()
        if index != 0:
            distrip = self.combo_colors_selector.itemText(index)
            colors = PlotSetting.get_all_colors()
            for color, dis in colors:
                if distrip in dis:
                    self.plot_color = color
                    self.plot_print()
    def selected_marker(self):
        """Передает выбранный <b>маркер</b> переменной класса и обновляет график.

        Этот метод проверяет выбранный маркер в выпадающем списке и обновляет 
        соответствующую переменную класса. Если выбранный индекс не равен 0,
        вызывается метод для обновления графика.

        :return: None
        :raises ValueError: Если выбранный маркер недоступен.
        """
        index = self.combo_markers_selector.currentIndex()
        if index != 0:
            distrip = self.combo_markers_selector.itemText(index)
            markers = PlotSetting.get_all_markers()
            for marker, dis in markers:
                if distrip in dis:
                    self.plot_marker = marker
                    self.plot_print()
    def selected_line(self):
        """Передает выбранную <b>линию</b> переменной класса и обновляет график.

        Этот метод проверяет выбранную линию в выпадающем списке и обновляет 
        соответствующую переменную класса. Если выбранный индекс не равен 0,
        вызывается метод для обновления графика.

        :return: None
        :raises ValueError: Если выбранная линия недоступна.
        """
        index = self.combo_lines_selector.currentIndex()
        if index != 0:
            distrip = self.combo_lines_selector.itemText(index)
            lines = PlotSetting.get_all_line()
            for line, dis in lines:
                if distrip in dis:
                    self.plot_line = line
                    self.plot_print()
    def update_setting_plot(self):
        """Обновляет настройки графика на основе выбранных параметров.

        Этот метод проверяет, выбраны ли все необходимые параметры (цвет, линия, маркер).
        Если все параметры выбраны, обновляется график. В противном случае выводится предупреждение.

        :return: None
        :raises ValueError: Если какие-либо параметры не выбраны.
        """
        if self.plot_color and self.plot_line and self.plot_color is not None:
            self.plot_print()
        else:
            QMessageBox.warning(self, 'Не корректные настройки', 'Выберите пожалуйста все настройки графика')
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
        ax.plot(date, **self.PlotSetting.get_plot_parag(self.plot_color, self.plot_marker, self.plot_line))
        ax.set_xlabel('Значение кванта')
        ax.set_ylabel('Колличество квантов')
        ax.set_title(f'Spektr № {self.my_id}')
        # ax.set_yscale('log')
    def plot_print(self):
        ''' <h1>Рисует обновленный график </h1>
        <h3 style="color: blue;">Эта функция очищает текущий график и рисует его заново на основе текущих данных из <b>DataManager</b>. 
        Устанавливает метки осей и заголовок графика.</h3>
        
        <strong>Внимание!</strong> Используйте эту функцию только тогда, когда необходимо обновить график с текущими значениями.

        :param self: экземпляр класса, в котором определена функция.
        '''
        self.figure.clear()
        ax = self.figure.add_subplot()

        # Получение текущих данных
        current_data = self.DataManager.get_current_data()
        if not current_data:
            print("Текущие данные пусты!")

        # Построение первого графика
        ax.plot(current_data, **self.PlotSetting.get_plot_parag(self.plot_color, self.plot_marker, self.plot_line), label='Накопленные импульсы')
        
        # # Добавление второго графика для проверки легенды
        # ax.plot([0, len(current_data) - 1], [min(current_data), max(current_data)], color='red', label='Линия тренда')

        # Установка меток осей и заголовка
        ax.set_xlabel('Значение кванта')
        ax.set_ylabel('Количество квантов')
        ax.set_title(f'Spektr № {self.my_id}')

        # # Добавление легенды
        ax.legend(loc='upper right')
        # ax.set_yscale('log')
        # Обновление холста
        self.canvas.draw()


    def plot_data(self,data):
        """<h1>Строит график на основе переданных данных.</h1>
        </h3>Эта функция очищает текущий график и строит новый на основе переданных данных. 
        Устанавливает метки осей и заголовок графика, а также обновляет данные в <b>DataManager</b>.</h3>

        :param self: экземпляр класса, в котором определена функция.
        :param data: данные для построения графика.
        """
        self.figure.clear()
        ax = self.figure.add_subplot()
        ax.plot(data, **self.PlotSetting.get_plot_parag(), label='Накопленные импульсы')
        # ax.stem(range(len(data)), data)
        ax.set_xlabel('Значение кванта')
        ax.set_ylabel('Колличество квантов')
        ax.set_title(f'Spektr № {self.my_id}')

        ax.legend(loc='upper right')
        # ax.set_yscale('log')
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