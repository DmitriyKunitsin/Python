import sqlite3

import os

if os.path.exists("bot_database.db"):
    os.remove("bot_database.db")

connect = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = connect.cursor()
    
# Таблица с пользователем   
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, -- уникальный Telegram ID пользователя
    username TEXT,                        -- имя пользователя (@username)
    first_name TEXT,                      -- имя
    last_name TEXT,                       -- фамилия
    full_name TEXT,                       -- полное имя (можно формировать из first_name + last_name)
    language_code TEXT,                   -- язык пользователя
    is_bot BOOLEAN DEFAULT 0,             -- флаг, является ли пользователь ботом
    is_premium_activeted BOOLEAN DEFAULT 1, -- Флаг, является ли пользователь премиум подписчиком
    height_user REAL,                   -- Рост пользователя
    weight_user REAL,                   --- Вес пользователя
    IWM_user REAL,                      -- ИМТ пользователя
    age_user INTEGER CHECK(age > 0 AND age < 100),-- Возраст пользователя
    email TEXT UNIQUE,                  -- Email пользователя ( только уникальный )
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- дата и время добавления пользователя в БД
)
''')
connect.commit()

# Таблица программы конкретного пользователя
cursor.execute(
    '''
    CREATE TABLE trainings (
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
    '''
    CREATE TABLE workouts (
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
CREATE INDEX idx_trainings_user_id ON workouts(training_id);

    '''
)
connect.commit()

def add_or_update_user(user):
    cursor.execute('''
        INSERT INTO users(user_id, username, first_name, last_name,full_name)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username,
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            full_name=excluded.full_name
    ''', (user.id, user.username, user.first_name, user.last_name, user.full_name))
    connect.commit()

def get_user_data(user_id: int) -> str | None:
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return row if row else None