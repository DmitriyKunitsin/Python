import os
import shutil


def clean_cache(directories):
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            if '__pycache__' in dirs:
                cache_dir = os.path.join(root, '__pycache__')
                print(f'удаление : {cache_dir}')
                shutil.rmtree(cache_dir)

        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                print(f'удаление : {file_path}')
                os.remove(file_path)

def main():
    dir_to_clean = ['Model', 'View', 'ViewModel']
    print('Запуск скрипта очистки кэша')
    clean_cache(dir_to_clean)

if __name__ == '__main__':
    main()