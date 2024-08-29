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

``` 
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
```

## ToggleButton.py : Кнопка переключателя

Кнопка переключателя – это QPushButton в особом режиме. Это кнопка, которая имеет два состояния: нажатое и не нажатое. Мы переключаемся между этими двумя состояниями, кликая по ней. Существуют ситуации, где эта функциональность отлично подходит.

```
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QFrame, QApplication)
from PyQt5.QtGui import QColor


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Это начальное значение цвета (чёрный).
        self.col = QColor(0,0,0)
        # Чтобы создать кнопку переключателя, 
        # мы создаём QPushButton и делаем её проверяемой, 
        redb = QPushButton('Red', self)
        # путём вызова метода setCheckable().
        redb.setCheckable(True)
        redb.move(10,10)
        # Мы привязываем сигнал к нашему пользовательскому методу. 
        # Мы используем сигнал clicked, который работает с логическим значением.
        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
            self.col.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()

    def setColor(self, pressed):

            # Мы получаем кнопку, которая была переключена.
            source = self.sender()

            if pressed:
                val = 255
            else:
                val = 0
            # В случае кнопки red, мы обновляем красную часть цвета соответственно.
            if source.text() == 'Red':
                self.col.setRed(val)
            elif source.text() == 'Green':
                self.col.setGreen(val)
            else:
                self.col.setBlue(val)
            # Мы используем таблицы стилей, чтобы менять цвет фона.
            self.square.setStyleSheet("QFrame { background-color: %s }" %
            self.col.name())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

## Slider.py : Ползунок
Qslider – ползунок (виджет, который имеет простой регулятор). Этот регулятор может быть утянут назад и вперёд. Таким способом, мы выбираем значение для конкретной задачи. Иногда, использование ползунка более естественно, чем ввод числа или использование переключателя-счётчика. В нашем примере, мы покажем один ползунок и одну метку. Метка будет показывать изображение. Ползунок будет контролировать метку.

```
import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

name_jpg_mute = '../images/mute.jpg'
name_jpg_open = '../images/open.jpg'
name_jpg_exit = '../images/exit.jpg'
name_jpg_looch = '../images/Looch_120_px.jpg'
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Здесь мы создаём горизонтальный ползунок. Qt.Vertical - это вертикальный
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30,40,100,30)
        # Мы привязываем сигнал valueChanged к определенному нами методу changeValue().
        sld.valueChanged[int].connect(self.changeValue)

        # Мы создаём виджет QLabel и устанавливаем начальное изображение "Mute" на него.
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(name_jpg_mute))
        self.label.setGeometry(160,40,80,30)

        self.setGeometry(300,300,280,170)
        self.setWindowTitle('QSlider')
        self.show()


    def changeValue(self, value):
        # Основываясь на значении ползунка, мы устанавливаем изображение на метку. 
        # В коде выше, мы устанавливаем изображение mute.png на метку, если ползунок приравнен к нулю.
        if value == 0:
            self.label.setPixmap(QPixmap(name_jpg_mute))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap(name_jpg_exit))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap(name_jpg_open))
        else:
            self.label.setPixmap(QPixmap(name_jpg_looch))

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

## ProgressBar.py : прогресс бар

QProgressBar – прогресс бар (виджет, который используется, когда мы обрабатываем продолжительные задачи). Он анимирует процесс, чтобы пользователи знали, что задача продвигается. Мы можем установить минимальное и максимальное значение для прогресс бара. Значения по умолчанию – 0 и 99.

```
import sys
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer, Qt



class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Это конструктор QProgressBar.
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40,80)
        self.btn.clicked.connect(self.doAction)

        # Чтобы активировать индикатор прогресса, мы используем объект таймера.
        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300,300,280,170)
        self.setWindowTitle('QProgressBar')
        self.show()


    def timerEvent(self, e):
        # Каждый QObject и его наследники имеют обработчик событий timerEvent(). 
        # Для того, чтобы реагировать на события таймера, мы переопределяем обработчик событий.
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return
        
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        # Внутри метода doAction(), мы запускаем и останавливаем таймер.
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            # Чтобы запустить событие таймера, мы вызываем его методом start(). 
            # Этот метод имеет два параметра: таймаут, и объект, который будет принимать события.
            self.timer.start(100,self)
            self.btn.setText('Stop')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```
В нашем примере, мы имеем горизонтальный индикатор прогресса и кнопку. Кнопка запускает и останавливает индикатор прогресса.

##  CalendarWidget.py : виджет календаря

QCalendarWidget предоставляет виджет помесячного календаря. Он позволяет пользователю выбирать дату простым и интуитивно-понятным способом.

```
import sys
from PyQt5.QtWidgets import (QWidget, QCalendarWidget,
    QLabel, QApplication)
from PyQt5.QtCore import QDate


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        # Если мы выбираем дату из виджета, срабатывает сигнал clicked[QDate]. 
        # Мы присоединяем этот сигнал к пользовательскому методу showDate().
        cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(130, 260)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')
        self.show()


    def showDate(self, date):
        # Мы возвращаем выбранную дату путём вызова метода selectedDate(). 
        # Тогда мы превращаем объект даты в строку и устанавливаем его в виджет метки.
        self.lbl.setText(date.toString())


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```
Пример имеет виджет календаря и виджет метки. Текущая выбранная дата отображается в виджете метки.

##  PixMap.py 

QPixMap – это один из виджетов, использующихся для работы с изображениями. Он оптимизирован для показа изображений на экране. В приведенном ниже примере, мы будем использовать QPixMap для того, чтобы показать изображение в окне.

```
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        hbox = QHBoxLayout(self)
        # Мы создали объект QPixMap.
        pixmap = QPixmap("../images/open.jpg")

        lbl = QLabel(self)
        # Мы поместили изображение в виджет QLabel.
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

В нашем примере, мы показываем изображение в окне.

## LineEdit.py 

QLineEdit – это виджет, который разрешает вводить и редактировать одну строку текста. Для этого виджета доступны функции "Отменить" и "Повторить", "Вырезать" и "Вставить", а также функция "перетаскивания".

```
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
    QLineEdit, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.lbl = QLabel(self)
        # Создается виджет QLineEdit.
        qle = QLineEdit(self)

        qle.move(60, 100)
        self.lbl.move(60, 40)

        # Если текст в виджете редактирования строки меняется, мы вызываем метод onChanged().
        qle.textChanged[str].connect(self.onChanged)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QLineEdit')
        self.show()


    def onChanged(self, text):
        # Внутри метода onChanged, мы устанавливаем напечатанный текст в виджет метки. 
        # Мы вызываем метод adjustSize(), чтобы менять размер метки соответственно длине текста.
        self.lbl.setText(text)
        self.lbl.adjustSize()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```
Этот пример показывает виджет строки редактирования и метку. Текст, который мы вбиваем в строку редактирования, немедленно отображается в виджете метки.

## Splitter.py

QSplitter позволяет пользователю контролировать размер виджетов путём перетаскивания границы между ними. В нашем примере, мы показываем три виджета QFrame, организованные с двумя разделителями.

```
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame,
    QSplitter, QStyleFactory, QApplication)
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        hbox = QHBoxLayout(self)

        # Для того, чтобы видеть границы между виджетами QFrame, мы используем стилизованный фрейм.
        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        # Мы создаём виджет QSplitter и добавляем в него два виджета.
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)
        # К тому же, мы можем добавить разделитель к ещё одному виджету разделителя.
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

В нашем примере, мы имеем три виджета фрейма и два разделителя. Обратите внимание, что в некоторых темах оформления, разделители могут не быть хорошо видимыми.

## ComboBox.py
QComboBox – это виджет, который позволяет пользователю выбирать из списка вариантов (выпадающий список)

```
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
```
Пример показывает QComboBox и QLabel. Блок со списком имеет список из пяти вариантов. Это имена дистрибутивов Linux. Виджет метки показывает выбранный вариант.

