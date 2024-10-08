import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QApplication)
from PyQt5.QtGui import QColor


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Это начальное значение цвета (чёрный).
        self.col = QColor(0,0,0)
        # Чтобы создать кнопку переключателя, 
        # мы создаём QPushButton и делаем её проверяемой, 
        redb = QPushButton('Red', self)
        # путём вызова метода setCheckable().
        redb.setCheckable(True)
        redb.move(10,10)
        # Мы привязываем сигнал к нашему пользовательскому методу. 
        # Мы используем сигнал clicked, который работает с логическим значением.
        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
            self.col.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()

    def setColor(self, pressed):

            # Мы получаем кнопку, которая была переключена.
            source = self.sender()

            if pressed:
                val = 255
            else:
                val = 0
            # В случае кнопки red, мы обновляем красную часть цвета соответственно.
            if source.text() == 'Red':
                self.col.setRed(val)
            elif source.text() == 'Green':
                self.col.setGreen(val)
            else:
                self.col.setBlue(val)
            # Мы используем таблицы стилей, чтобы менять цвет фона.
            self.square.setStyleSheet("QFrame { background-color: %s }" %
            self.col.name())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()