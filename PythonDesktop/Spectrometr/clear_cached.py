import os
import shutil
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def clean_cache(directories):
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            if '__pycache__' in dirs:
                cache_dir = os.path.join(root, '__pycache__')
                print(f'{Colors.BLUE}удаление : {cache_dir}{Colors.RESET}')
                shutil.rmtree(cache_dir)

        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                print(f'{Colors.YELLOW}удаление : {file_path}{Colors.RESET}')
                os.remove(file_path)

def main():
    dir_to_clean = ['Model', 'View', 'ViewModel']
    print(f'{Colors.RED}Запуск скрипта очистки кэша{Colors.RESET}')
    clean_cache(dir_to_clean)
    print(f'{Colors.GREEN}Удаление завершено{Colors.RESET}')

if __name__ == '__main__':
    main()