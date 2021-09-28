class NonZeroExitException(Exception):
    """Exception raised for errors from commands.

    Attributes:
        exit_code -- exit code returned from the command
        message -- message returned from command
        command -- the command ran
    """

    def __init__(self, exit_code: int, message: str, command: str):
        self.exit_code = exit_code
        self.message = message
        self.command = command
        super().__init__(self.message)
