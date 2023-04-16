"""has all the system specific exceptions"""
import logging


class CommandException(Exception):
    """Exception that is raised if calling an external command fails"""

    def __init__(self, command):
        self.command = command

    def __str__(self):
        return self.command


class LogAndPrintException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.log_and_print()

    def log_and_print(self):
        self.logger.error(self)
        print(f"Error: {self=}, {type(self)=}")
