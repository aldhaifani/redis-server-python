from app import DatabaseHandler, ExpirationManager

COMMAND_NAME = "ECHO"

def handle_command(args: list, database: DatabaseHandler, expirations_manager: ExpirationManager) -> str:
    if len(args) != 1:  # Error if no argument is provided
        return "-ERR wrong number of arguments for command\r\n"
    if len(args[0]) == 0:
        return "$0\r\n\r\n"
    return f"${len(args[0])}\r\n{args[0]}\r\n"