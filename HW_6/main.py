# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
# - Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# - Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# - Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
# > Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
# > Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# > Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.

import uvicorn
import products
import orders
import home
from db import database
from fastapi import FastAPI

import users

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(orders.router, tags=["orders"])
app.include_router(home.router, tags=["home"])
    

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
