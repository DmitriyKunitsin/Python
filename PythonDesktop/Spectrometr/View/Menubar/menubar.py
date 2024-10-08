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
        self.setting_menu = None

        # Создаем статусный виджет
        self.status_widget = QWidget()
        self.status_layout = QHBoxLayout(self.status_widget)
        # Создаем лейбл для информации
        self.info_label = QLabel(f"time:{self.view_model.time_update}\nporog:{self.view_model.porog}")
        self.status_layout.addWidget(self.info_label)

        self.status_label = QLabel()
        self.status_label.setFixedSize(20, 20)
        self.update_status(False)

        # Добавляем статусный кружок в layout
        self.status_layout.addWidget(self.status_label)
        self.status_layout.setAlignment(Qt.AlignRight)  # Выравнивание вправо
        self.status_widget.setLayout(self.status_layout)

        self.addWidgetToMenu(self.status_widget)

        if self.view_model:
            self.view_model.connect_signal.connect(self.on_status)
            self.view_model.disconnect_signal.connect(self.off_status)
            self.view_model.new_data.connect(self.update_text_info)

        self.initMenu()
    def update_text_info(self):
        new_text = f'time :{self.view_model.time_update}\n porog: {self.view_model.porog}'
        self.info_label.setText(new_text)
    def addWidgetToMenu(self, widget):
        self.setCornerWidget(widget)
    def set_view_model(self, view_model):
        self.view_model = view_model
    def on_status(self):
        self.update_status(True)
    def off_status(self):
        self.update_status(False)
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


    def disconect(self):
        ''' Меняет булевое значение в цикле чтения порта'''
        if self.view_model:
            try:
                self.view_model.disconect_port()
                # self.update_status(False)
            except Exception as ex:
                print(f'Error : {ex}')
        else:
            print('self.view_model not found')
    def open_connect_window(self):
        ''' Создает окно подключения к девайсу'''
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
            
            # Проверяем, существует ли меню
            if self.setting_menu is None:  # Добавляем меню только если его еще нет
                self.setting_menu = self.addMenu('Setting')

                setting_uart_command = QAction(QIcon(setting_file_name_jpg), 'Настройки платы', self)
                setting_uart_command.setStatusTip('Отправка настроек плате')
                setting_uart_command.triggered.connect(self.open_setting_command_for_stm)

                self.setting_menu.addAction(setting_uart_command)
        else:
            self.status_label.setStyleSheet("background-color: red; border-radius: 10px;")
            
            # Удаляем меню, если оно существует
            if self.setting_menu is not None:
                self.removeAction(self.setting_menu.menuAction())  # Удаляем действие меню
                self.setting_menu = None  # Сбрасываем ссылку на меню
