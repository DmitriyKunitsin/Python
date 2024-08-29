import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

name_jpg_mute = '../images/mute.jpg'
name_jpg_open = '../images/open.jpg'
name_jpg_exit = '../images/exit.jpg'
name_jpg_looch = '../images/Looch_120_px.jpg'
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Здесь мы создаём горизонтальный ползунок. Qt.Vertical - это вертикальный
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30,40,100,30)
        # Мы привязываем сигнал valueChanged к определенному нами методу changeValue().
        sld.valueChanged[int].connect(self.changeValue)

        # Мы создаём виджет QLabel и устанавливаем начальное изображение "Mute" на него.
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(name_jpg_mute))
        self.label.setGeometry(160,40,80,30)

        self.setGeometry(300,300,280,170)
        self.setWindowTitle('QSlider')
        self.show()


    def changeValue(self, value):
        # Основываясь на значении ползунка, мы устанавливаем изображение на метку. 
        # В коде выше, мы устанавливаем изображение mute.png на метку, если ползунок приравнен к нулю.
        if value == 0:
            self.label.setPixmap(QPixmap(name_jpg_mute))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap(name_jpg_exit))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap(name_jpg_open))
        else:
            self.label.setPixmap(QPixmap(name_jpg_looch))

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()