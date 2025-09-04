# PROJECT CONTEXT

## 1. Общая концепция

**Название проекта:** TaskHub
**Краткое описание:** Веб-сервис и мобильное приложение для управления задачами и проектами с поддержкой ролей пользователей, статусов, тегов, уведомлений и аналитики.
**Пример пользовательского сценария:**
Менеджер создаёт проект, добавляет задачи, назначает исполнителей. Исполнители видят свои задачи, обновляют статусы, прикрепляют файлы. Менеджер получает уведомления о прогрессе и может сформировать отчёт. Пользователь может работать как через браузер, так и через мобильное приложение (Android/iOS), сохраняя единый опыт.

---

## 2. Архитектура

**Описание общей структуры:**

- **Frontend Web:** React + Tailwind CSS + React Query
- **Frontend Mobile:** React Native + Tailwind for RN + React Query
- **Backend:** Python (FastAPI)
- **Database:** PostgreSQL
- **Слои backend:**
  - API (FastAPI endpoints)
  - Business Logic (сервисы)
  - Data Layer (SQLAlchemy ORM)
  - Notifications (email/websocket)

**Принципы:**

- Модульная архитектура
- REST API
- JWT авторизация
- Event-driven уведомления
- **Изоляция модулей** — взаимодействие только через API или сервисный слой
- **Единый API** для веб- и мобильного приложения
- **Повторное использование логики API-запросов** в веб и мобайле

---

## 3. Структура базы данных (минимум для старта)

**Таблицы:**

- **users**
  - id (SERIAL, PK)
  - username (VARCHAR, unique)
  - email (VARCHAR, unique)
  - password_hash (VARCHAR)
  - role (ENUM: admin, manager, user)
  - created_at (TIMESTAMP)
- **projects**
  - id (SERIAL, PK)
  - name (VARCHAR)
  - description (TEXT)
  - owner_id (FK → users.id)
  - created_at (TIMESTAMP)
- **tasks**
  - id (SERIAL, PK)
  - project_id (FK → projects.id)
  - title (VARCHAR)
  - description (TEXT)
  - status (ENUM: todo, in_progress, done)
  - assignee_id (FK → users.id, nullable)
  - due_date (DATE)
  - created_at (TIMESTAMP)

---

## 4. API (первый набор)

[POST] /auth/register
Описание: Регистрация пользователя
Параметры (JSON): username, email, password
Ответ: { "id": 1, "username": "john" }

[POST] /auth/login
Описание: Авторизация, выдача JWT токена
Параметры: email, password
Ответ: { "access_token": "..." }

[GET] /auth/me
Описание: Получение информации о текущем пользователе
Параметры: JWT токен
Ответ:

```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "created_at": "2025-09-01T12:00:00Z"
}

[GET] /projects
Описание: Список проектов пользователя
Параметры: JWT токен
Ответ: [ { "id": 1, "name": "Project A" } ]

---

## 5. Глобальные переменные и константы

| Имя             | Тип | Значение по умолчанию | Описание                   |
| --------------- | --- | --------------------- | -------------------------- |
| JWT_SECRET      | str | dev_secret_key        | Секрет для подписи токенов |
| JWT_EXPIRE_DAYS | int | 7                     | Срок действия токена       |
| JWT_ALG         | str | HS256                 | Алгоритм подписи JWT       |
| DB_URL          | str | postgres://...        | Подключение к БД           |

---

## 6. Существующие классы и объекты

- modules/models.py
  - User
  - Project
  - Task
- modules/schemas.py (Pydantic-схемы)
  - UserCreate, UserLogin, UserRead
  - Token

---

## 7. Форматы данных

- **Формат даты:** `YYYY-MM-DD`
- **Время:** `YYYY-MM-DDTHH:MM:SSZ`
- **Кодировка:** UTF-8
- **JSON-ответы:** все ответы содержат ключ `data` или `error`

---

## 8. Текущий список модулей

| Модуль          | Файл/папка            | Описание                                                             | Взаимодействие |
| --------------- | --------------------- | -------------------------------------------------------------------- | -------------- |
| auth            | modules/auth.py       | Регистрация, логин, токены, сброс пароля                             | Только API     |
| users           | modules/users.py      | Управление профилями пользователей, смена роли                       | Только API     |
| projects        | modules/projects.py   | CRUD для проектов                                                    | Только API     |
| tasks           | modules/tasks.py      | CRUD для задач                                                       | Только API     |
| comments        | modules/comments.py   | Комментарии к задачам и проектам                                     | Только API     |
| notifications   | modules/notify.py     | Email, WebSocket уведомления                                         | Только API     |
| reports         | modules/reports.py    | Генерация отчётов по проектам/задачам                                | Только API     |
| tags            | modules/tags.py       | Метки для задач и проектов                                           | Только API     |
| files           | modules/files.py      | Загрузка/хранение вложений                                           | Только API     |
| calendar        | modules/calendar.py   | Календарный вид задач, интеграция с внешними календарями             | Только API     |
| activity        | modules/activity.py   | Журнал действий (аудит лог)                                          | Только API     |
| search          | modules/search.py     | Поиск по задачам, проектам, комментариям                             | Только API     |
| db              | modules/db.py         | Подключение к БД, миграции                                           | Сервисный слой |
| config          | modules/config.py     | Глобальные настройки                                                 | Сервисный слой |
| utils           | modules/utils.py      | Утилиты, хелперы                                                     | Сервисный слой |
| middleware      | modules/middleware.py | Логирование, обработка ошибок, CORS, rate-limiting                   | Сервисный слой |
| frontend_web    | frontend/web/         | Веб-фронтенд на React + Tailwind CSS + React Query                   | Через API      |
| frontend_mobile | frontend/mobile/      | Мобильное приложение на React Native + Tailwind for RN + React Query | Через API      |

⚠️ На текущем этапе реализованы только базовые модули backend и минимальный веб-фронтенд:

- main.py — точка входа FastAPI.
- modules/config.py — глобальные настройки, загрузка .env.
- modules/db.py — подключение к PostgreSQL и база SQLAlchemy.
- modules/auth.py — регистрация, логин, JWT.
- modules/models.py — модели (User, Project, Task, пока только базовый каркас).
- modules/schemas.py — Pydantic-схемы (UserCreate, UserRead и др., пока только для auth).
- alembic.ini и migrations/ — миграции БД.
- requirements.txt — зависимости backend.
- frontend/web/ — минимальный фронтенд на React (Vite).

---

## 10. Структура фронтенда

### 10.1 Веб-фронтенд (`frontend_web`)

**Технологический стек:**

- React 18
- Tailwind CSS
- React Query (работа с API)
- React Router (навигация)
- Axios (запросы к API)

**Структура директорий:**

⚠️ На текущем этапе фронтенд-web представлен минимальным шаблоном Vite+React:

frontend/web/
│ package.json, package-lock.json, vite.config.js, index.html
│ .gitignore, README.md, eslint.config.js
│
├─ public/             # статические файлы (favicon, иконки и пр.)
└─ src/
   │ App.jsx           # UI регистрации/логина, кнопка Who am I?
   │ App.css           # кастомные стили
   │ main.jsx          # точка входа React
   │ index.css         # Tailwind base
   │ api.js            # функции register/login/me через Axios
   └─ assets/          # картинки/иконки

Структура с pages/components/hooks пока не реализована, весь функционал в App.jsx.

**Подключение к API:**

- Все запросы выполняются через src/api.js с использованием Axios (в дальнейшем планируется вынести в src/api/ и подключить React Query).
- API-адрес хранится в `.env`.

---

### 10.2 Мобильное приложение (`frontend_mobile`)

**Технологический стек:**

- React Native (Expo)
- Tailwind for RN (`nativewind`)
- React Query (работа с API)
- React Navigation (навигация между экранами)
- Axios (запросы к API)

**Структура директорий:**
frontend/mobile/
│ package.json
│ app.json
│ babel.config.js
│
└─ src/
├─ api/ # Логика API-запросов
├─ components/ # UI-компоненты
├─ screens/ # Экраны приложения
├─ hooks/ # Кастомные хуки
├─ store/ # Глобальное состояние (если потребуется)
├─ App.js # Главный компонент приложения

**Подключение к API:**

- Логика API полностью повторяет веб-версию (повторное использование кода возможно через общий пакет).
- Конфигурация API-адреса в `.env`.

---

**Общие принципы для фронтенда:**

- Веб и мобайл используют **один и тот же REST API** из backend.
- UI строится по единой дизайн-системе (одинаковые цвета, шрифты, размеры).
- Логика API-запросов и модели данных максимально переиспользуются между веб и мобайлом.
- Все изменения в API backend должны отражаться одновременно в веб и мобайл.

---

## 11. Стартовый шаблон фронтенда

### 11.1 Веб-фронтенд (`frontend_web`)

Минимальный рабочий проект React + Tailwind + React Query.
Файлы:

- `package.json` — зависимости и скрипты
- `tailwind.config.js` — конфигурация Tailwind
- `src/main.jsx`, `src/App.jsx`, `src/index.css` — точка входа и базовая страница

Стартовый шаблон дополнен файлами api.js (Axios-запросы), App.css (стили), vite.config.js, .gitignore, README.md, eslint.config.js.

Подключение API реализовано через api.js, где определены функции register, login, me.

---

## 9. История изменений проекта

- **2025-08-11:** Создан базовый контекст проекта TaskHub
- **2025-08-11:** Добавлен расширенный список модулей с описанием и принципом изоляции
- **2025-08-11:** Добавлены модули фронтенда (Web и Mobile) и выбран единый стек
- **2025-08-11:** Добавлен раздел "Структура фронтенда" с шаблоном для React и React Native
- **2025-08-13:** Реализован базовый backend на FastAPI, добавлены файлы `config.py` и `db.py`, создан модуль `auth` (регистрация, логин, JWT), добавлен `main.py` для подключения роутов.
- **2025-08-28:** Настроен и установлен PostgreSQL, создан пользователь и БД `taskhub`.
  Backend успешно подключается к БД, таблицы создаются через SQLAlchemy.
  Файлы `main.py`, `config.py`, `db.py`, `auth.py` приведены в рабочее состояние, проект стартует через `uvicorn`.
- **2025-09-03:** Вынесены модели User, Project, Task из auth.py в modules/models.py. Добавлен modules/schemas.py с Pydantic-схемами для регистрации, логина и чтения пользователей.  Интегрирован Alembic для управления миграциями: добавлены migrations/env.py и alembic.ini. Добавлена команда alembic revision --autogenerate для первичной схемы БД.
- **2025-09-04:** Настроен CORS в backend/main.py под Vite-разработку (http://localhost:5173).
Добавлены .env файлы в backend и frontend/web для конфигурации DB_URL, JWT_SECRET и VITE_API_URL. Модули config.py и dotenv подключают переменные окружения. Реализовано демо аутентификации на фронтенде:
• frontend/web/src/api.js — регистрация, логин, получение /auth/me.
• frontend/web/src/App.jsx — формы для register/login, хранение токена в localStorage, кнопка “Who am I?”.



```
