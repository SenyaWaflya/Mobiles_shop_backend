from fastapi import FastAPI

from models.database import engine, Base

from routers.user_router import router as user_router
from routers.product_router import router as product_router


swagger_ui_parameters = {
    'tryItOutEnabled': True,
    'syntaxHighlight': {
        'activate': True,
        'theme': 'nord'
    }
}

app = FastAPI(title='Mobiles shop', swagger_ui_parameters=swagger_ui_parameters)

app.include_router(user_router)
app.include_router(product_router)

Base.metadata.create_all(bind=engine)
