import sys
from PyQt5.QtWidgets import QApplication

try:
    from View.view import MainWindow
    from ViewModel.viewmodel import ViewModel
except ImportError as e:
    print(f'Ошибка импорта: {e}')
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
