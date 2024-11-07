from importlib import import_module

"""
CommandHandler class is responsible for handling the commands received from the client.
"""
class CommandHandler:
    def __init__(self, database, expiration_manager):
        self.database = database
        self.expiration_manager = expiration_manager
        self.command_registry = self.load_commands()

    def load_commands(self) -> dict:
        """
        Load all the commands from the commands directory and create a registry of commands.
        :return: A dictionary with the command name as the key and the command handler as the value.
        """
        commands_registry = {}
        supported_commands = ["PING", "ECHO", "SET", "GET"]

        for command in supported_commands:
            try:
                # Import the module dynamically
                module = import_module(f"app.commands.{command.lower()}")
                commands_registry[module.COMMAND_NAME] = module.handle_command
            except ImportError as e:
                print(f"Error loading command {command}: {e}")

        return commands_registry

    async def handle_command(self, command: str, args: list) -> str:
        """
        Handle the command by calling the appropriate command handler.
        :param command: command name
        :param args: arguments for the command
        :return: The response from the command handler
        """
        command = command.upper()
        if command in self.command_registry:
            return self.command_registry[command](args, self.database, self.expiration_manager)
        else:
            return "-ERR unknown command\r\n"