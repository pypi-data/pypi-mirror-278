from fastapi import FastAPI
from api.routes.v1.v1 import v1_app
from api.routes.health.routes import router as health_router


app = FastAPI(docs_url=None, redoc_url=None)


app.mount("/api/v1/", v1_app)
app.include_router(health_router)
