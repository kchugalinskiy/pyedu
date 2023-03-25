from __future__ import print_function

import logging
import os

import grpc
from gen import *


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    host = os.environ.get('GRPC_HOST')
    port = os.environ.get('GRPC_PORT')
    with grpc.insecure_channel(host + ':' + port) as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
