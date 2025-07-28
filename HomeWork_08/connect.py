from mongoengine import connect
import os

# Важливо: Замініть YOUR_USERNAME, YOUR_PASSWORD, YOUR_CLUSTER_URL та YOUR_DB_NAME на ваші реальні дані з MongoDB Atlas.
# Отримайте URL підключення з змінної оточення або встановіть за замовчуванням
# Рекомендується використовувати змінні оточення для конфіденційних даних
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://mitus66:Alaska725@cluster0.qzzbjox.mongodb.net/?retryWrites=true&w=majority")

def connect_db():
    """Встановлює з'єднання з базою даних MongoDB Atlas."""
    try:
        connect(host=MONGO_URI)
        print("Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        # Можна додати sys.exit(1) тут, якщо з'єднання є критичним
