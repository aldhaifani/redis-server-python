import asyncio

from app import RedisServer

"""
Main entry point for the Redis server.
"""
def main():
    server = RedisServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main()