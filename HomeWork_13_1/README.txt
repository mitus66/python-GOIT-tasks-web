1. Run Docker
docker-compose up --build

# .env
SECRET_KEY="your-secret-key"
DATABASE_URL="postgresql://postgres:postgres@db:5432/postgres"
MAIL_USERNAME="your-email@example.com"
MAIL_PASSWORD="your-email-password"
MAIL_FROM="your-email@example.com"
MAIL_PORT=587
MAIL_SERVER="smtp.example.com"
CLOUDINARY_CLOUD_NAME="your-cloud-name"
CLOUDINARY_API_KEY="your-api-key"
CLOUDINARY_API_SECRET="your-api-secret"
