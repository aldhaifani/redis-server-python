import pytest
import asyncio
import socket

@pytest.mark.asyncio
async def test_echo(start_redis_server):
    # Connect to the Redis server
    reader, writer = await asyncio.open_connection('localhost', 6379)

    # Send the ECHO command with a test message in RESP format: "*2\r\n$4\r\nECHO\r\n$5\r\nHello\r\n"
    echo_command = b"*2\r\n$4\r\nECHO\r\n$5\r\nHello\r\n"
    writer.write(echo_command)
    await writer.drain()

    # Read the response from the server
    response = await reader.read(1024)

    # Expected response: "$5\r\nHello\r\n"
    expected_response = b"$5\r\nHello\r\n"
    assert response == expected_response

    # Test ECHO with a long string
    long_message = b"A" * 1000
    echo_command_long = f"*2\r\n$4\r\nECHO\r\n${len(long_message)}\r\n{long_message.decode()}\r\n".encode()
    writer.write(echo_command_long)
    await writer.drain()
    response = await reader.read(1024)
    expected_response_long = f"${len(long_message)}\r\n{long_message.decode()}\r\n".encode()
    assert response == expected_response_long

    writer.close()
    await writer.wait_closed()
