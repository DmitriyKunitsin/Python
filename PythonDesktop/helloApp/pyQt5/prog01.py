import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
# Три важные вещи в объектно-ориентированном программировании это классы, данные и методы
# Здесь мы создаем новый класс Example. Класс Example наследуется от класса QWidget. 
#  Это означает, что мы вызываем два конструктора: первый для класса Example и второй для родительского класса
# Функция super() возвращает родительский объект Example с классом, и мы вызываем его конструктор.
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    # Создание GUI делегируется методу initUI().
    def initUI(self):
        # Все три метода были унаследованы от класса QWidget.
        self.setGeometry(300,300,300,220)
        # Метод setGeometry() делает две вещи: помещает окно на экране и устанавливает его размер.
        # Первые два параметра х и у - это позиция окна.
        # Третий - ширина, и четвертый - высота окна.
        # На самом деле, он сочетает в себе методы resize() и move() в одном методе.
        self.setWindowTitle('Icon')
        # метод устанавливает иконку приложения. Чтобы сделать это, мы создали объект QIcon. QIcon получает путь к нашей иконке для отображения
        self.setWindowIcon(QIcon('Looch_120_px.png'))

        self.show()

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
