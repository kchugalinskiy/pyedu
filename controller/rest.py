from typing import Annotated
from fastapi import Depends, FastAPI
from repo.pg import Repository
from pydantic import BaseModel
import uvicorn

app = FastAPI()
g_repo = Repository


def get_db():
    return g_repo


async def serve(port: int, repo):
    global g_repo
    g_repo = repo
    config = uvicorn.Config("controller.rest:app", host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    config.setup_event_loop()
    await server.serve()


def run(port: int, repo):
    global g_repo
    g_repo = repo
    config = uvicorn.Config("controller.rest:app", host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()


class HelloRequest(BaseModel):
    name: str


class HelloResponse(BaseModel):
    message: str


class GoodbyeRequest(BaseModel):
    name: str


class GoodbyeResponse(BaseModel):
    message: str
    hello_count: int | None = None


@app.post("/hello", response_model=HelloResponse)
async def hello(request: HelloRequest, repo: Repository = Depends(get_db)) -> HelloResponse:
    print("rest: received request from: " + request.name)
    repo.insert_hello(request.name)
    return HelloResponse(message='Hello ' + request.name)


@app.post("/goodbye", response_model=GoodbyeResponse)
async def goodbye(request: GoodbyeRequest, repo: Repository = Depends(get_db)) -> GoodbyeResponse:
    print("received goodbye from: " + request.name)
    cnt = repo.count_hello(request.name)
    return GoodbyeResponse(message='Goodbye ' + request.name, hello_count=cnt)


class Item(BaseModel):
    name: str


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100, name: str = ""):
    return {"q": q, "skip": skip, "limit": limit, "name": name}


@app.post("/items/")
async def create_item(item: Item, commons: Annotated[dict, Depends(common_parameters)]):
    print(commons)
    return item
