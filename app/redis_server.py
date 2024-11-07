import asyncio

from app import CommandHandler, DatabaseHandler, ExpirationManager
from app.utils import resp_parser

"""
A simple Redis server implementation.

Redis commands supported:
- PING
- ECHO message
- SET key value [PX milliseconds]
- GET key

Handles multiple clients concurrently using asyncio.
"""
class RedisServer:
    def __init__(self, host: str = "localhost", port: int = 6379):
        """
        Set the host and port for the server.
        :param host: host name or IP address, str
        :param port: port number, int
        """
        self.port = port
        self.host = host
        self.db = DatabaseHandler()
        self.expirations_manager = ExpirationManager()
        self.command_handler = CommandHandler(self.db, self.expirations_manager)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handle a single client connection.
        Read commands from the client, process them, and send a response.
        :param reader: reader object
        :param writer: writer object
        :return: nothing
        """
        try:
            while True: # Loop to read commands from the client
                data = await reader.read(1024)
                # If no data is received, the client has closed the connection
                if not data:
                    break
                command = resp_parser(data.decode()) # Parse the command
                # Handle the command and get the response
                response = await self.command_handler.handle_command(command[0], command[1:])
                if response: # If there is a response, send it back to the client
                    writer.write(response.encode())
                    await writer.drain()
        except Exception as e:
            print(e)
        finally:
            # Close the connection
            writer.close()
            await writer.wait_closed()

    async def start(self):
        """
        Start the server asynchronously and listen for incoming connections.
        :return: nothing
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            await server.serve_forever()
