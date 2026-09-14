from fastapi import FastAPI
from Routers import product
from Routers import purchases
from Routers import users
from Database.db import Base, engine
from Database import tables
from Utils import cloudinary

app = FastAPI()
app.include_router(users.router)
app.include_router(product.router)
app.include_router(purchases.router)

@app.get('/')
async def index():
    return {'message':'Welcome to Lore'}

Base.metadata.create_all(bind=engine)