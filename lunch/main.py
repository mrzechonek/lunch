import uvicorn
from alembic.command import upgrade
from alembic.config import Config
from fastapi import FastAPI
from lunch import debug
from pkg_resources import resource_filename

app = FastAPI()


@app.on_event("startup")
def migrations():
    config = Config(resource_filename("lunch", "alembic.ini"))
    upgrade(config, "head")


@app.get("/")
def topic():
    return "Być czy mieć?"


def run():
    uvicorn.run("lunch.main:app", reload=True, log_config=debug.LOGGING_CONFIG)
