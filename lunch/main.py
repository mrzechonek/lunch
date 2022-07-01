import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def topic():
    return "Być czy mieć?"


def run():
    uvicorn.run("lunch.main:app", reload=True)
