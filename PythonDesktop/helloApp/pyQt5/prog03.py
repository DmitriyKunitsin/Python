import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication, Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # создаем кнопку. Кнопка является экземпляром класса QPushButton. Первый параметр конструктора - название кнопки.
        # Вторым параметром является родительский виджет.
        # Родительский виджет является виджетом Example, который наследуется от QWidget.
        qbtn = QPushButton('Quit', self)
        
        # Система обработки событий в PyQt5 построена на механизме сигналов и слотов.
        # Если мы нажмем на кнопку, вызовется сигнал "нажатие". 
        # Слот может быть слот Qt или любая Python функция.
        # внимание, что QCoreApplication создается с QApplication. 
        # Сигнал "нажатие" подключен к методу quit(), который завершает приложение. 
        # Коммуникация осуществляется между двумя объектами: отправителя и приемника. 
        # Отправитель кнопка, приемник - объект приложения.
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50,50)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Quic button')
        self.show()

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()