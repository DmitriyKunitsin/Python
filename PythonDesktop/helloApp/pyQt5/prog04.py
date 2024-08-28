import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Message box')
        self.show()

    def closeEvent(self, event):
        # Если мы закрываем QWidget, генерируется QCloseEvent. 
        # Чтобы изменить поведение виджета, нам нужно переопределить обработчик события closeEvent().
        reply = QMessageBox.question(self, 'Message', 'Вы действительно хотетие закрыть приложение?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Мы показываем окно с сообщением и с двумя кнопками: Yes и No. 
        # Первая строка отображается в заголовке окна. 
        # Вторая строка является текстовым сообщением и отображается в диалоговом окне. 
        # Третий аргумент определяет комбинацию кнопок, появляющихся в диалоге. 
        # Последний параметр - кнопка по умолчанию. Это кнопка, на которой изначально установлен фокус клавиатуры. 
        # Возвращаемое значение хранится в переменной reply.
        if reply == QMessageBox.Yes:
        # Здесь мы проверяем возвращаемое значение. 
        # Если мы нажмем на кнопку Yes, мы принимаем событие, которое приводит к закрытию виджета и приложения. 
            event.accept()
        else:
        # В противном случае мы будем игнорировать событие закрытия.
            event.ignore()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()