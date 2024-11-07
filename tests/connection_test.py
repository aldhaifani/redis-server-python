import pytest
import asyncio


@pytest.mark.asyncio
async def test_ping(start_redis_server):
    # Connect to the Redis server
    reader, writer = await asyncio.open_connection('localhost', 6379)

    # Send the PING command in RESP format: "*1\r\n$4\r\nPING\r\n"
    ping_command = b"*1\r\n$4\r\nPING\r\n"
    writer.write(ping_command)
    await writer.drain()

    # Read the response from the server
    response = await reader.read(1024)

    # Expected response: "+PONG\r\n"
    expected_response = b"+PONG\r\n"
    assert response == expected_response

    writer.close()
    await writer.wait_closed()
