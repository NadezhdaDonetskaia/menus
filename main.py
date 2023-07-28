from fastapi import FastAPI

from routes import menu_router, sub_menu_router, dish_router

app = FastAPI()

app.include_router(menu_router)
app.include_router(sub_menu_router)
app.include_router(dish_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
