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


async def runServers(repo: Repository, enable_http: bool, enable_grpc: bool):
    if enable_http:
        task1 = asyncio.create_task(serve_http(repo))
        await task1

    if enable_grpc:
        task2 = asyncio.create_task(run_grpc(repo))
        await task2


def run():
    repo = getDb()
    httpon = bool(os.environ.get('ENABLE_HTTP'))
    grpcon = bool(os.environ.get('ENABLE_GRPC'))
    try:
        asyncio.run(runServers(repo=repo, enable_http=httpon, enable_grpc=grpcon))
    except (asyncio.CancelledError, KeyboardInterrupt):
        print('program interrupted')
    except Exception as ex:
        print('exception:', ex)
    finally:
        print("program exit")


def run_http(repo: Repository):
    port = int(os.environ.get('HTTP_PORT'))
    print("http starting, listening on " + str(port))
    rest.run(port=port, repo=repo)


async def serve_http(repo: Repository):
    port = int(os.environ.get('HTTP_PORT'))
    print("http serving, listening on " + str(port))
    await rest.serve(port=port, repo=repo)


async def run_grpc(repo: Repository):
    host = os.environ.get('GRPC_HOST')
    port = os.environ.get('GRPC_PORT')
    print("grpc starting, listening on " + host + port)
    proto_srv = pb.Greeter(host=host, port=port, repo=repo)
    serve2 = asyncio.create_task(proto_srv.serve())
    await serve2


if __name__ == '__main__':
    logging.basicConfig()
    run()
