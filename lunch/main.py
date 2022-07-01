import uvicorn
from alembic.command import upgrade
from alembic.config import Config
from fastapi import Body, FastAPI
from fastapi.responses import RedirectResponse
from lunch import database, debug
from pkg_resources import resource_filename
from sqlalchemy.dialects.sqlite import insert
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


@app.post("/feed")
async def post_feed(db=database.DB, url: str = Body(...)):
    await db.execute(insert(database.Feed).values([url]).on_conflict_do_nothing())
    await db.commit()
    return RedirectResponse(app.url_path_for("get_feed"))


def run():
    uvicorn.run("lunch.main:app", reload=True, log_config=debug.LOGGING_CONFIG)
