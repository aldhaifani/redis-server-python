import subprocess

import pytest
import asyncio


@pytest.mark.asyncio
async def test_config_get(start_redis_server):
    # Connect to the Redis server
    reader, writer = await asyncio.open_connection('localhost', 6379)

    # Send the SET command in RESP format: "*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
    set_command = b"*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$3\r\ndir\r\n"
    writer.write(set_command)
    await writer.drain()

    # Read the response from the server
    response = await reader.read(1024)

    # Expected response:"*2\r\n$3\r\ndir\r\n$5\r\n./rdb\r\n"
    expected_response = b"*2\r\n$3\r\ndir\r\n$5\r\n./rdb\r\n"
    assert response == expected_response
