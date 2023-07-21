from dotenv import load_dotenv
import os

from .menu import Menu
from .submenu import SubMenu
from .dish import Dish

load_dotenv()


db_url = os.getenv("DATABASE_URL")


