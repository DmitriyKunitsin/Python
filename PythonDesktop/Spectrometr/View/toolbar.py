from PyQt5.QtWidgets import QAction, qApp, QToolBar
from PyQt5.QtGui import QIcon
import os

exit_file_name_jpg = 'images/exit.jpg'

class CustomToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initTool()

    def initTool(self):
        # наличие файла для иконки
        if not os.path.isfile(exit_file_name_jpg):
            print(f"Файл не найден: {exit_file_name_jpg}")

        # действие для выхода
        exit_action = QAction(QIcon(exit_file_name_jpg), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')  # комбинация клавиш
        exit_action.setStatusTip('Выход')    # Подсказка
        exit_action.triggered.connect(qApp.quit)  # выход 

        self.addAction(exit_action)
