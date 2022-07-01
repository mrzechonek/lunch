import asyncio
import logging
from contextlib import asynccontextmanager

import aiohttp
import feedparser
import uvicorn
from alembic.command import upgrade
from alembic.config import Config
from fastapi import Body, FastAPI
from fastapi.responses import RedirectResponse
from lunch import database, debug
from pkg_resources import resource_filename
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

app = FastAPI()


@app.on_event("startup")
def migrations():
    config = Config(resource_filename("lunch", "alembic.ini"))
    upgrade(config, "head")


@app.middleware("http")
async def request_id(request, next):
    with debug.request_id_context():
        response = await next(request)
        logging.debug("%s: %s", request.url, response.status_code)
        return response


@app.middleware("http")
async def db_session(request, next):
    async with database.db_session_context():
        return await next(request)


@app.get("/")
async def topic():
    cursor = await database.DB.session.execute(select(database.Topic).order_by(func.random()))
    try:
        (topic,) = cursor.first()
    except TypeError:
        return "Być czy mieć?"
    else:
        return topic.title


@app.get("/feed")
async def get_feed():
    cursor = await database.DB.session.execute(select(database.Feed))
    return [feed.url for feed, in cursor.all()]


async def find_topics(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = feedparser.parse(await response.text())
        topics = [entry["title"] for entry in data["entries"]]

        async with database.db_session_context() as db:
            await database.DB.session.execute(
                insert(database.Topic)
                .values([[topic] for topic in topics])
                .on_conflict_do_nothing()
            )

        logging.info("TOPICS: %s", topics)


@app.post("/feed")
async def post_feed(url: str = Body(...)):
    logging.info("FEED: %s", url)

    await database.DB.session.execute(insert(database.Feed).values([url]).on_conflict_do_nothing())
    await database.DB.session.commit()

    asyncio.create_task(find_topics(url))
    return RedirectResponse(app.url_path_for("get_feed"))


def run():
    uvicorn.run("lunch.main:app", reload=True, log_config=debug.LOGGING_CONFIG)
