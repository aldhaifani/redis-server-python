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