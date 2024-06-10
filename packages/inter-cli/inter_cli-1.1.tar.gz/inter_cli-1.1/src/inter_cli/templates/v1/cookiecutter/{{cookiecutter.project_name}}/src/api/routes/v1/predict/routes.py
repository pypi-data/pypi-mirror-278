from fastapi import APIRouter, status
from api.routes.v1.predict.schemas import responses
from api.routes.v1.predict.schemas import requests
from contextlib import asynccontextmanager
import pathlib
import pickle as pkl

ml_model = {}


@asynccontextmanager
async def lifespan(router: APIRouter):
    current_path = pathlib.Path(__file__).resolve()
    with open(f"{current_path}../../../artifacts/model.pkl", "rb") as model:
        ml_model["model"] = pkl.load(model)
    yield


router = APIRouter(prefix="/predict", tags=["predict"], lifespan=lifespan)


@router.get(path="/inference", status_code=status.HTTP_200_OK)
async def predict(request: requests.PredictRequest) -> responses.PredictResponse:
    # model = ml_model.get("model")
    pass
