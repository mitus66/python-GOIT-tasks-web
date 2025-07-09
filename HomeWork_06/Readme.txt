Інструкції для запуску create_and_populate_db.py:

1. Встановіть бібліотеку Faker, якщо ви ще цього не зробили:

Bash
pip install Faker

python create_and_populate_db.py

Це створить файл university.db у тому ж каталозі.
_________________________________________________________
2. Запустіть программу DBeaver і виконайте запити до бази даних
_________________________________________________________
або
3. Виконати запити SQL через термінал SQLite:

Відкрийте термінал і перейдіть до каталогу, де знаходиться university.db.

Запустіть SQLite CLI: sqlite3 university.db

Виконайте команду: .read query_1.sql (замініть query_1.sql на потрібний файл запиту).

Щоб вийти: .quit
_________________________________________________________
або
4. Виконати запити SQL через Python-скрипт:

import sqlite3

def execute_query(query_file):
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    with open(query_file, 'r', encoding='utf-8') as f:
        sql_query = f.read()

    print(f"\n--- Executing {query_file} ---")
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # Виведення заголовків (якщо вони доступні)
    if cursor.description:
        headers = [description[0] for description in cursor.description]
        print(headers)

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    # Переконайтеся, що university.db вже створено та заповнено
    for i in range(1, 11):
        execute_query(f"query_{i}.sql")
