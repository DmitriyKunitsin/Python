import sqlite3

import os

NAME_CONST_TABLE_USERS = "users"
NAME_CONST_TABLE_TRAININGS = "trainings"
NAME_CONST_TABLE_WORKOUTS = "workouts"
db_path = r"Python_Bot\\db\\bot_database.db"
is_corect = False
folder = os.path.dirname(db_path)
if not os.path.exists(folder):
    os.makedirs(folder)
if os.path.exists(db_path):
    is_corect = True
    print("Подключен к базе данных")
if is_corect:
    """
    ! При необходимости удалить базу данных поставил True
    """
    if False:
        connect = sqlite3.connect(db_path, check_same_thread=False)
        cursor = connect.cursor()
        db_path = "db\\bot_database.db"
        if os.path.exists(db_path):
            print(f"Удаляю файл базы {db_path}")
            os.remove(db_path)
        else:
            print(f"Файл базы {db_path} не найден, удаление не требуется")
            
            
        # Таблица с пользователем   
        cursor.execute(f'''
        CREATE TABLE {NAME_CONST_TABLE_USERS} (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный Telegram ID пользователя
            username TEXT,                        -- имя пользователя (@username)
            first_name TEXT,                      -- имя
            last_name TEXT,                       -- фамилия
            full_name TEXT,                       -- полное имя (можно формировать из first_name + last_name)
            language_code TEXT,                   -- язык пользователя
            is_bot BOOLEAN DEFAULT 0,             -- флаг, является ли пользователь ботом
            is_premium_activeted BOOLEAN DEFAULT 1, -- Флаг, является ли пользователь премиум подписчиком
            height_user REAL CHECK(height_user >= 50 AND height_user <= 272),                   -- Рост пользователя
            weight_user REAL CHECK(weight_user >= 2 AND weight_user <= 635),                   --- Вес пользователя
            IWM_user REAL,                      -- ИМТ пользователя
            gender TEXT CHECK(gender IN ('Boy', 'Girl')),
            age_user INTEGER CHECK(age_user > 0 AND age_user < 100),-- Возраст пользователя
            email TEXT UNIQUE,                  -- Email пользователя ( только уникальный )
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- дата и время добавления пользователя в БД
        )
        ''')
        connect.commit()

        # Таблица программы конкретного пользователя
        cursor.execute(
            f'''
            CREATE TABLE {NAME_CONST_TABLE_TRAININGS} (
            training_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,               -- внешний ключ на users.user_id
            training_name TEXT NOT NULL,            -- название программы
            description TEXT,                       -- описание программы (опционально)
            is_individual BOOLEAN DEFAULT 1,        -- флаг, является ли тренировка индвидиуальной, не в общем доступе
            is_premium BOOLEAN DEFAULT 0,           -- Флаг, является ли тренировка доступна только по премиуму
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            '''
        )
        connect.commit()

        # Индекс на таблицу, для ускорения сортировки быстрый (индексированный) доступ ко вторичным ключам
        cursor.execute(
            '''
        CREATE INDEX idx_trainings_user_id ON trainings(user_id);

            '''
        )
        connect.commit()

        # Таблица с результатами тренировок
        cursor.execute(
            f'''
            CREATE TABLE {NAME_CONST_TABLE_WORKOUTS} (
            workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
            training_id INTEGER NOT NULL,          -- внешний ключ на trainings.training_id
            exercise_name TEXT NOT NULL,          -- название упражнения
            weight REAL NOT NULL,                  -- поднятый вес (кг или фунты)
            repetitions INTEGER,                   -- количество повторений (опционально)
            notes TEXT,                           -- дополнительные заметки (опционально)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (training_id) REFERENCES trainings(training_id) ON DELETE CASCADE
            )
            '''
        )
        connect.commit()

        # Индекс на таблицу, для ускорения сортировки быстрый (индексированный) доступ ко вторичным ключам
        cursor.execute(
            '''
        CREATE INDEX idx_workoutss_user_id ON workouts(training_id);

            '''
        )
        connect.commit()

def connect_to_db():
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"База данных не найдена по пути: {db_path}")
    connect = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connect.cursor()
    return connect, cursor

def add_or_update_user(user):
    connect, cursor = connect_to_db()
    if connect is None or cursor is None:
        print("Ошибка: база данных отсутствует")
    else:
        cursor.execute(f'''
            INSERT INTO {NAME_CONST_TABLE_USERS}(user_id, username, first_name, last_name,full_name)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                full_name=excluded.full_name
        ''', (user.id, user.username, user.first_name, user.last_name, user.full_name))
        connect.commit()

def get_user_data(user_id: int) -> str | None:
    try:
        connect, cursor = connect_to_db()
        cursor.execute(f'SELECT * FROM {NAME_CONST_TABLE_USERS} WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        return row if row else None
    except sqlite3.Error as ex:
        # Ошибка работы с базой — пробрасываем дальше
        raise RuntimeError(f"Ошибка базы данных: {ex}")
    finally:
        cursor.close()
    
def set_user_age(user ,age) -> str | None:
    try:
        connect, cursor = connect_to_db()
        if connect is None or cursor is None:
            print("Ошибка: база данных отсутствует")
        else:
            cursor.execute(f'''
                        UPDATE {NAME_CONST_TABLE_USERS}
                        SET  age_user = {age}
                        WHERE user_id = {user.id}
                        ''')
            connect.commit()
    except Exception as ex:
        print(f'Ошибка при записи возраста в базу данных {ex}')
        return f"{ex}"
    finally:
        cursor.close()
    return "Успешно"

def set_user_weight(user ,weight) -> str | None:
    try:
        connect, cursor = connect_to_db()
        if connect is None or cursor is None:
            print("Ошибка: база данных отсутствует")
        else:
            cursor.execute(f'''
                        UPDATE {NAME_CONST_TABLE_USERS}
                        SET  weight_user = ?
                        WHERE user_id = ?
                        ''', (weight, user.id))
            connect.commit()
    except Exception as ex:
        print(f'Ошибка при записи веса в базу данных {ex}')
        return f"{ex}"
    finally:
        cursor.close()
    return "Успешно"

def set_user_height(user, height) -> str | bool:
    try:
        connect, cursor = connect_to_db()
        if connect is None or cursor is None:
            print("Ошибка: база данных отсутствует")
        else:
            cursor.execute(f'''
                        UPDATE {NAME_CONST_TABLE_USERS}
                        SET  height_user = ?
                        WHERE user_id = ?
                        ''', (height, user.id))
            connect.commit()
    except Exception as ex:
        print(f'Ошибка при записи роста в базу данных {ex}')
        return f"{ex}"
    finally:
        cursor.close()
    return True    

def set_user_gender(user, gender) -> str | bool:
    try:
        connect,cursor = connect_to_db()
        if connect is None or cursor is None:
            print("Ошибка: база данных отсутствует")
        else:
            cursor.execute(f'''
                UPDATE {NAME_CONST_TABLE_USERS}
                SET gender = ?
                WHERE user_id = ?
            ''', (gender, user.id))
            connect.commit()
    except Exception as ex:
        print(f'Ошибка при записи пола в базу данных {ex}')
        return f"{ex}"
    finally:
        cursor.close()
    return True