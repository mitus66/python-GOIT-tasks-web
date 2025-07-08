import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta


def create_database():
    """Створює таблиці в базі даних."""
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            group_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            grade INTEGER NOT NULL,
            grade_date DATE NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            CHECK (grade >= 0 AND grade <= 100)
        );
    ''')

    conn.commit()
    conn.close()
    print("Database tables created successfully.")


def populate_database(num_students=40, num_groups=3, num_teachers=4, num_subjects=7):
    """Заповнює базу даних випадковими даними."""
    fake = Faker('uk_UA')  # Використовуємо українську локаль для імен
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    # Заповнення груп
    group_ids = []
    for i in range(num_groups):
        group_name = f"Group {chr(65 + i)}"  # Group A, Group B, etc.
        cursor.execute("INSERT INTO groups (name) VALUES (?)", (group_name,))
        group_ids.append(cursor.lastrowid)
    print(f"Populated {num_groups} groups.")

    # Заповнення викладачів
    teacher_ids = []
    for _ in range(num_teachers):
        teacher_name = fake.name()
        cursor.execute("INSERT INTO teachers (fullname) VALUES (?)", (teacher_name,))
        teacher_ids.append(cursor.lastrowid)
    print(f"Populated {num_teachers} teachers.")

    # Заповнення предметів
    subject_ids = []
    subject_names = [
        "Математика", "Фізика", "Хімія", "Історія", "Література",
        "Програмування", "Економіка", "Біологія"
    ]
    random.shuffle(subject_names)  # Перемішуємо, щоб брати випадкові назви

    for i in range(num_subjects):
        subject_name = subject_names[i]
        teacher_id = random.choice(teacher_ids)
        cursor.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", (subject_name, teacher_id))
        subject_ids.append(cursor.lastrowid)
    print(f"Populated {num_subjects} subjects.")

    # Заповнення студентів
    student_ids = []
    for _ in range(num_students):
        student_name = fake.name()
        group_id = random.choice(group_ids)
        cursor.execute("INSERT INTO students (fullname, group_id) VALUES (?, ?)", (student_name, group_id))
        student_ids.append(cursor.lastrowid)
    print(f"Populated {num_students} students.")

    # Заповнення оцінок
    for student_id in student_ids:
        # Кожен студент отримує оцінки з випадкової кількості предметів (від 1 до num_subjects)
        num_subjects_for_student = random.randint(1, num_subjects)
        subjects_for_student = random.sample(subject_ids, num_subjects_for_student)

        for subject_id in subjects_for_student:
            # До 20 оцінок для кожного студента з кожного предмета
            num_grades = random.randint(1, 20)
            for _ in range(num_grades):
                grade = random.randint(60, 100)  # Оцінки від 60 до 100

                # Випадкова дата оцінки за останній рік
                grade_date = fake.date_between(start_date='-1y', end_date='today').isoformat()

                cursor.execute(
                    "INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (?, ?, ?, ?)",
                    (student_id, subject_id, grade, grade_date)
                )
    print("Populated grades for students.")

    conn.commit()
    conn.close()
    print("Database populated successfully.")


if __name__ == "__main__":
    create_database()
    populate_database()

