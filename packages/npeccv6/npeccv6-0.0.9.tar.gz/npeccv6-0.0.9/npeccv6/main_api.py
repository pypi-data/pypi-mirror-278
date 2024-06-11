from fastapi import FastAPI
from model_func import create_model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/create_model/{name}")
def create_model_api(name: str):
    create_model(name)
