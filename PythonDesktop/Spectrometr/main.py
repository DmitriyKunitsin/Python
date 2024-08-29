import sys
from PyQt5.QtWidgets import QApplication
from view import MainWindow
from viewmodel import ViewModel

def main():
    app = QApplication(sys.argv)
    view_model = ViewModel()
    window = MainWindow(view_model)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
