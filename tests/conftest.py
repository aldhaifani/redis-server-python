import subprocess
import pytest
import socket
import time


@pytest.fixture(scope="session")
def start_redis_server():
    # Start the Redis server in a subprocess
    server_process = subprocess.Popen(
        ["python", "-m", "app.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Allow some time for the server to start
    time.sleep(2)

    # Ensure the server is running by checking if the socket is available
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_up = False
    try:
        sock.connect(('localhost', 6379))
        server_up = True
    except Exception as e:
        pytest.fail(f"Redis server failed to start.\n{e}")
    finally:
        sock.close()

    yield server_process

    # Terminate the server after tests
    server_process.terminate()
    server_process.wait()
