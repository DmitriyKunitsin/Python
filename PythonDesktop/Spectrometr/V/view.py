from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QMainWindow, QStatusBar
import pyqtgraph as pg

from V.menubar import CustomMenuBar
from V.toolbar import CustomToolBar
from V.device_selector import DeviceSelector
from V.PlotWindow import PlotWindow

class MainWindow(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.initUI()
        self.selected_device = None
        self.view_model.data_changed.connect(self.update_graph)

        # self.populate_devices()

    def initUI(self):
        self.setWindowTitle("Spectromетр")
        self.setGeometry(300,300,300,300)

        # центральный виджет
        cental_widget = QWidget(self)
        self.setCentralWidget(cental_widget)

        layout = QVBoxLayout(cental_widget)

        # Выпадающее окно выбора порта
        # self.device_selector = DeviceSelector(self.view_model)#QComboBox()
        # self.device_selector.device_selected.connect(self.on_device_selected)# Подключаем сигнал
        # layout.addWidget(self.device_selector)

        # self.button_selected_device = QPushButton('Подключиться')
        # self.button_selected_device.clicked.connect(self.select_device)
        # layout.addWidget(self.button_selected_device)

        # Меню бар (верхние кнопки)
        self.menu_bar = CustomMenuBar(self)
        self.menu_bar.set_view_model(self.view_model)
        layout.setMenuBar(self.menu_bar)

        # статус бар (подсказки внизу слева)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # ToolBar (Верхняя панель с картинками)
        self.tool_bar = CustomToolBar()
        self.addToolBar(self.tool_bar)

        self.plot_widget = PlotWindow()
        layout.addWidget(self.plot_widget)

        self.button_fetch_data = QPushButton('Получить данные')
        self.button_fetch_data.clicked.connect(self.fetch_data)
        layout.addWidget(self.button_fetch_data)


    def on_device_selected(self, selected_device):
        # if selected_device is not None:
            self.selected_device = selected_device
            print("Устройство выбрано:", selected_device)

    def populate_devices(self):
        devices = self.view_model.list_devices()
        if not devices:
            print('Нет доступных USB устройств')
            self.device_selector.addItem('Нет доступных USB устройств')
            return
        self.device_selector.add_item(devices)

    def select_device(self):
        selected = self.device_selector.get_selected_device()
        if selected:
            # idVendor, idProduct = selected
            try:
                # self.view_model.select_device(idVendor, idProduct)
                print("Устройство выбрано:", selected)
            except ValueError as e:
                print(e)

    def fetch_data(self):
        try:
            self.view_model.fetch_data()
        except ValueError as e:
            print(e)

    def update_graph(self, data):
        self.plot_widget.plot_data(data)
