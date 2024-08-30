from PyQt5.QtWidgets import QAction, qApp, QToolBar
from PyQt5.QtGui import QIcon
from View.ConnectWindow.ConnectWIndow import ConnectWindow
import os

exit_file_name_jpg = 'images/exit.jpg'
connect_file_name_jpg = 'images/connect.jpg'

class CustomToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initTool()

    def set_view_model(self, view_model):
        self.view_model = view_model
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

        connect_action = QAction(QIcon(connect_file_name_jpg), 'Подключиться', self)
        connect_action.setStatusTip('Подключить устройство')
        connect_action.triggered.connect(self.open_connect_window)

        self.addAction(connect_action)

    def open_connect_window(self):
        self.connect_win = ConnectWindow(self.view_model)
        self.connect_win.show()