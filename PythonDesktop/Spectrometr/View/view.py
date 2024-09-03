import sys
from PyQt5.QtWidgets import QSizePolicy,QScrollArea,QApplication,QSplitter ,QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLabel , QComboBox, QMainWindow, QStatusBar, QProgressBar, QSpinBox
from PyQt5.QtCore import Qt  

try:
# ViewModel folder
    from ViewModel.viewmodel import ViewModel
# View folder
    from View.Menubar.menubar import CustomMenuBar
    from View.toolbar import CustomToolBar
    from View.ProgressBar import CustomProgressBar
    from View.PlotWindow import PlotWindow
except ImportError as e:
    print(f'Ошибка импорта: {e}')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spektrometr")
        # Инициализация ViewModel
        self.viewmodel = ViewModel()
        self.viewmodel.data_changed.connect(self.update_label)
        self.value_sleep = 0
        self.setGeometry(150,150,1600,800)
        self.initUI()
        self.count_plot = 0
        

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
        self.tool_bar.set_view_model(self.viewmodel)
        self.addToolBar(self.tool_bar)


        self.splitter = QSplitter(Qt.Horizontal)
        ## левый виджет для графиков
        # График
        self.graph_scroll_area = QScrollArea()
        self.graph_scroll_area.setWidgetResizable(True)

        self.graph_scroll_content = QWidget()
        self.graph_scroll_layout = QHBoxLayout(self.graph_scroll_content)
        # Устанавливаем graph_scroll_content как виджет для graph_scroll_area
        self.graph_scroll_area.setWidget(self.graph_scroll_content)

        self.splitter.addWidget(self.graph_scroll_area)

        # правый виджет
        self.right_content = QWidget()
        self.right_layout = QVBoxLayout(self.right_content)

        self.splitter.addWidget(self.right_content)

        self.layout.addWidget(self.splitter)
        
    def update_label(self, data):  # Пришли данные
        print('Пришли новые данные через сигнал data_changed')
        self.created_progress_bar(60000)
        self.count_plot += 1

        new_plot_window = PlotWindow(self.count_plot)  # Создаем новый график
        new_plot_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        try:
            new_plot_window.plot_data(data)  # Обработка данных для нового графика
        except Exception as e:
            print(f"Ошибка при обработке данных для графика: {e}")
        if self.count_plot == 1:
            self.right_layout.addWidget(new_plot_window)
        else:
            if self.right_layout.count() > 0:
                old_plot = self.right_layout.itemAt(0).widget() 
                self.right_layout.removeWidget(old_plot) 
                self.graph_scroll_layout.addWidget(old_plot)  
                self.right_layout.addWidget(new_plot_window)

    def get_data(self):## отправили команду
        self.viewmodel.fetch_data(self.value_sleep)  # Запрос данных из ViewModel
        
    def created_progress_bar(self, value_sleep):
        self.value_sleep = value_sleep
        print(f'self.value_sleep = value_sleep : {self.value_sleep}')
        # Прогресс бар под графиков, показывающий прогресс до обновления
        self.progress_bar = CustomProgressBar(self)
        self.layout.addWidget(self.progress_bar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
