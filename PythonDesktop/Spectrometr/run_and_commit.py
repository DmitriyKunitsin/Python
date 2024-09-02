import subprocess
import os

def run_script(script_path):
    """Запускает указанный скрипт."""
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Скрипт {script_path} успешно выполнен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении скрипта {script_path}: {e}")

def git_add_and_commit(commit_message):
    """Добавляет изменения в Git и делает коммит."""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("Изменения успешно добавлены и закоммичены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при добавлении или коммите: {e}")

if __name__ == "__main__":
    # Путь к вашему скрипту
    script_to_run = 'clear_cached.py'  # Замените на имя вашего скрипта

    run_script(script_to_run)

    # Стандартное сообщение для коммита
    commit_message = "Автоматическое обновление после выполнения скрипта."

    git_add_and_commit(commit_message)
