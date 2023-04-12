from concurrent import futures

import grpc

from gapp.gen import hello_pb2_grpc
from happ.services.grpc import hello_pb2
from gapp.repo.pg import Repository


class Greeter(hello_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.repo = Repository()

    def SayHello(self, request, context):
        print("received request from: " + request.name)
        self.repo.insert_hello(request.name)
        return hello_pb2.HelloReply(message='Hello ' + request.name)

    def SayGoodbye(self, request, context):
        print("received goodbye from: " + request.name)
        cnt = self.repo.count_hello(request.name)
        return hello_pb2.GoodbyeReply(message='Goodbye ' + request.name, hello_count=cnt)

    async def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        hello_pb2_grpc.add_GreeterServicer_to_server(self, server)
        server.start()
        print("Server started, listening on ")
        server.wait_for_termination()
