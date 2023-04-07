from fastapi import Depends, FastAPI
from repo.pg import Repository
from pydantic import BaseModel
import uvicorn

app = FastAPI()
g_repo = Repository


def get_db():
    return g_repo


class Rest:
    def __init__(self, port: int, repo):
        self.port = port
        global g_repo
        g_repo = repo

    async def serve(self):
        config = uvicorn.Config("controller.rest:app", port=self.port, log_level="info")
        server = uvicorn.Server(config)
        config.setup_event_loop()
        await server.serve()

    def run(self):
        config = uvicorn.Config("controller.rest:app", port=self.port, log_level="info")
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


@app.post("/items/")
async def create_item(item: Item):
    return item
