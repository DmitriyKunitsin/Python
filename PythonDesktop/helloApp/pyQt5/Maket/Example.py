import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        # Мы создаём сеточный макет и устанавливаем промежуток между виджетами.
        grid.setSpacing(10)

        grid.addWidget(title,1,0)
        grid.addWidget(titleEdit,1,1)
        
        grid.addWidget(author,2,0)
        grid.addWidget(authorEdit,2,1)

        # Если мы добавляем виджет к сетке, мы можем обеспечить объединение строк и столбцов виджета. 
        grid.addWidget(review,3,0)
        # В нашем примере, мы делаем так, что виджет reviewEdit объединяет 5 строк.
        grid.addWidget(reviewEdit,3,1,5,1)

        self.setLayout(grid)

        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Review')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()