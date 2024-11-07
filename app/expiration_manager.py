from datetime import datetime

"""
ExpirationManager class to manage key expirations for the SET command.
"""
class ExpirationManager:
    def __init__(self):
        self.expirations = {}

    def set_expiration(self, key: str, expiry_time: datetime):
        """
        Set the expiration time for a key.
        :param key: key to set expiration for
        :param expiry_time: expiration time
        :return:
        """
        self.expirations[key] = expiry_time

    def check_expiration(self, key: str) -> bool:
        """
        Check if a key has expired.
        :param key: key to check
        :return: True if key has expired, False otherwise
        """
        if key in self.expirations:
            if datetime.now() >= self.expirations[key]:
                del self.expirations[key]
                return True
        return False

    def remove_expiration(self, key: str):
        """
        Remove the expiration time for a key.
        :param key: key to remove expiration for
        :return:
        """
        if key in self.expirations:
            del self.expirations[key]