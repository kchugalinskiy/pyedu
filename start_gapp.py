import logging
import signal
import sys

from gapp.grpc.server import GRPCServer
from gapp.gen import hello_pb2_grpc
from gapp.controller.greeter import Greeter


def add_services(server):
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)


def signalHandler(signal, frame):
    print('Process Interrupted!\n\a')
    server.stop()
    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig()

    server = GRPCServer(port=8082)

    signal.signal(signal.SIGINT, signalHandler)

    add_services(server.instance)
    print('Server start')
    server.serve()
