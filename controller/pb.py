from concurrent import futures

import grpc

from gen import *
from repo.pg import Repository


class Greeter(hello_pb2_grpc.GreeterServicer):
    def __init__(self, host: str, port: str, repo: Repository):
        self.host = host
        self.port = port
        self.repo = repo

    def SayHello(self, request, context):
        print("received request from: " + request.name)
        self.repo.insert_hello(request.name)
        return hello_pb2.HelloReply(message='Hello ' + request.name)

    def SayGoodbye(self, request, context):
        print("received goodbye from: " + request.name)
        cnt = self.repo.count_hello(request.name)
        return hello_pb2.GoodbyeReply(message='Goodbye ' + request.name, hello_count=cnt)

    async def serve(self):
        port = self.port
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        hello_pb2_grpc.add_GreeterServicer_to_server(self, server)
        server.add_insecure_port('[' + self.host + ']:' + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
