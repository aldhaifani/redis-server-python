from app import RedisServer
import pytest
import socket

@pytest.fixture(scope="session")
def server():
    server = RedisServer()
    server.start()
    yield server
    server.stop()

@pytest.fixture(scope="session")
def tcp_connection(server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 6379))
    yield sock
    sock.close()