from PyQt5.QtWidgets import QWidget , QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 


class PlotWindow(QWidget):

    def __init__(self, id):
        super().__init__()
        self.setWindowTitle('Data Plot')
        self.setGeometry(300, 300, 800, 600)
        
        self.my_id = id
        self.layout = QVBoxLayout(self)
        
        # Закрыть
        self.button_exit = QPushButton('Закрыть', self)
        self.button_exit.clicked.connect(self.close)

        self.layout.addWidget(self.button_exit)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # self.layout.addItem(QSpacerItem(20,40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Кнопка для увеличения графика
        self.button = QPushButton(f'Открыть график {self.my_id}')
        self.button.clicked.connect(self.increase_size)
        self.layout.addWidget(self.button)

        self.button_horizont_layout = QHBoxLayout()

        # Увеличить график по Времени
        self.button_time_plus = QPushButton(f'Увеличить по времени', self)

        # Уменьшить график по времени
        self.button_time_minus = QPushButton(f'Уменьшить по времени', self)

        self.button_horizont_layout.addWidget(self.button_time_plus)
        self.button_horizont_layout.addWidget(self.button_time_minus)

        # Увеличить график по значению
        self.button_value_plus = QPushButton(f'Увеличить по значению', self)
        # Уменьшить график по значению
        self.button_value_minus = QPushButton(f'Уменьшить по значению', self)

        self.button_horizont_layout.addWidget(self.button_value_plus)
        self.button_horizont_layout.addWidget(self.button_value_minus)
        

        self.layout.addLayout(self.button_horizont_layout)


    def plot_data(self,data):

        # self.figure.clear()

        ax = self.figure.add_subplot()

        ax.plot(data)
        ax.set_xlabel('Time')
        ax.set_ylabel('Values')
        ax.set_title(f'Spektr № {self.my_id}')

        # Обновление Canvas
        self.canvas.draw()
        self.data = data
        # plt.plot(data)
        # plt.xlabel('Time')
        # plt.ylabel('Values')
        # plt.title('Spektr')
        # plt.show()

    def increase_size(self):
        self.pl = PlotWindow(self.my_id)
        self.pl.button.deleteLater()
        self.pl.resize(800,800)
        self.pl.plot_data(self.data)
        self.pl.canvas.draw
        self.pl.show()

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        
        min_width_px = 400 
        min_height_px = 300 

        if width < min_width_px:
            width = min_width_px
        if height < min_height_px:
            height = min_height_px

        winch = width / self.figure.dpi
        hinch = height / self.figure.dpi

        if winch > 0 and hinch > 0:
            self.figure.set_size_inches(winch, hinch, forward=False)
        else:
            print("Получены некорректные размеры:", winch, hinch)
            self.figure.set_size_inches(4, 5, forward=False)

        self.canvas.draw()
