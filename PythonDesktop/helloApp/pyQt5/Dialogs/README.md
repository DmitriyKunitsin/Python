# Диалоговоые окна

Диалоговые окна (диалоги) являются неотъемлемой частью большинства современных графических приложений. Диалог в обычной жизни - это беседа между двумя и более людьми. В компьютерном приложении, диалог – это окно, которое используется, чтобы «беседовать» с приложением. Диалоги используются для ввода и изменения данных, изменения настроек приложения, и так далее.

## inputdialog.py : Диалог

QInputDialog - простой удобный диалог для получения единственного значения от пользователя. Введённое значение может быть строкой, числом или пунктом из списка.

```
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
```

Пример имеет кнопку и виджет редактирования строки. Кнопка показывает диалог ввода. Вводимый текст может быть отображён в виджете редактирования строки.

## ColorDialog.py : Цветовой диалог

QColorDialog - виджет диалога для выбора цветовых значений.

```
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QColorDialog, QApplication)
from PyQt5.QtGui import QColor


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Это первоначальный цвет фона QtGui.QFrame.
        col = QColor(0,0,0)

        self.btn = QPushButton('Dialog', self)
        self.move(20,20)

        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(133,22,100,100)

        self.setGeometry(300,300,250,180)
        self.setWindowTitle('Color Dialog')
        self.show()



    def showDialog(self):

        # Это строка высветит QColorDialog.
        col = QColorDialog.getColor()

        if col.isValid():
            # Мы проверяем, является ли цвет валидным. 
            # Если мы нажимаем кнопку «Cancel», возвращается невалидный цвет. 
            # Если цвет валиден, мы меняем цвет фона, используя таблицы стилей (CSS).
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

## FontDialog.py :  виджет диалога для выбора шрифта.

QFontDialog – это виджет диалога для выбора шрифта.

```
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QFontDialog, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btn.move(20,20)

        vbox.addWidget(btn)

        btn.clicked.connect(self.showDialog)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130,20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setGeometry(300,300,250,180)
        self.setWindowTitle('Font dialog')
        self.show()


    def showDialog(self):

        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```
В нашем примере, мы имеем кнопку и метку. С помощью QFontDialog, мы меняем шрифт метки.

## FileDialog.py : диалог, который позволяет пользователям выбирать файлы

QFileDialog – это диалог, который позволяет пользователям выбирать файлы или папки. Файлы могут быть выбраны и для открытия, и для сохранения.

