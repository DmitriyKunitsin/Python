# События
Все приложения с графическим интерфейсом являются событийно-ориентированными. События вызываются главным образом пользователем приложения. Однако, они могут быть вызваны другими средствами, к примеру подключением к Интернету, диспетчером окон или таймером. Когда мы вызываем метод exec_(), приложение входит в главный цикл. Главный цикл получает события и отправляет их объектам.

В модели событий имеются три участника:

   1) Источник события
   2) Объект события
   3) Цель события

Источник события – это объект, состояние которого меняется. Он вызывает событие. Событие инкапсулирует изменение состояния в источнике события. Цель события – это объект, которому требуется уведомление. Объект источника события делегирует задачу обработки события цели события.

Для работы с событиями PyQt5 имеет уникальный механизм сигналов и слотов. Сигналы и слоты используются для связи между объектами. Сигнал срабатывает тогда, когда происходит конкретное событие. Слот может быть любой функцией. Слот вызывается, когда срабатывает его сигнал.


## SignalAndSlots.py : Сигналы и слоты

В этом примере, мы показываем QtGui.QLCDNumber и QtGui.QSlider. Мы меняем число lcd путём перемещения ползунка регулятора.

```
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        # Здесь мы присоединяем сигнал valueChanged слайдера к слоту display числа lcd.
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Signal & slot')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

```

Отправитель – объект, который посылает сигнал. Получатель – объект, который получает сигнал. Слот – это метод, который реагирует на сигнал.

## EventHandlOverrid.py : Переопределение обработчика события

События в PyQt5 часто обрабатываются путём переопределения обработчиков.

```
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Event handler')
        self.show()


    def keyPressEvent(self, e):
    # Если мы нажимаем клавишу Esc, то приложение завершается.
        if e.key() == Qt.Key_Escape:
            self.close()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```
В этом примере, мы переопределяем обработчик события keyPressEvent().

## Event sender : Отправитель события

Иногда удобно знать, какой именно виджет является отправителем сигнала. Для этого PyQt5 имеет метод sender()

```
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
```
В нашем примере у нас есть две кнопки. В методе buttonClicked() мы определяем, какую из кнопок мы нажали с помощью метода sender().

## PushEvent.py : Отправка сигналов

Объекты, создаваемые из QObject, могут посылать сигналы. В следующем примере, мы увидим, как мы может послать пользовательский сигнал.

```
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
```

Когда мы дважды кликаем на окне курсором мыши, посылается сигнал closeApp. Приложение завершается.

В этой части руководства PyQt5, мы рассмотрели сигналы и слоты.