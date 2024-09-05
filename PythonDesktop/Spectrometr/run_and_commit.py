import subprocess
import os
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"{Colors.GREEN}Скрипт {script_path} успешно выполнен.{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Ошибка при выполнении скрипта {script_path}: {e}{Colors.RESET}")

def git_add_and_commit(commit_message):
    try:
        subprocess.run(['git', 'status'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'status'], check=True)
        print(f"{Colors.BLUE}Изменения успешно добавлены и закоммичены.{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Ошибка при добавлении или коммите: {e}{Colors.RESET}")

if __name__ == "__main__":
    script_to_run = 'clear_cached.py'
    run_script(script_to_run)
    commit_message = "Автоматическое обновление после выполнения скрипта.Удалил отладочные принты и закомиченное"

    git_add_and_commit(commit_message)
