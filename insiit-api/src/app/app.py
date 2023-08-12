from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from app.auth.key import get_api_key
from config import api_config


def create_app() -> FastAPI:
    app = FastAPI()
    origins = [
        f"{value['host']}:{value['port']}"
        for _key, value in api_config["origins"].items()
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


@app.get("/")
async def root(api_key: str = Security(get_api_key)):
    print("route:", api_key)
    return {"message": "hello world"}
