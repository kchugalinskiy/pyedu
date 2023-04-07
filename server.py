import os
import logging
import asyncio

from controller import pb
from controller import rest
from repo.pg import Repository
from repo import pg


def getDb() -> Repository:
    pghost = os.environ.get('POSTGRES_HOST')
    pgport = os.environ.get('POSTGRES_PORT')
    pguser = os.environ.get('POSTGRES_USER')
    pgpasswd = os.environ.get('POSTGRES_PASSWORD')
    pgdbname = os.environ.get('POSTGRES_DB')
    return pg.Repository(host=pghost, port=pgport, username=pguser, password=pgpasswd, dbname=pgdbname)


async def runServers(repo: Repository, enableHttp: bool, enableGRPC: bool):
    if enableHttp:
        task1 = asyncio.create_task(serveHttp(repo))
        await task1

    if enableGRPC:
        task2 = asyncio.create_task(runGRPC(repo))
        await task2

def run():
    repo = getDb()
    httpon = bool(os.environ.get('ENABLE_HTTP'))
    grpcon = bool(os.environ.get('ENABLE_GRPC'))
    try:
        asyncio.run(runServers(repo=repo, enableHttp=httpon, enableGRPC=grpcon))
    except (asyncio.CancelledError, KeyboardInterrupt):
        print('program interrupted')
    except Exception as ex:
        print('exception:', ex)
    finally:
        print("program exit")


def runHttp(repo: Repository):
    port = int(os.environ.get('HTTP_PORT'))
    print("http starting, listening on " + str(port))
    rest_srv = rest.Rest(port=port, repo=repo)
    rest_srv.run()


async def serveHttp(repo: Repository):
    port = int(os.environ.get('HTTP_PORT'))
    print("http serving, listening on " + str(port))
    rest_srv = rest.Rest(port=port, repo=repo)
    await rest_srv.serve()


async def runGRPC(repo: Repository):
    host = os.environ.get('GRPC_HOST')
    port = os.environ.get('GRPC_PORT')
    print("grpc starting, listening on " + host + port)
    proto_srv = pb.Greeter(host=host, port=port, repo=repo)
    serve2 = asyncio.create_task(proto_srv.serve())
    await serve2


if __name__ == '__main__':
    logging.basicConfig()
    run()
