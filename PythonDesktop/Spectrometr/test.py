import usb.core
import usb.util

try:
    devices = list(usb.core.find(find_all=True))  # Преобразуем генератор в список
    print('Devices:')
    
    if devices:  # Проверяем, есть ли устройства
        for dev in devices:
            print(f'Device: {dev.idVendor}:{dev.idProduct}:{dev.address}')
    else:
        print('Нет USB устройств')
except Exception as e:
    print(f'Ошибка: {e}')