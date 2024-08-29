import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Это конструктор QCheckBox.
        cb = QCheckBox('Show title', self)
        cb.move(20,20)
        # Мы установили заголовок окна так, что мы должны к тому же проверять чекбокс. 
        # По умолчанию, заголовок окна не установлен и чекбокс выключен.
        cb.toggle()
        # Мы связываем наш метод changeTitle(), с сигналом stateChanged. 
        # Метод changeTitle() будет переключать заголовок окна.
        cb.stateChanged.connect(self.changeTitle)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('QCheckBox')
        self.show()


    def changeTitle(self,state):
        if state == Qt.Checked:
        # Если виджет помечен галочкой, мы устанавливаем заголовок окна. 
            self.setWindowTitle('QCheckBox')
        else:
        # В противном случае, мы устанавливаем пустую строку в заголовке.
            self.setWindowTitle('')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
