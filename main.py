from fastapi import FastAPI

from models.database import engine, Base

from routers.user_router import router as user_router
from routers.product_router import router as product_router


app = FastAPI(title='Mobiles shop')

app.include_router(user_router)
app.include_router(product_router)

Base.metadata.create_all(bind=engine)
