from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.database.connection import create_tables, engine
from src.routers.products import router as products_router
from src.routers.users import router as users_router

swagger_ui_parameters = {'tryItOutEnabled': True, 'syntaxHighlight': {'activate': True, 'theme': 'nord'}}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    _ = app
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(title='Mobiles shop', swagger_ui_parameters=swagger_ui_parameters, lifespan=lifespan)

app.include_router(users_router)
app.include_router(products_router)


@app.get('/')
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse('/docs')
