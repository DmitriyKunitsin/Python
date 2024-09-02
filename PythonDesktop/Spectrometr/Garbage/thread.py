import threading
import time

# Создаем событие для остановки потоков
stop_event = threading.Event()

# Функция для вывода чисел
def print_numbers():
    for i in range(1, 6):
        if stop_event.is_set():  # Проверяем, установлено ли событие
            print("Stopping number thread.")
            break
        print(f"Number: {i}")
        time.sleep(1)

# Функция для вывода букв
def print_letters():
    for letter in 'ABCDE':
        if stop_event.is_set():  # Проверяем, установлено ли событие
            print("Stopping letter thread.")
            break
        print(f"Letter: {letter}")
        time.sleep(1.5)

# Создаем потоки
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Запускаем потоки
thread1.start()
thread2.start()

# Даем потокам немного поработать
time.sleep(3)

# Устанавливаем событие для остановки потоков
stop_event.set()

# Ждем завершения обоих потоков
thread1.join()
thread2.join()

print("Both threads have finished.")
