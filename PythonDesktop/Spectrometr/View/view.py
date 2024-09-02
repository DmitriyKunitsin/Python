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
        self.tool_bar.set_view_model(self.viewmodel)
        self.addToolBar(self.tool_bar)
        # График
        # self.plot_widget = PlotWindow()
        # self.layout.addWidget(self.plot_widget)


        # QSplitter для графиков
        self.splitter = QSplitter(Qt.Horizontal)

        # Создаем фреймы для добавления в splitter
        left_frame = QWidget()
        left_frame.setStyleSheet("background-color: lightgray;")  # Пример стиля
        right_frame = QWidget()
        right_frame.setStyleSheet("background-color: lightblue;")  # Пример стиля

        # Добавляем фреймы в splitter
        self.splitter.addWidget(left_frame)
        self.splitter.addWidget(right_frame)

        # scroll_content
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # виджет для хранения графиков
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)

        # Добавляем scroll_area в правый фрейм
        right_frame_layout = QVBoxLayout(right_frame)
        right_frame_layout.addWidget(self.scroll_area)

        # Добавляем scroll_area в splitter
        # self.splitter.addWidget(self.scroll_area)

        # Добавляем splitter в основной layout
        self.layout.addWidget(self.splitter)

        # self.layout.addWidget(self.scroll_area)

        # self.setLayout(self.layout)
        

    def get_data(self):## отправили команду
        self.viewmodel.fetch_data(self.value_sleep)  # Запрос данных из ViewModel

    def update_label(self, data): ## Пришли данные
        print('Пришли новые данные через сигнал data_changed')
        self.created_progress_bar(60000)
        # self.value_sleep = 100
        # self.progress_bar = CustomProgressBar(self)
        # self.label.setText(f"Полученные данные: {data}")
        new_plot_frame = QWidget()  # Создаем новый фрейм для графика
        new_plot_layout = QHBoxLayout(new_plot_frame)  # Макет для нового фрейма

        new_plot_window = PlotWindow()  # Создаем новый график
        new_plot_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        new_plot_window.plot_data(data)

        new_plot_layout.addWidget(new_plot_window)  # Добавляем график в новый фрейм

        self.scroll_layout.addWidget(new_plot_frame)  # Добавляем новый фрейм в scroll_layout
        ###
        # new_plot_window = PlotWindow()
        # new_plot_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # new_plot_window.plot_data(data)

        # # self.plot_widget.plot_data(data)
        # self.scroll_layout.addWidget(new_plot_window)


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
