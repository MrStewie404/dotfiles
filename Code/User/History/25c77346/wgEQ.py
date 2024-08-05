import os
from pathlib import Path

from database_handler import BotDatabaseHandler


BASE_DIR = Path(__file__).resolve().parent

EXCEPTION_LOG = os.path.join(BASE_DIR, "exception.log")

Bot_DB = BotDatabaseHandler("data.db")

photo_path = "./data/default/"

BOT_TOKEN = "7171351515:AAE1i0kUje5wuLmvsf45DWaAqDNWq-gZOm4"


ADMINS = []



class PATTERNS:
    product = "<b>NAME</b>\nЦена: PRICE\n\nОписание: <pre>DESCRIPTION</pre>\n\nРейтинг: RATING"
    in_cart = "NAME  -  PRICE"

class TEXTS:
    START_MESSAGE = "<b>Сообщение - заглушка</b>"
    PRODUCTS = "Здесь представлены товары"

class ACTIONS:
    PRODUCTS = "PRODUCTS"
    CART = "CART"

    LEFT = "LEFT"
    POSITION = "POSITION" 
    RIGHT = "RIGHT"
    ADD_TO_CART = "ADD_TO_CART"

    CREATE_PRODUCT = "CREATE_PRODUCT"
    CHANGE_PRODUCT = "CHANGE_PRODUCT"
    GET_ORDERS = "GET_ORDERS"

class BUTTON_TEXTS:
    PRODUCTS = "Товары 📦"
    CART = "Корзина 🛒"
    
    LEFT = "<<"
    POSITION = "POSITION/LENGHT"
    RIGHT = ">>"
    ADD_TO_CART = "Добавить в корзину 🛒"

    CREATE_PRODUCT = "Создать товар 📦"
    CHANGE_PRODUCT = "Изменить товар ✍️"
    GET_ORDERS = "Список заказов 📦"
    


help = {
    'help': '/start - Старт\n/help - Помощь по командам'
}