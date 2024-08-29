import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QWidget)
from PyQt5.QtGui import QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('../images/open.jpg'), 'open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300,300,350,300)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialog(self):
        # Мы показываем QFileDialog. Первая строка в методе getOpenFileName() – это заголовок. 
        # Вторая строка указывает на показываемую директорию. 
        # По умолчанию, файловый фильтр установлен в положение «Все файлы (*)».
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        # Выбранный файл читается и содержимое файла записывается в виджет редактирования текста.
        f = open(fname, 'r')

        with f:
            data = f.read()
            self.textEdit.setText(data)



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()