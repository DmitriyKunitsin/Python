from PyQt5.QtWidgets import QMenuBar, QAction, qApp
from PyQt5.QtGui import QIcon
# View folder
from View.ConnectWindow.ConnectWIndow import ConnectWindow

# Setting folder
from View.SettingMenuBar.SettingCommandUartWindow import Setting_Command
# imgages
from PIL import Image

import os

exit_file_name_jpg = 'images/exit.jpg'
connect_file_name_jpg = 'images/connect.jpg'

class CustomMenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
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

        connect_action = QAction(QIcon(connect_file_name_jpg),'Подключиться', self)
        connect_action.setStatusTip('Подключиться к порту')
        connect_action.triggered.connect(self.open_connect_window)

        connect_menu.addAction(connect_action)

        setting_menu = self.addMenu('Setting')

        setting_uart_command = QAction(QIcon(), 'Настройки платы', self)
        setting_uart_command.setStatusTip('Отправка настроек плате')
        setting_uart_command.triggered.connect(self.open_setting_command_for_stm)

        setting_menu.addAction(setting_uart_command)

    def open_connect_window(self):
        self.connect_window = ConnectWindow(self.view_model)
        self.connect_window.show()
    
    def open_setting_command_for_stm(self):
        self.connect_setting_command = Setting_Command(self.view_model)
        self.connect_setting_command.show()


