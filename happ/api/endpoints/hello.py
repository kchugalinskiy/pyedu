from fastapi import APIRouter, Depends
from happ.schemas import hello
from happ.services.grpc.hello_pb2_grpc import GreeterStub
from happ.deps import get_grpc_client
from happ.services.grpc import hello_pb2

router = APIRouter(prefix='/hello', tags=['Hello request'])


@router.post("/hello")
async def get_hello(item_in: hello.HelloRequest,
                    cli: GreeterStub = Depends(get_grpc_client)) -> hello.HelloResponse:
    print("rest: received request from: " + item_in.name)
    response = cli.SayHello(hello_pb2.HelloRequest(name=item_in.name))
    return {'message': response.message}


@router.post("/goodbye")
async def get_goodbye(item_in: hello.GoodbyeRequest,
                      cli: GreeterStub = Depends(get_grpc_client)) -> hello.GoodbyeResponse:
    print("received goodbye from: " + item_in.name)
    response: hello_pb2.GoodbyeReply = cli.SayHello(hello_pb2.GoodbyeRequest(name=item_in.name))
    return {'message': response.message, 'hello_count': 1}
