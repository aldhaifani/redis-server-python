import pytest
import asyncio
import socket

@pytest.mark.asyncio
async def test_set_get(start_redis_server):
    # Connect to the Redis server
    reader, writer = await asyncio.open_connection('localhost', 6379)

    # Send the SET command in RESP format: "*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
    set_command = b"*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"
    writer.write(set_command)
    await writer.drain()

    # Read the response from the server
    response = await reader.read(1024)

    # Expected response: "+OK\r\n"
    expected_response = b"+OK\r\n"
    assert response == expected_response

    # Send the GET command: "*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n"
    get_command = b"*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n"
    writer.write(get_command)
    await writer.drain()

    # Read the response from the server
    response = await reader.read(1024)

    # Expected response: "$3\r\nbar\r\n"
    expected_response = b"$3\r\nbar\r\n"
    assert response == expected_response

    # Test GET for a key that doesn't exist
    get_command_non_existent = b"*2\r\n$3\r\nGET\r\n$4\r\nnonexistent\r\n"
    writer.write(get_command_non_existent)
    await writer.drain()

    # Expected response for non-existent key: "$-1\r\n"
    response = await reader.read(1024)
    expected_response_non_existent = b"$-1\r\n"
    assert response == expected_response_non_existent

    # # Test SET with an empty value
    # set_command_empty = b"*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n$0\r\n\r\n"
    # writer.write(set_command_empty)
    # await writer.drain()
    #
    # # Expected response: "+OK\r\n"
    # response = await reader.read(1024)
    # expected_response_empty = b"+OK\r\n"
    # assert response == expected_response_empty

    # # Test GET with an empty string
    # get_command_empty = b"*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n"
    # writer.write(get_command_empty)
    # await writer.drain()
    #
    # # Expected response for an empty value: "$0\r\n\r\n"
    # response = await reader.read(1024)
    # expected_response_empty_get = b"$0\r\n\r\n"
    # assert response == expected_response_empty_get

    # Test SET with a large string (e.g., 500 characters)
    long_value = b"B" * 500
    set_command_large = f"*3\r\n$3\r\nSET\r\n$3\r\nfoo\r\n${len(long_value)}\r\n{long_value.decode()}\r\n".encode()
    writer.write(set_command_large)
    await writer.drain()

    # Expected response: "+OK\r\n"
    response = await reader.read(1024)
    expected_response_large = b"+OK\r\n"
    assert response == expected_response_large

    # Test GET for the large string
    get_command_large = b"*2\r\n$3\r\nGET\r\n$3\r\nfoo\r\n"
    writer.write(get_command_large)
    await writer.drain()

    # Read the response from the server (large string)
    response = await reader.read(1024)

    # Expected response for the large string
    expected_response_large_get = f"${len(long_value)}\r\n{long_value.decode()}\r\n".encode()
    assert response == expected_response_large_get

    writer.close()
    await writer.wait_closed()
