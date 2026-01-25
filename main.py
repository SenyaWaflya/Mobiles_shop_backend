from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.database.database import create_tables, engine
from src.routers.product import router as product_router
from src.routers.user import router as user_router

swagger_ui_parameters = {'tryItOutEnabled': True, 'syntaxHighlight': {'activate': True, 'theme': 'nord'}}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    _ = app
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(title='Mobiles shop', swagger_ui_parameters=swagger_ui_parameters, lifespan=lifespan)

app.include_router(user_router)
app.include_router(product_router)


@app.get('/')
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse('/docs')
