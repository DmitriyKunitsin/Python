import sys
from PyQt5.QtWidgets import (QWidget, QCalendarWidget,
    QLabel, QApplication)
from PyQt5.QtCore import QDate


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        # Если мы выбираем дату из виджета, срабатывает сигнал clicked[QDate]. 
        # Мы присоединяем этот сигнал к пользовательскому методу showDate().
        cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(130, 260)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')
        self.show()


    def showDate(self, date):
        # Мы возвращаем выбранную дату путём вызова метода selectedDate(). 
        # Тогда мы превращаем объект даты в строку и устанавливаем его в виджет метки.
        self.lbl.setText(date.toString())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()