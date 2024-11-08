import argparse
import asyncio

from app import RedisServer

"""
Main entry point for the Redis server.
"""
def main():
    """
    Parse command line arguments and start the Redis server.
    :return:
    """
    parser = argparse.ArgumentParser(description='Run a Redis server')
    parser.add_argument('--dir', type=str, help='Directory to store the database files', nargs='?', default='./rdb')
    parser.add_argument('--dbfilename', type=str, help='Database filename', nargs='?', default='dump.rdb')
    config = vars(parser.parse_args())

    server = RedisServer(config=config)
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    main()