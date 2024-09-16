from PyQt5.QtWidgets import QProgressBar, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QBasicTimer




class CustomProgressBar(QWidget):


    def __init__(self, view):
        super().__init__()
        self.view = view
        self.max_value_timer = self.view.value_sleep
        self.initProgress()
        self.view.viewmodel.data_changed.connect(self.doAction)

    def initProgress(self):
        layout = QVBoxLayout(self)
        self.label = QLabel(f'Обновление через {self.max_value_timer / 1000} секунд ...', self)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
        self.timer = QBasicTimer()
        self.step = 0
        self.doAction() 
        print('Создан прогресс бар')

    def doAction(self):
        if self.timer.isActive():
            self.step = 0
            # self.timer.stop()
            self.close()
        else:
            self.timer.start(1000,self)# Запуск таймера с интервалом 1 секунда
            self.progress_bar.setMaximum(int(self.max_value_timer / 1000))
    
    def timerEvent(self, e): ## каждый тик событие
        if self.step >= self.max_value_timer / 1000:# миллисекунды в секунды
            self.close()
            return
        self.step = self.step + 1
        self.progress_bar.setValue(self.step)