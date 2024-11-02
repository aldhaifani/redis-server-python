import asyncio

"""
This is a simple Redis server that only responds to the PING command.
It handles multiple clients concurrently using asyncio, with a single thread.
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
                response = await self.process_command(data.decode())
                if response: # If there is a response, send it back to the client
                    writer.write(response)
                    await writer.drain()
        except Exception as e:
            print(e)
        finally:
            # Close the connection
            writer.close()
            await writer.wait_closed()

    async def process_command(self, command: str):
        """
        Process commands received from the client.
        :param command: command string
        :return: response string or None
        """
        if "PING" in command:
            return b"+PONG\r\n"
        else:
            return None

    async def start(self):
        """
        Start the server asynchronously and listen for incoming connections.
        :return: nothing
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        await server.serve_forever()

if __name__ == "__main__":
    redis_server = RedisServer()
    asyncio.run(redis_server.start())
