import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20,20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130,22)

        self.setGeometry(300,300,290,150)
        self.setWindowTitle('Input dialog')
        self.show()


    def showDialog(self):
        # Эта строка показывает диалог ввода. 
        # Первая строка – это заголовок диалога, 
        # вторая – сообщение внутри диалога. 
        # Диалог возвращает введённый текст и логическое значение. 
        # Если мы нажимаем кнопку «ОК», то логическое значение является правдой.
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Введите ваше имя : ')
        # Текст, который мы получили из диалога, устанавливается в виджет редактирования строки.
        if ok:
            self.le.setText(str(text))



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()