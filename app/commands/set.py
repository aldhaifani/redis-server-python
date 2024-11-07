from datetime import datetime, timedelta

from app import DatabaseHandler, ExpirationManager

COMMAND_NAME = "SET"

def handle_command(args: list, database: DatabaseHandler, expirations_manager: ExpirationManager) -> str:
    if len(args) < 2:
        return "-ERR wrong number of arguments for command\r\n"
    key = args[0]
    value = args[1]
    if len(args) > 2 and args[2].upper() == "PX":  # Handle expiry time
        if len(args) < 4:
            return "-ERR wrong number of arguments for command\r\n"
        try:
            expiry = int(args[3])
        except ValueError:
            return "-ERR invalid expire time\r\n"
        expiry_time = datetime.now() + timedelta(milliseconds=expiry)
        expirations_manager.set_expiration(key, expiry_time)
    database.set(key, value)
    return "+OK\r\n"