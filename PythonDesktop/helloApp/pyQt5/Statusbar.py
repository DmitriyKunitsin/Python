import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Чтобы получить строку состояния, мы вызываем метод statusBar() класса QtWidgets.
        # QMainWindow. Первый вызов метода создает строку состояния. 
        # Последующие вызовы возвращают объект статусбара. showMessage() отображает сообщение в строке состояния.
        self.statusBar().showMessage('Ready')

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Statusbar')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
