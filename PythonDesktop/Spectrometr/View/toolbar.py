from PyQt5.QtWidgets import QAction, qApp, QToolBar
from PyQt5.QtGui import QIcon
try:
    from View.Menubar.ConnectWindow.ConnectWIndow import ConnectWindow
except ImportError as e:
    print(f'Ошибка импорта: {e}')
import os

exit_file_name_jpg = 'images/exit.jpg'
connect_file_name_jpg = 'images/connect.jpg'
disconnect_file_name_png = 'images/disconnect.png'

class CustomToolBar(QToolBar):

    def __init__(self, parent=None,view_model=None, menu_bar=None):
        super().__init__(parent)
        self.menu_bar = menu_bar
        self.view_model = view_model
        self.initTool()

    # def set_view_model(self, view_model):
    #     self.view_model = view_model
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

        disconnect_action = QAction(QIcon(disconnect_file_name_png), 'Отключиться', self)
        disconnect_action.setStatusTip('Отключиться от порта')
        disconnect_action.triggered.connect(self.menu_bar.disconect)

        self.addAction(disconnect_action)


    def open_connect_window(self):
        self.connect_win = ConnectWindow(self.view_model, self.menu_bar)
        self.connect_win.show()