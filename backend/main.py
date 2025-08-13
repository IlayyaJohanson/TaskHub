from fastapi import FastAPI
from modules import config, db
from modules.auth import router as auth_router

# Создание таблиц (на старте, пока без Alembic)
db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(
    title="TaskHub API",
    description="Backend API для веб и мобильного приложения TaskHub",
    version="0.1.0",
)

# Подключаем роуты
app.include_router(auth_router)


# Заглушки для остальных модулей
@app.get("/")
def root():
    return {"message": "TaskHub API is running"}


# Пример будущих модулей
# from modules.users import router as users_router
# app.include_router(users_router)
