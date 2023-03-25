import os
import logging

from controller import pb
from repo import pg


def run():
    print("Server starting")
    host = os.environ.get('GRPC_HOST')
    port = os.environ.get('GRPC_PORT')

    pghost = os.environ.get('POSTGRES_HOST')
    pgport = os.environ.get('POSTGRES_PORT')
    pguser = os.environ.get('POSTGRES_USER')
    pgpasswd = os.environ.get('POSTGRES_PASSWORD')
    pgdbname = os.environ.get('POSTGRES_DB')
    repo = pg.Repository(host=pghost, port=pgport, username=pguser, password=pgpasswd, dbname=pgdbname)
    print("Server starting, listening on " + host + port)
    proto_srv = pb.Greeter(host=host, port=port, repo=repo)
    proto_srv.serve()


if __name__ == '__main__':
    logging.basicConfig()
    run()
