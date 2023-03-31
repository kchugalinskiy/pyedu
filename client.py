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
        stub.SayHello(hello_pb2.HelloRequest(name='Вася'))
        response = stub.SayGoodbye(hello_pb2.GoodbyeRequest(name='Вася'))
        print("Greeter client received: " + response.message)
        if response.hello_count == 0:
            print("User is impolite!")
        response = stub.SayGoodbye(hello_pb2.GoodbyeRequest(name='Петя'))
        print("Greeter client received: " + response.message)
        if response.hello_count == 0:
            print("User is impolite!")


if __name__ == '__main__':
    logging.basicConfig()
    run()
