import sys
from PyQt5.QtCore import  pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication

class Communicate(QObject):
    # Сигнал создаётся с помощью pyqtSignal() как атрибут внешнего класса Communicate.
    closeApp = pyqtSignal()

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.c = Communicate()
        # Пользовательский сигнал closeApp присоединяется к слоту close() класса QMainWindow
        self.c.closeApp.connect(self.close)

        self.setGeometry(300,300,290,150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mouseDoubleClickEvent(self, event):

        self.c.closeApp.emit()



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()