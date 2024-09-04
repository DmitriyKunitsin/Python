from PyQt5.QtWidgets import QWidget , QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
time_plus = 'time_plus'
time_minus = 'time_minus'
value_plus = 'value_plus'
value_minus = 'value_minus'

class PlotWindow(QWidget):

    def __init__(self, id):
        super().__init__()
        self.setWindowTitle('Data Plot')
        self.setGeometry(300, 300, 800, 600)
        self.all_data = []
        self.count_data = 0
        self.temp_data = None
        self.my_id = id
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
        self.button_open_graph.clicked.connect(self.increase_size)
        self.layout.addWidget(self.button_open_graph)

        self.button_horizont_layout = QHBoxLayout()
        # Увеличить график по значению
        self.button_value_plus = QPushButton(f'Увеличить чувствительность нижнего значения', self)
        self.button_value_plus.setStyleSheet('background-color: green')
        self.button_value_plus.clicked.connect(lambda: self.change_plot(value_plus))
        # Уменьшить график по значению
        self.button_value_minus = QPushButton(f'Уменьшить по значению', self)
        self.button_value_minus.setStyleSheet('background-color: blue')
        self.button_value_minus.clicked.connect(lambda: self.change_plot(value_minus))

        self.button_horizont_layout.addWidget(self.button_value_plus)
        self.button_horizont_layout.addWidget(self.button_value_minus)

        # Увеличить график по Времени
        self.button_time_plus = QPushButton(f'Увеличить по времени', self)
        self.button_time_plus.setStyleSheet('background-color: green')
        self.button_time_plus.clicked.connect(lambda: self.change_plot(time_plus))

        # Уменьшить график по времени
        self.button_time_minus = QPushButton(f'Уменьшить по времени', self)
        self.button_time_minus.setStyleSheet('background-color: blue')
        self.button_time_minus.clicked.connect(lambda: self.change_plot(time_minus))

        self.button_horizont_layout.addWidget(self.button_time_plus)
        self.button_horizont_layout.addWidget(self.button_time_minus)

        

        self.layout.addLayout(self.button_horizont_layout)
    def multiply_pairs(self,date):
        temp = []
        for i in range(0, len(date)):
            if date[i] < 50:
                temp.append(date[i] * 2)
        return temp
        
    def delim_pairs(self, data):
        ''' Делит каждое значение '''
        temp = []
        for i in range(0 , len(data)):
            if i + 1 < len(data):
                temp.append(data[i] / 2)
            else:
                temp.append(data[i] / 2)
        return temp
    def sum_pairs(self,data):
        """Суммирует пары элементов в списке."""
        temp = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):  # Проверка на наличие следующего элемента
                temp.append(data[i] + data[i + 1])
            else:
                temp.append(data[i])
        return temp
    def change_plot(self, action):
        if action == time_plus:
            print('нажат PLUS вывод ниже результата')
            self.plot_update(time_plus)
        elif action == time_minus:
            print('нажат MINUS вывод ниже результата')
            self.plot_update(time_minus)
        elif action == value_plus:
            self.plot_update(value_plus)
        elif action == value_minus:
            self.plot_update(value_minus)
    def plot_resize_count(self):
        ''' Рисует новый график из буфера, увеличивая колличество счетов '''
        self.figure.clear()
        ax = self.figure.add_subplot()
        # ax.stem(range(len(self.all_data[self.count_data])), self.multiply_pairs(self.all_data[self.count_data]))
        ax.plot(self.temp_data)
        ax.set_xlabel('Time')
        ax.set_ylabel('Values')
        ax.set_title(f'Spektr № {self.my_id}')
    def plot_print(self):
        ''' Рисует обновленный график '''
        self.figure.clear()
        ax = self.figure.add_subplot()
        # ax.stem(range(len(self.all_data[self.count_data])), self.all_data[self.count_data])
        ax.plot(self.all_data[self.count_data])
        ax.set_xlabel('Time')
        ax.set_ylabel('Values')
        ax.set_title(f'Spektr № {self.my_id}')
    def plot_update(self, action):
        if self.count_data >= 0:
            if action == time_minus and self.count_data != 0:
                self.count_data -= 1
                self.all_data.pop()
                self.temp_data = None
                self.plot_print()
                print(len(self.all_data))
                print(f'Всего сохранено список данных {self.count_data}')
                
            elif action == time_plus and self.count_data < 6: # plus time
                
                self.all_data.append(self.sum_pairs(self.all_data[self.count_data]))
                self.count_data += 1
                self.temp_data = None
                self.plot_print()
                
                print(len(self.all_data))
                print(f'Всего сохранено список данных {self.count_data}')
            elif action == value_minus:
                # TODO изменение по x-ксу уменьшаем
                print('Заглушка уменьшения порога')
            elif action == value_plus:
                if self.temp_data is None:
                    self.temp_data = self.multiply_pairs(self.all_data[self.count_data])
                else:
                    self.temp_data = self.multiply_pairs(self.temp_data)
                self.plot_resize_count()
                # TODO изменения по х-ксу увеличиваем, каждый раз *2, что меньше 50
        self.canvas.draw()

    def plot_steam(self,data):
        self.figure.clear()
        ax = self.figure.add_subplot()

        ax.stem(range(len(data)), data)

        ax.set_title('Stem Plot')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')

        self.canvas.draw()
    def plot_data(self,data):
        self.figure.clear()
        ax = self.figure.add_subplot()
        ax.plot(data)
        # ax.stem(range(len(data)), data)
        ax.set_xlabel('Time')
        ax.set_ylabel('Values')
        ax.set_title(f'Spektr № {self.my_id}')
        # Обновление Canvas
        self.canvas.draw()   
        self.data = data
        self.all_data.append(data)
        print(len(self.all_data))
        print(f'Всего сохранено список данных {self.count_data}')

    def increase_size(self):
        self.pl = PlotWindow(self.my_id)
        self.pl.button_open_graph.deleteLater()
        self.pl.resize(800,800)
        self.pl.plot_data(self.data)
        self.pl.canvas.draw
        self.pl.show()

class DataManager:
    def __init__(self):
        self.all_data = []
        self.count_data = 0
        self.temp_data = None

    def add_data(self, data):
        self.all_data.append(data)
        self.count_data += 1

    def remove_data(self):
        if self.count_data > 0:
            self.all_data.pop()
            self.count_data -= 1

    def get_current_data(self):
        return self.all_data[self.count_data] if self.count_data < len(self.all_data) else None

    def multiply_current_data(self):
        if self.temp_data is None:
            self.temp_data = self.multiply_pairs(self.get_current_data())
        else:
            self.temp_data = self.multiply_pairs(self.temp_data)

    def multiply_pairs(self, data):
        # Реализация умножения пар
        return [x * 2 for x in data]  # Пример умножения на 2

    def get_all_data_length(self):
        return len(self.all_data)
