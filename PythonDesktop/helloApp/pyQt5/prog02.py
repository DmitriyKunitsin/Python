import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget,QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Этот статический метод устанавливает шрифт, используемый для отображения подсказки. Мы используем шрифт 10px SansSerif.
        QToolTip.setFont(QFont('SansSerif', 10))

        # Чтобы создать всплывающую подсказку, мы вызываем метод setToolTip(). Мы можем использовать форматирование текста.
        self.setToolTip('This is a <b>QWidget</b> widget')

        # Мы создаем виджет кнопки и устанавливаем подсказку для него.
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        # Меняем размер кнопки и перемещаем относительно окна. Метод sizeHint() дает рекомендуемый размер для кнопки.
        btn.resize(btn.sizeHint())
        btn.move(50,50)

        self.setGeometry(300,300,300,200)
        self.setWindowTitle('ToolTips')
        self.show()

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()