import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание меню
        # menubar = self.menuBar()
        # file_menu = menubar.addMenu('File')

        # save_action = QAction('Save', self)
        # save_action.triggered.connect(self.save_plot)
        # file_menu.addAction(save_action)

        # Генерация данных для графика
        self.data = np.random.rand(100)

        # Отображение графика
        self.plot_data()

    def plot_data(self):
        """Строит график на основе данных."""
        plt.figure()  # Создание нового окна для графика
        plt.plot(self.data, label='Random Data')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Random Data Plot')
        plt.legend()
        plt.show()  # Отображение графика

    def save_plot(self):
        """Сохранение графика."""
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;All Files (*)", options=options)
        if fileName:
            plt.savefig(fileName)  # Сохранение текущего окна графика

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
