from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routers import product
from Routers import purchases
from Routers import login
from Routers import users
from Database.db import Base, engine
from Database import tables
from Utils import cloudinary

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lore-gilt-one.vercel.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(product.router)
app.include_router(purchases.router)
app.include_router(login.router)

@app.get('/')
async def index():
    return {'message':'Welcome to Lore'}

Base.metadata.create_all(bind=engine)
