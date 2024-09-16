from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QComboBox, QHBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon
import numpy as np


setting_file_name_jpg = 'images/setting.jpg'

class Setting_Command(QWidget):
    def __init__(self, viev_model):
        super().__init__()
        self.setWindowTitle('Setting Window')
        self.setWindowIcon(QIcon(setting_file_name_jpg))
        self.setGeometry(300,300,300,200)
        self.viev_model = viev_model
        self.initUI()
        self.value_sleep = 100
        self.time = None
        self.coefficient = None
        self.porog = None
    def initUI(self):
        self.layout = QVBoxLayout()
        # self.h_time_layout = QHBoxLayout()
        # ## Настройка времени сбора платой
        # self.label_baud = QLabel('Выберите частоту обновления (в секундах)')
        # self.h_time_layout.addWidget(self.label_baud)
        # self.list_time_update = QComboBox()
        # self.set_list_time_upd()
        # self.list_time_update.currentTextChanged.connect(self.selected_time)
        # self.h_time_layout.addWidget(self.list_time_update)

        # self.layout.addLayout(self.h_time_layout)

        # self.h_voultage_porog = QHBoxLayout()
        # ## Настройка резистора (Коэфициент усиления)
        # self.label_voultage = QLabel('Выберите коэфициент усиления')
        # self.h_voultage_porog.addWidget(self.label_voultage)
        # self.list_coefficient_voultage = QComboBox()
        # self.set_list_coefficient_value()
        # self.list_coefficient_voultage.currentTextChanged.connect(self.selected_voultage)
        # self.h_voultage_porog.addWidget(self.list_coefficient_voultage)

        # self.layout.addLayout(self.h_voultage_porog)
        
        ## Настройка напряжения отсечки
        self.h_min_voultage = QHBoxLayout()
        self.label_osechka = QLabel('Выберите минимальный порог напряжения для сбора')
        self.h_min_voultage.addWidget(self.label_osechka)
        self.list_min_porog = QComboBox()
        self.set_list_min_voult()
        self.list_min_porog.currentTextChanged.connect(self.selected_porog)
        self.h_min_voultage.addWidget(self.list_min_porog)

        self.layout.addLayout(self.h_min_voultage)

        self.h_button_control = QHBoxLayout()

        self.button_connect = QPushButton('Установить')
        ## TODO Отправка команды плате и обнуление графика
        self.h_button_control.addWidget(self.button_connect)
        self.button_connect.clicked.connect(self.push_fetch_setting)

        self.button_cancel = QPushButton('Отмена')
        self.h_button_control.addWidget(self.button_cancel)
        self.button_cancel.clicked.connect(self.close)


        self.layout.addLayout(self.h_button_control)

        self.setLayout(self.layout)
    def push_fetch_setting(self):
        if self.porog is not None:
            self.viev_model.setting_new_values_configurate(self.porog)
            self.close()
            print(f'Выбраное время :{self.time}\nВыбранный коэфициент усиления :{self.coefficient}\nВыбранный минимальный порог :{self.porog}')
        else:
            self.show_dialog_input_date()
            print('выберите значения')

    def show_dialog_input_date(self):
        if self.time is None:
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите время обновления')
        elif self.coefficient is None:
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите коэфициент усиления')
        elif self.porog is None:
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите порог')
        # Если пользователь не выбрал все значения
        elif not (self.coefficient and self.time and self.porog):
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, введите все значения!')

    def selected_time(self):
        index = self.list_time_update.currentIndex()
        if index != 0:
            self.time = self.list_time_update.itemText(index)
            print('selected time',self.time)
        else:
            self.time = None

    def selected_voultage(self):
        index = self.list_coefficient_voultage.currentIndex()
        if index != 0:
            self.coefficient = self.list_coefficient_voultage.itemText(index)
            print('selected coeff',self.coefficient)
        else:
            self.coefficient = None

    def selected_porog(self):
        index = self.list_min_porog.currentIndex()
        if index != 0:
            self.porog = self.list_min_porog.itemText(index)
            print('selected porog',self.porog)
        else:
            self.porog = None
            
    def populate_combobox(self, combobox, default_text, start, end, unit):
        combobox.addItem(f'Текущий {str(default_text)}')
        # if combobox == self.list_time_update:
        #     combobox.addItems([f'{i} {unit}' for i in range(5, 61, 5)])
        # else:
        values = np.arange(start, end + 0.1, 0.1)
        combobox.addItems([f'{i:.1f}{unit}' for i in values])

    # def set_list_time_upd(self):
    #     self.populate_combobox(self.list_time_update,'Выберите...', 5, 60, ' Сек')

    def set_list_min_voult(self):
        self.populate_combobox(self.list_min_porog,self.viev_model.current_configuration(), 0.1, 3.0, ' Вольт')

    def set_list_coefficient_value(self):
        self.populate_combobox(self.list_coefficient_voultage,'Выберите...', 0.1, 3.0, ' Вольт')