import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Здесь мы создаём две кнопки
        okButton = QPushButton('Ok')
        cancelButton = QPushButton('Cancel')
        
        # Мы создаём макет горизонтального блока, добавляем показатель растяжения и обе кнопки. 
        # Растяжение добавляет растянутое свободное пространство перед двумя кнопками. 
        # Это прижмёт их к правому краю окна.
        hbox = QHBoxLayout() # Мы создаём макет горизонтального блока
        hbox.addStretch(1) # добавляем показатель растяжения
        hbox.addWidget(okButton) # добавляем обе кнопки
        hbox.addWidget(cancelButton)

        # Чтобы создать необходимый макет, мы поставим горизонтальный макет в вертикальный. 
        # Показатель растяжения в вертикальном блоке прижмёт горизонтальный блок с кнопками к нижней части окна.
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox) # поставим горизонтальный макет в вертикальный.


        self.setLayout(vbox) # устанавливаем главный макет окна.

        self.setGeometry(300,300,300,150)
        self.setWindowTitle('Buttons')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
