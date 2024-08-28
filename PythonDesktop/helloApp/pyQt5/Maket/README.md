## AbsolutPosition.py : Абсолютное позиционирование

Программист указывает позицию и размер каждого виджета в пикселях. При использовании абсолютного позиционирования, у нас есть следующие ограничения:
Размеры и позиция виджета не меняются, если мы меняем размер окна
Приложения могут выглядеть по-разному на разных платформах
Изменение шрифтов в нашем приложении может испортить макет
Если мы решаем изменить наш макет, мы должны полностью переделать его, что утомительно и занимает много времени

```
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15,10)
        lbl2 = QLabel('Tutorials', self)
        lbl2.move(35,40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55,70)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Absolute')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```



Мы используем метод move(), чтобы разместить наши виджеты.
В нашем случае ими являются метки. Мы размещаем их путём предоставления координат x и y. 
Начало координатной системы – левый верхний угол экрана. 
Значения x возрастают слева направо. Значения y – сверху вниз.

## BlockedMaket.py : Блочный макет

Управление макетом классами макета является более гибким и практичным. Это предпочтительный путь размещения виджетов в окне. QHBoxLayout и QVBoxLayout – это основные классы макета, которые выстраивают виджеты горизонтально или вертикально.

Представьте, что мы хотим разместить две кнопки в правом нижнем углу. Чтобы создать такой макет, мы будем использовать один горизонтальный и один вертикальный блок. Чтобы создать необходимое свободное пространство, мы добавим показатель растяжения.

В этом примере мы размещаем две кнопки в нижнем правом углу окна. Они остаются там, когда мы изменяем размер окна приложения. Мы можем использовать и QHBoxLayout, и QVBoxLayout.
```
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

```

## GridLayout.py : сеточный макет

Самый универсальный класс макета – это сеточный макет. Этот макет делит пространство на строки и столбцы. Чтобы создать сеточный макет, мы используем класс QGridLayout.

В нашем примере, мы создаём сетку из кнопок. Чтобы заполнить один промежуток, мы добавляем один виджет QLabel.

```
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        
        # Создаётся экземпляр QGridLayout, он назначается как макет окна приложения.
        grid = QGridLayout()
        self.setLayout(grid)

        # Это метки, используемые в дальнейшем для кнопок.
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        
        # Мы создаём список позиций для сетки.
        positions = [(i,j) for i in range(5) for j in range(4)] 

        for position, name in zip(positions, names):
# С помощью метода addWidget, создаются и добавляются кнопки к макету.
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        self.move(300,150)
        self.setWindowTitle('Calculate')
        self.show()



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



```