from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal

class DeviceSelector(QComboBox):

    device_selected = pyqtSignal(object)# Сигнал, который будет отправляться при выборе устройства
    def __init__(self,viev_model):
        super().__init__()
        self.viev_model = viev_model
        self.selected_device = None
        self.currentIndexChanged.connect(self.on_device_changed)

    def add_item(self, devices):
        for device in devices:
            self.addItem(f"{device}", device)  # Добавляем данные устройства как значение элемента
    def on_device_changed(self, index):
        if index >= 0:
            selected_device = self.itemData(index)
            self.device_selected.emit(selected_device)  # Отправляем сигнал с выбранным устройством

    def get_selected_device(self):
        current_index = self.currentIndex()
        if current_index >= 0:
            return self.itemData(current_index)  # Возвращает данные элемента по индексу
        return None