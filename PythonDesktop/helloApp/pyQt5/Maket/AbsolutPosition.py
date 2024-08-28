import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15,10)
        # Мы используем метод move(), чтобы разместить наши виджеты.
        # В нашем случае ими являются метки. Мы размещаем их путём предоставления координат x и y. 
        # Начало координатной системы – левый верхний угол экрана. 
        # Значения x возрастают слева направо. Значения y – сверху вниз.
        lbl2 = QLabel('Tutorials', self)
        lbl2.move(35,40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55,70)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Absolute')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

