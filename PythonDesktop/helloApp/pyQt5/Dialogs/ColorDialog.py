import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QColorDialog, QApplication)
from PyQt5.QtGui import QColor


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Это первоначальный цвет фона QtGui.QFrame.
        col = QColor(0,0,0)

        self.btn = QPushButton('Dialog', self)
        self.move(20,20)

        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(133,22,100,100)

        self.setGeometry(300,300,250,180)
        self.setWindowTitle('Color Dialog')
        self.show()



    def showDialog(self):

        # Это строка высветит QColorDialog.
        col = QColorDialog.getColor()

        if col.isValid():
            # Мы проверяем, является ли цвет валидным. 
            # Если мы нажимаем кнопку «Cancel», возвращается невалидный цвет. 
            # Если цвет валиден, мы меняем цвет фона, используя таблицы стилей (CSS).
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()