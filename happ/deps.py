from sqlalchemy.ext.asyncio import AsyncSession
from happ.db.session import assync_session
from happ.services.grpc.hello_pb2_grpc import GreeterStub
from happ.core.config import settings
import grpc
from happ.services.grpc import hello_pb2_grpc

greeter = GreeterStub


async def get_db() -> AsyncSession:
    async with assync_session() as session:
        yield session


def get_grpc_client():
    host = settings.GRPC_HOST
    port = settings.GRPC_PORT
    with grpc.insecure_channel(host + ':' + port) as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        yield stub
