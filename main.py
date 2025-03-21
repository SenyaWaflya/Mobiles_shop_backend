from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.database.database import engine, create_tables
from src.services.admin import AdminService
from src.routers.user import router as user_router
from src.routers.product import router as product_router
from src.routers.admin import router as admin_router


swagger_ui_parameters = {
    'tryItOutEnabled': True,
    'syntaxHighlight': {
        'activate': True,
        'theme': 'nord'
    }
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await AdminService.init_superuser()
    yield
    await engine.dispose()


app = FastAPI(title='Mobiles shop', swagger_ui_parameters=swagger_ui_parameters, lifespan=lifespan)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(admin_router)


@app.get('/')
def redirect_to_docs():
    return RedirectResponse('/docs')
