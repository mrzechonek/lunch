import uvicorn
from fastapi import FastAPI
from lunch import debug

app = FastAPI()


@app.get("/")
def topic():
    return "Być czy mieć?"


def run():
    uvicorn.run("lunch.main:app", reload=True, log_config=debug.LOGGING_CONFIG)
