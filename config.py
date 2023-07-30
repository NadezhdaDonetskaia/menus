import os
from dotenv import load_dotenv


load_dotenv()


db_url = os.getenv("DATABASE_URL")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

db_url_test = os.getenv("DB_USER_TEST")

DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DB_USER_TEST")
DB_HOST_TEST = os.getenv("DB_USER_TEST")
DB_PORT_TEST = os.getenv("DB_USER_TEST")
DB_NAME_TEST = os.getenv("DB_USER_TEST")