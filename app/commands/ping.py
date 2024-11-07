from app import DatabaseHandler, ExpirationManager

COMMAND_NAME = "PING"

def handle_command(args: list, database: DatabaseHandler, expirations_manager: ExpirationManager) -> str:
    return "+PONG\r\n"