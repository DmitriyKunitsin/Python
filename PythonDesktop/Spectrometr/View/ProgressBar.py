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
        self.label = QLabel('Обновление через...', self)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
        self.timer = QBasicTimer()
        self.step = 0
        self.doAction() ## !!!!!!!!!!!!!!!! Имитация пришедшего события (якобы по Uart пришли данные), если этого не сделать, то будет ждать команды из вне
        print('Создан прогресс бар')

    def doAction(self):
        if self.timer.isActive():
            self.step = 0
            # self.timer.stop()
            self.close()
        else:
            self.timer.start(self.max_value_timer,self)
    
    def timerEvent(self, e): ## каждый тик событие
        if self.step >= self.max_value_timer:
            self.close()
            return
        self.step = self.step + 1
        self.progress_bar.setValue(self.step)



