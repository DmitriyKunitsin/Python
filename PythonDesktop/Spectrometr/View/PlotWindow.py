from PyQt5.QtWidgets import QWidget , QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Plot')
        self.setGeometry(300, 300, 800, 600)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def plot_data(self,data):

        self.figure.clear()

        ax = self.figure.add_subplot()

        ax.plot(data)
        ax.set_xlabel('Time')
        ax.set_ylabel('Values')
        ax.set_title('Spektr')

        # Обновление Canvas
        self.canvas.draw()
        # plt.plot(data)
        # plt.xlabel('Time')
        # plt.ylabel('Values')
        # plt.title('Spektr')
        # plt.show()