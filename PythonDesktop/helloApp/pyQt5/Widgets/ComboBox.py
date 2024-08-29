import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
    QComboBox, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.lbl = QLabel("Ubuntu", self)

        # Мы создаём виджет QComboBox с пятью вариантами.
        combo = QComboBox(self)
        combo.addItems(["Ubuntu", "Mandriva",
                        "Fedora", "Arch", "Gentoo"])

        combo.move(50, 50)
        self.lbl.move(50, 150)

        # После выбора пункта, мы вызываем метод onActivated().
        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()


    def onActivated(self, text):
        # Внутри метода, мы устанавливаем текст выбранного пункта в виджет метки. 
        # Мы приспосабливаем размер метки, как в прошлом примере.
        self.lbl.setText(text)
        self.lbl.adjustSize()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()