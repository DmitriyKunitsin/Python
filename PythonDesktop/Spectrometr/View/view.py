import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel , QComboBox, QMainWindow, QStatusBar
from ViewModel.viewmodel import ViewModel
from View.menubar import CustomMenuBar
from View.toolbar import CustomToolBar
from View.PlotWindow import PlotWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронное чтение данных")
        # Инициализация ViewModel
        self.viewmodel = ViewModel()
        self.viewmodel.data_changed.connect(self.update_label)
        self.initUI()
        

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)  # Установите макет для центрального виджета
        
        self.label = QLabel("Нажмите кнопку для получения данных")
        self.layout.addWidget(self.label)
        
        self.button = QPushButton("Получить данные")
        self.button.clicked.connect(self.get_data)
        self.layout.addWidget(self.button)
        
        # Меню бар (верхние кнопки)
        self.menu_bar = CustomMenuBar(self)
        self.menu_bar.set_view_model(self.viewmodel)
        self.layout.setMenuBar(self.menu_bar)

        # статус бар (подсказки внизу слева)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # ToolBar (Верхняя панель с картинками)
        self.tool_bar = CustomToolBar()
        self.addToolBar(self.tool_bar)

        self.plot_widget = PlotWindow()
        self.layout.addWidget(self.plot_widget)

        self.setLayout(self.layout)
        

    def get_data(self):
        self.viewmodel.fetch_data()  # Запрос данных из ViewModel

    def update_label(self, data):
        # self.label.setText(f"Полученные данные: {data}")
        self.plot_widget.plot_data(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
