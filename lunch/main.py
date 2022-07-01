import uvicorn
from alembic.command import upgrade
from alembic.config import Config
from fastapi import Body, FastAPI
from lunch import database, debug
from pkg_resources import resource_filename
from sqlalchemy.sql import select

app = FastAPI()


@app.on_event("startup")
def migrations():
    config = Config(resource_filename("lunch", "alembic.ini"))
    upgrade(config, "head")


@app.get("/")
def topic():
    return "Być czy mieć?"


@app.get("/feed")
async def get_feed(db=database.DB):
    feeds = await db.execute(select(database.Feed))
    return [feed.url for feed, in feeds.all()]


def run():
    uvicorn.run("lunch.main:app", reload=True, log_config=debug.LOGGING_CONFIG)
