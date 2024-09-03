from PyQt5.QtWidgets import QMenuBar, QAction, qApp, QLabel, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
try:
    # View folder
    from View.Menubar.ConnectWindow.ConnectWIndow import ConnectWindow

    # Setting folder
    from View.Menubar.SettingMenuBar.SettingCommandUartWindow import Setting_Command
except ImportError as e:
    print(f'Ошибка импорта: {e}')
# imgages
from PIL import Image

import os

exit_file_name_jpg = 'images/exit.jpg'
connect_file_name_jpg = 'images/connect.jpg'
setting_file_name_jpg = 'images/setting.jpg'
disconnect_file_name_png = 'images/disconnect.png'

class CustomMenuBar(QMenuBar):

    def __init__(self, parent=None, view_model=None):
        super().__init__(parent)
        self.view_model = view_model

        # Создаем статусный виджет
        self.status_widget = QWidget()
        self.status_layout = QHBoxLayout(self.status_widget)
        self.status_label = QLabel()
        self.status_label.setFixedSize(20, 20)
        self.update_status(False)

        # Добавляем статусный кружок в layout
        self.status_layout.addWidget(self.status_label)
        self.status_layout.setAlignment(Qt.AlignRight)  # Выравнивание вправо
        self.status_widget.setLayout(self.status_layout)

        self.addWidgetToMenu(self.status_widget)

        self.initMenu()
    
    def addWidgetToMenu(self, widget):
        self.setCornerWidget(widget)
    def set_view_model(self, view_model):
        self.view_model = view_model

    def initMenu(self):
        file_menu = self.addMenu('Menu') # создаю объект менюшки
        if not os.path.isfile(exit_file_name_jpg):
            print(f"Файл не найден: {exit_file_name_jpg}")
            
        # создаю действие
        exit_action = QAction(QIcon(exit_file_name_jpg), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q') # Комбинация 
        exit_action.setStatusTip('Выход') # Подсказка 
        exit_action.triggered.connect(qApp.quit) 
        
        file_menu.addAction(exit_action)

        connect_menu = self.addMenu('Device')
        # Подключение к порту
        connect_action = QAction(QIcon(connect_file_name_jpg),'Подключиться', self)
        connect_action.setStatusTip('Подключиться к порту')
        connect_action.triggered.connect(self.open_connect_window)

        connect_menu.addAction(connect_action)

        disconect_port_action = QAction(QIcon(disconnect_file_name_png), 'Отключиться', self)
        disconect_port_action.setStatusTip('Отключиться от порта')
        disconect_port_action.triggered.connect(self.disconect)

        connect_menu.addAction(disconect_port_action)

        setting_menu = self.addMenu('Setting')

        setting_uart_command = QAction(QIcon(setting_file_name_jpg), 'Настройки платы', self)
        setting_uart_command.setStatusTip('Отправка настроек плате')
        setting_uart_command.triggered.connect(self.open_setting_command_for_stm)

        setting_menu.addAction(setting_uart_command)

    def disconect(self):
        ''' Меняет булевое значение в цикле чтения порта'''
        if self.view_model:
            self.view_model.disconect_port()
            self.update_status(False)
        else:
            print('self.view_model not found')
    def open_connect_window(self):
        ''' Создает окно подключения к девайсу'''
        self.update_status(True)
        self.connect_window = ConnectWindow(self.view_model)
        self.connect_window.show()
    def open_setting_command_for_stm(self):
        ''' Создает окно с настройками платы'''
        self.connect_setting_command = Setting_Command(self.view_model)
        self.connect_setting_command.show()
    def update_status(self, is_connected):
        """Обновляет статус подключения."""
        if is_connected:
            self.status_label.setStyleSheet("background-color: green; border-radius: 10px;")
        else:
            self.status_label.setStyleSheet("background-color: red; border-radius: 10px;")
