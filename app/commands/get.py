from app import DatabaseHandler, ExpirationManager

COMMAND_NAME = "GET"

def handle_command(args: list, database: DatabaseHandler, expirations_manager: ExpirationManager) -> str:
    if len(args) != 1:
        return "-ERR wrong number of arguments for command\r\n"
    key = args[0]
    # Check if key exists and is not expired
    if database.exists(key) and not expirations_manager.check_expiration(key):
        v = database.get(key)
        return f"${len(v)}\r\n{v}\r\n"
    else:
        # Delete the key if it is expired
        if expirations_manager.check_expiration(key):
            database.delete(key)
            expirations_manager.remove_expiration(key)
        return "$-1\r\n"