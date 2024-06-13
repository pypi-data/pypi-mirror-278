from abc import ABC, abstractmethod
from datetime import datetime


class Validator(ABC):
    """Abstract class for data validation.

    Contains methods for validating data and logging errors to a log if validation fails.
    Log messages are stored in the format [datetime, data, error_message].
    """

    @property
    @abstractmethod
    def error_messages(self) -> dict:
        pass

    def __init__(self):
        self.log = []

    @abstractmethod
    def validate(self, data) -> bool:
        pass

    def _add_error_to_log(self, error_key: str, data: str) -> None:
        """Add a message to the log.

        Args:
            error_key (str): The message to add to the log.
        """
        log_message = self.error_messages.get(error_key)

        if log_message is None:
            raise ValueError(f"Error message '{error_key}' not found.")

        self.log.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data, log_message])

    def get_log(self) -> list[list[datetime, str, str]]:
        """Return the log."""

        return self.log

    def get_last_error(self) -> list[datetime, str, str]:
        """Return the last error in the log."""

        return self.log[-1]
