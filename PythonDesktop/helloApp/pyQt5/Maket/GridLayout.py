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

