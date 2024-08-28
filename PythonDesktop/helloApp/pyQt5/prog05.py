import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication


class Example(QWidget):
# Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана.
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.resize(250,150)
        # Код, который будет центрировать окно, находится в нами созданном методе center().
        self.center()

        self.setWindowTitle('Center')
        self.show()

    def center(self):
        # Мы получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
        qr = self.frameGeometry()
        # Мы получаем разрешение экрана нашего монитора. И с этим разрешением, мы получаем центральную точку.
        cp = QDesktopWidget().availableGeometry().center()
        # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
        qr.moveCenter(cp)
        # Мы двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
