from typing import Annotated, Optional
from fastapi import Depends, FastAPI

from gen import hello_pb2
from gen.hello_pb2_grpc import GreeterStub
from pydantic import BaseModel
import uvicorn

app = FastAPI()
g_greeter = GreeterStub


def get_grpc_client():
    return g_greeter


async def serve(port: int, greeter):
    global g_greeter
    g_greeter = greeter
    config = uvicorn.Config("controller.rest:app", host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    config.setup_event_loop()
    await server.serve()


def run(port: int, greeter):
    global g_greeter
    g_greeter = greeter
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
    hello_count: Optional[int]


@app.post("/hello", response_model=HelloResponse)
async def hello(request: HelloRequest,  cli: GreeterStub = Depends(get_grpc_client)) -> HelloResponse:
    print("rest: received request from: " + request.name)
    response = cli.SayHello(hello_pb2.HelloRequest(name=request.name))
    return HelloResponse(message=response.message)


@app.post("/goodbye", response_model=GoodbyeResponse)
async def goodbye(request: GoodbyeRequest, cli: GreeterStub = Depends(get_grpc_client)) -> GoodbyeResponse:
    print("received goodbye from: " + request.name)
    response = cli.SayGoodbye(hello_pb2.HelloRequest(name=request.name))
    return GoodbyeResponse(message=response.message, hello_count=response.hello_count)


