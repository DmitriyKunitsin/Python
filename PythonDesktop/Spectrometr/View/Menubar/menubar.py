from PyQt5.QtWidgets import QMenuBar, QAction, qApp
from PyQt5.QtGui import QIcon
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

class CustomMenuBar(QMenuBar):

    def __init__(self, parent=None, view_model=None):
        super().__init__(parent)
        self.view_model = view_model
        self.initMenu()

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

        # # Загрузка и изменение размера изображения
        # image = Image.open(connect_file_name_jpg)
        # image = image.resize((1024, 1024))  # Задайте нужный размер
        # image.save('images/resized_image.jpg')  # Сохраните изменённое изображение

        # Подключение к порту
        connect_action = QAction(QIcon(connect_file_name_jpg),'Подключиться', self)
        connect_action.setStatusTip('Подключиться к порту')
        connect_action.triggered.connect(self.open_connect_window)

        connect_menu.addAction(connect_action)

        disconect_port_action = QAction(QIcon(), 'Отключиться', self)
        disconect_port_action.setStatusTip('Отключиться от порта')
        disconect_port_action.triggered.connect(self.disconect)

        connect_menu.addAction(disconect_port_action)


        setting_menu = self.addMenu('Setting')

        setting_uart_command = QAction(QIcon(setting_file_name_jpg), 'Настройки платы', self)
        setting_uart_command.setStatusTip('Отправка настроек плате')
        setting_uart_command.triggered.connect(self.open_setting_command_for_stm)

        setting_menu.addAction(setting_uart_command)

    def disconect(self):
        # self.set_view_model()
        if self.view_model:
            self.view_model.disconect_port()
        else:
            print('self.view_model not found')

    def open_connect_window(self):
        self.connect_window = ConnectWindow(self.view_model)
        self.connect_window.show()
    
    def open_setting_command_for_stm(self):
        self.connect_setting_command = Setting_Command(self.view_model)
        self.connect_setting_command.show()


