"""
Utility functions for the application.
"""

def resp_parser(data: str) -> list:
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

def config_handler(args: list, config: dict) -> str:
    """
    Handle CONFIG command.
    :param args: arguments list
    :param config: configuration dictionary
    :return:
    """
    if len(args) < 2:
        return "-ERR wrong number of arguments for command\r\n"

    if args[1].upper() == "GET": # Handle GET command
        try:
            config_key = args[2].lower()
            config_value = config[config_key]
            return f"*2\r\n${len(config_key)}\r\n{config_key}\r\n${len(config_value)}\r\n{config_value}\r\n"
        except KeyError:
            return "$-1\r\n"