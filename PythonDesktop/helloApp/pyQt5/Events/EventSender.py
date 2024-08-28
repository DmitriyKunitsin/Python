import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        btn1 = QPushButton('Button 1', self)
        btn1.move(30,50)

        btn2 = QPushButton('Button 2', self)
        btn2.move(150,50)
        # Обе кнопки подключаются к одному слоту.
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300,300,290,150)
        self.setWindowTitle('Event sender')
        self.show()

    
    def buttonClicked(self):
        # Мы определяем источник сигнала с помощью метода sender(). 
        sender = self.sender()
        # В строке состояния приложения, мы показываем метку нажатой кнопки
        self.statusBar().showMessage(sender.text() + ' was pressed')

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()