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
                    writer.write(response.encode())
                    await writer.drain()
        except Exception as e:
            print(e)
        finally:
            # Close the connection
            writer.close()
            await writer.wait_closed()

    async def process_command(self, data: str):
        """
        Process commands received from the client.
        :param data: data string
        :return: response string or None
        """
        commands = self.resp_parser(data)

        if "PING" in commands[0].upper(): # Handle the command PING
            return "+PONG\r\n"
        elif "ECHO" in commands[0].upper(): # Handle the command ECHO
            if len(commands) != 2 or len(commands[1]) == 0: # Error if no argument is provided
                return "-ERR wrong number of arguments for command\r\n"
            return f"${len(commands[1])}\r\n{commands[1]}\r\n"
        else:
            return None  # No response for invalid commands

    async def start(self):
        """
        Start the server asynchronously and listen for incoming connections.
        :return: nothing
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        await server.serve_forever() # Start the server and keep it running

    def resp_parser(self, data: str):
        """
        Parse RESP protocol data.
        :param data: data string to parse
        :return: commands list
        """
        data_list = data.strip().split("\r\n")
        commands = []

        # Filter out empty strings and protocol markers
        for d in data_list:
            if d[0] in ['*', '$', ':'] or len(d) == 0:
                continue
            else:
                commands.append(d)

        return commands


if __name__ == "__main__":
    redis_server = RedisServer()
    asyncio.run(redis_server.start())
