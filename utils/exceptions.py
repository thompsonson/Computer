"""has all the system specific exceptions"""


class CommandException(Exception):
    """Exception that is raised if calling an external command fails"""

    def __init__(self, command):
        self.command = command

    def __str__(self):
        return self.command
