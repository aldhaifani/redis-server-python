import asyncio

from app import RedisServer

"""
Main entry point for the Redis server.
"""

if __name__ == "__main__":
    server = RedisServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Server shutting down...")