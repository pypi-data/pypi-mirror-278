import asyncio
import unittest

from superblocks_agent_sdk.client import Client, Config
from superblocks_types.api.v1.service_pb2_grpc import ExecutorServiceStub


class TestClient(unittest.TestCase):
    def test_bad_connection_info(self):
        client = Client(config=Config(token=""))
        with self.assertRaises(Exception) as context:
            asyncio.run(
                client._run(
                    with_stub=ExecutorServiceStub,
                    stub_func_name="TwoWayStream",
                    initial_request={},
                    response_handler=lambda _: True,
                )
            )
