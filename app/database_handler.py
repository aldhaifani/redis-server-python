"""
This module contains the DatabaseHandler class which is responsible for handling the database operations.
"""
class DatabaseHandler:
    def __init__(self):
        self.db = {}

    def set(self, key: str, value: str) -> str:
        """
        Set the value of a key in the database.
        :param key: key to set, str
        :param value: value to set, str
        :return: response string, RESP protocol
        """
        self.db[key] = value
        return "+OK\r\n"

    def get(self, key: str) -> str:
        """
        Get the value of a key from the database.
        :param key: key to get, str
        :return: response string, RESP protocol
        """
        if key in self.db:
            return self.db.get(key)
        else:
            return "$-1\r\n"

    def delete(self, key: str):
        """
        Delete a key from the database.
        :param key: key to delete, str
        :return:
        """
        if key in self.db:
            del self.db[key]

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the database.
        :param key: key to check, str
        :return: True if key exists, False otherwise
        """
        return key in self.db
