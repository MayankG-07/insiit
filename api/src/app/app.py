from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
from app.auth.key import get_api_key
from config import api_config

origins = [
    f"{value['host']}:{value['port']}" for _key, value in api_config["origins"].items()
]


def create_app():
    app = FastAPI()
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
async def root(api_key: APIKey = Depends(get_api_key)):
    return {"message": "hello world"}


from app.routes import outletRoutes
