import sys
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer, Qt



class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Это конструктор QProgressBar.
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40,80)
        self.btn.clicked.connect(self.doAction)

        # Чтобы активировать индикатор прогресса, мы используем объект таймера.
        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300,300,280,170)
        self.setWindowTitle('QProgressBar')
        self.show()


    def timerEvent(self, e):
        # Каждый QObject и его наследники имеют обработчик событий timerEvent(). 
        # Для того, чтобы реагировать на события таймера, мы переопределяем обработчик событий.
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return
        
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        # Внутри метода doAction(), мы запускаем и останавливаем таймер.
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            # Чтобы запустить событие таймера, мы вызываем его методом start(). 
            # Этот метод имеет два параметра: таймаут, и объект, который будет принимать события.
            self.timer.start(100,self)
            self.btn.setText('Stop')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()