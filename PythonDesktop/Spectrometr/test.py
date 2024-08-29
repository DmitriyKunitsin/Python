import serial
import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def read_uart(port, baudrate):
    print(port)
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Подключено к {port}. введенная скорость = {baudrate} Начинаем чтение данных...")
        while True:
            line = ser.readline()
            if line:
                data = line.decode('utf-8').strip()
                numbers = list(map(int, data.split('\r\n')))
                print("Полученные числа:", numbers)

if __name__ == "__main__":
    print("Доступные порты:")
    available_ports = list_ports()
    for i, port in enumerate(available_ports):
        print(f"{i + 1}: {port}")

    port_index = int(input("Выберите номер порта: ")) - 1
    selected_port = available_ports[port_index]

    baudrate = int(input("Введите скорость передачи данных (например, 9600): "))
    
    read_uart(selected_port, baudrate)
