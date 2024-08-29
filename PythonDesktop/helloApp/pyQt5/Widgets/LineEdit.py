import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
    QLineEdit, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.lbl = QLabel(self)
        # Создается виджет QLineEdit.
        qle = QLineEdit(self)

        qle.move(60, 100)
        self.lbl.move(60, 40)

        # Если текст в виджете редактирования строки меняется, мы вызываем метод onChanged().
        qle.textChanged[str].connect(self.onChanged)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QLineEdit')
        self.show()


    def onChanged(self, text):
        # Внутри метода onChanged, мы устанавливаем напечатанный текст в виджет метки. 
        # Мы вызываем метод adjustSize(), чтобы менять размер метки соответственно длине текста.
        self.lbl.setText(text)
        self.lbl.adjustSize()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()