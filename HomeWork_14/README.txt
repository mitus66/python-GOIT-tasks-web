1. Run Docker
docker-compose up --build

2. pip install sphinx sphinx-rtd-theme

3. sphinx-quickstart docs

Гаразд, продовжимо! Це чудове завдання, оскільки воно охоплює важливі аспекти розробки, такі як документація та тестування.  Ось покроковий план, як це зробити.

1. Документація за допомогою Sphinx
Sphinx — це потужний інструмент для автоматичного створення документації з коду, використовуючи docstrings.

Крок 1: Встановлення Sphinx
Спочатку додайте Sphinx та необхідні розширення до вашого requirements.txt або встановіть їх у віртуальне середовище.

Bash

pip install sphinx sphinx-rtd-theme sphinx-autodoc
Крок 2: Додавання Docstrings
Додайте docstrings (рядки документації) до ваших функцій, методів та класів. Sphinx може використовувати різні формати, але reStructuredText є стандартним.

Приклад формату reStructuredText:

Python

# auth.py

def get_current_user(token: str, db: Session) -> User:
    """Отримує поточного користувача на основі токена.

    :param token: JWT токен.
    :type token: str
    :param db: Сесія бази даних.
    :type db: Session
    :raises HTTPException: Якщо токен недійсний.
    :return: Об'єкт користувача.
    :rtype: User
    """
    # ... ваша логіка
Обов'язково додайте docstrings до всіх основних функцій у модулях, які ви хочете задокументувати (наприклад, auth.py, repository/contacts.py, routes/users.py).

Крок 3: Налаштування Sphinx
Створіть файл docs/source/conf.py. У ньому потрібно налаштувати шлях до вашого проєкту.

Python

# docs/source/conf.py

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))
Далі в conf.py додайте sphinx.ext.autodoc до розширень:

Python

# docs/source/conf.py

extensions = [
    'sphinx.ext.autodoc',
    # ... інші розширення
]
Крок 4: Генерація документації
Використовуйте команду sphinx-apidoc, щоб автоматично створити файли .rst з вашого коду.

Bash

# Знаходиться у корені проєкту
sphinx-apidoc -o docs/source/ .
Потім увійдіть в папку docs і згенеруйте HTML-документацію:

Bash

cd docs
make html
Документація буде створена в папці docs/_build/html.

2. Модульні тести за допомогою Unittest
Unittest — це стандартний фреймворк для модульного тестування в Python. Він ідеально підходить для тестування окремих функцій репозиторію.

Крок 1: Створення файлу тесту
Створіть папку tests/ і в ній файл, наприклад, test_contacts_repository.py.

Крок 2: Налаштування тестового середовища
Вам знадобиться мок-об'єкт (mock) для сесії бази даних, оскільки ви не хочете підключатися до реальної БД під час тестування.

Python

# tests/test_contacts_repository.py

import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.repository.contacts import create_contact, get_contacts
# ... імпорт інших функцій, які потрібно протестувати

class TestContactsRepository(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)

    def test_create_contact(self):
        body = MagicMock()
        user = MagicMock()

        result = create_contact(body=body, user=user, db=self.db)

        self.assertEqual(result.first_name, body.first_name)
        self.assertTrue(hasattr(result, "id"))

    def test_get_contacts(self):
        # ... напишіть тест для функції get_contacts
        pass

# Запуск тестів
if __name__ == '__main__':
    unittest.main()
Ці тести перевіряють, чи повертає функція create_contact об'єкт з коректними атрибутами.

3. Функціональні тести за допомогою Pytest
Pytest — більш гнучкий і сучасний фреймворк для тестування, що ідеально підходить для тестування маршрутів FastAPI.

Крок 1: Встановлення Pytest
Встановіть необхідні бібліотеки:

Bash

pip install pytest pytest-asyncio TestClient
Крок 2: Створення файлу тесту
Створіть файл tests/test_main.py та використайте TestClient від FastAPI.

Python

# tests/test_main.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_users_avatar():
    # Цей тест буде складнішим, бо потребує аутентифікації.
    # Вам потрібно буде згенерувати токен, щоб його використовувати у заголовках.
    headers = {"Authorization": "Bearer <YOUR_VALID_TOKEN>"}
    response = client.patch("/users/avatar", headers=headers, json={"avatar": "http://new-avatar.com/image.jpg"})

    # ... додайте перевірки на статус-код та дані у відповіді
    assert response.status_code == 200
    assert "avatar" in response.json()
Крок 3: Запуск тестів
Запускайте тести командою у терміналі:

Bash

pytest
Виконавши ці кроки, ви створите міцну основу для надійного та задокументованого REST API. Який з цих пунктів ви хочете почати реалізовувати першим?