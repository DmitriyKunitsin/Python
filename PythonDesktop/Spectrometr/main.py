import sys
from PyQt5.QtWidgets import QApplication

try:
    from V.view import MainWindow
    from VM.viewmodel import ViewModel
except ImportError as e:
    print(f'Ошибка импорта: {e}')
def main():
    app = QApplication(sys.argv)
    view_model = ViewModel()
    window = MainWindow(view_model)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
