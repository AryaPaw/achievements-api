# 🏆 Achievements API

## 📄 Описание

Achievements API - это RESTful API, разработанное с использованием FastAPI, для управления пользователями и их достижениями. API позволяет создавать пользователей и достижения, назначать достижения пользователям, а также предоставлять различную статистику по пользователям и их достижениям.

## 🚀 Установка и запуск

### Требования

- 🐳 Docker
- 🐳 Docker Compose

### Шаги для установки

1. **Клонируйте репозиторий:**

   ```sh
   git clone https://github.com/AryaPaw/achievements-api
   cd achievements-api
   ```

2. **Создайте файл `.env` в корне проекта с содержимым:**

   ```env
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=achievements_db
   POSTGRES_HOST=database
   POSTGRES_PORT=5432
   ```

3. **Запустите контейнеры с помощью Docker Compose:**

   ```sh
   docker-compose up -d --build
   ```

## 📚 API Документация

После запуска приложения, документация API будет доступна по следующим URL:

- 📄 Swagger UI: [http://localhost/docs](http://localhost/docs)
- 📘 ReDoc: [http://localhost/redoc](http://localhost/redoc)

## 📌 Эндпоинты API

### 👤 Пользователи

- **Создание пользователя**

  ```http
  POST /users/
  ```

  Тело запроса (JSON):
  ```json
  {
      "username": "testuser",
      "language": "en"
  }
  ```

- **Получение всех пользователей**

  ```http
  GET /users/
  ```

### 🏅 Достижения

- **Создание достижения**

  ```http
  POST /achievements/
  ```

  Тело запроса (JSON):
  ```json
  {
      "name": "First Achievement",
      "points": 10,
      "description": "This is the first achievement."
  }
  ```

- **Получение всех достижений**

  ```http
  GET /achievements/
  ```

### 👥 Достижения пользователей

- **Назначение достижения пользователю**

  ```http
  POST /user-achievements/
  ```

  Тело запроса (JSON):
  ```json
  {
      "user_id": 1,
      "achievement_id": 1
  }
  ```

- **Получение достижений пользователя**

  ```http
  GET /users/{user_id}/achievements/
  ```

### 📊 Статистика

- **Пользователь с максимальным количеством достижений**

  ```http
  GET /statistics/max-achievements
  ```

- **Пользователь с максимальным количеством очков достижений**

  ```http
  GET /statistics/max-points
  ```

- **Пользователи с максимальной разностью очков достижений**

  ```http
  GET /statistics/max-point-difference
  ```

- **Пользователи с минимальной разностью очков достижений**

  ```http
  GET /statistics/min-point-difference
  ```

- **Пользователи, у которых достижения выдавались 7 дней подряд**

  ```http
  GET /statistics/consistent-achievements
  ```

## 📂 Структура проекта

```plaintext
.
├── .env
├── docker-compose.yml
├── backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   └── healthcheck.sh
├── nginx
│   └── nginx.conf
```

## 👑 Автор

- AryaPaw