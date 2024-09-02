import serial
import serial.tools.list_ports
import time

def list_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def read_uart(port, baudrate):
    print(f"Подключено к {port}. Введенная скорость = {baudrate}. Начинаем чтение данных...")
    with serial.Serial(port, baudrate, timeout=1, bytesize=8, parity='N', stopbits=1) as ser:
        data_list = []
        i = 0
        last_received_time = time.time()
        timeout_duration = 2 # Время ожидания окончания пакета в секундах
        while True:
            if ser.in_waiting > 0:
                line = ser.readline()  # Читаем строку
                if line:
                    decoded_line = line.decode('utf-8', errors='ignore').strip()
                    
                    if decoded_line.isdigit():
                        last_received_time = time.time() 
                        data_list.append(int(decoded_line))
            # Проверяем таймаут
            if time.time() - last_received_time > timeout_duration and data_list:
                print(f"Получен пакет № {i+1}: {data_list}")
                i+=1
                data_list.clear() # очистка списка
            

if __name__ == "__main__":
    print("Доступные порты:")
    available_ports = list_ports()
    for i, port in enumerate(available_ports):
        print(f"{i + 1}: {port}")

    port_index = int(input("Выберите номер порта: ")) - 1
    selected_port = available_ports[port_index]

    baudrate = int(input("Введите скорость передачи данных (например, 9600): "))
    
    read_uart(selected_port, baudrate)
