import logging


class Logger:
    """
    A class that provides a logger with a file and console handler.

    Methods:
    --------
    __init__(name: str, filename: str, log_to_console: bool)
        Initializes a logger with the specified name,
        file name and a flag to indicate if logging should be done to console.

    add_file_handler(filename: str) -> None
        Adds a file handler to the logger with the specified file name.

    """

    def __init__(self, name: str, log_filename: str, log_to_console: bool = False):
        """
        Initializes a logger with the specified name and file name.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
                )
            )
            self.logger.addHandler(console_handler)

        self.add_file_handler(log_filename)

    def add_file_handler(self, log_filename: str) -> None:
        """
        Adds a file handler to the logger with the specified file name.
        """
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
            )
        )
        self.logger.addHandler(file_handler)


logger = Logger(__name__, "accountract.log", log_to_console=True).logger
