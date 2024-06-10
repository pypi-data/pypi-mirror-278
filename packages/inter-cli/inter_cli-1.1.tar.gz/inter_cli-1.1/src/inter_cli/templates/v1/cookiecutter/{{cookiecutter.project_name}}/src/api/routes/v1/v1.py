from fastapi import FastAPI
from api.routes.v1.predict.routes import router as predict_router


v1_app = FastAPI(title="Model prediction V1")

v1_app.include_router(predict_router)
