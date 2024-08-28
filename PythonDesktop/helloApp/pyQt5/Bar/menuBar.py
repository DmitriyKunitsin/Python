import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, qApp, QApplication
from PyQt5.QtGui import QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # QAction является абстракцией для действий, совершенных из меню, панели инструментов, или комбинаций клавиш. 
        # В этих трех строках, мы создаем действие с соответствующей иконкой. 
        # Кроме того, для этого действия определяется комбинация клавиш. 
        # Третья строка создает подсказку, которая показывается в строке состояния, когда вы наведёте указатель мыши на пункт меню.
        exitAction = QAction(QIcon('exit.jpg'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Выход')
        # Когда мы выбираем именно это действие, срабатывает сигнал. 
        # Сигнал подключен к методу quit() виджета QApplication. Это завершает приложение.
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        # Метод menuBar() создает строку меню. Мы создаем меню файла и добавляем к нему действие выхода.
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300,300,300,200)
        self.setWindowTitle('Menubar')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
