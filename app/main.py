from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.database import engine, Base
from app.api import routes
from app.init_db import init_db
import os

app = FastAPI(title="Event Management System", version="1.0")

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Заполнение тестовыми данными
init_db()

# Подключаем API роутер
app.include_router(routes.router, prefix="/api/v1")

# Статика
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Корневой маршрут
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>Файл static/index.html не найден</h1>", status_code=404)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
