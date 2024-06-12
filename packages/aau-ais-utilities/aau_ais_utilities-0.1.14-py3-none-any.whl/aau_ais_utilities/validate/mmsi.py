"""Module for MMSI number validation."""
from .validator import Validator


class MMSIValidator(Validator):

    @property
    def error_messages(self) -> dict:
        return {
            "incorrect_format": "Incorrect Format - MMSI number must be 9 digits long."
        }

    def __init__(self) -> None:
        """Initialize the MMSIValidator class."""
        super().__init__()

    def validate(self, mmsi: int) -> bool:
        """Validate MMSI number.

        Args:
            mmsi (int): MMSI number to validate.
        """
        mmsi = str(mmsi).rjust(9, "0")

        mmsi = self._parse_mmsi(mmsi)

        if not mmsi.isdigit() or len(mmsi) != 9:
            self._add_error_to_log("incorrect_format", mmsi)
            return False

        return True

    @staticmethod
    def _parse_mmsi(mmsi: str) -> str:
        """Parse MMSI number, removing any whitespace or MMSI prefix.

        Args:
            mmsi (str): MMSI number to parse.
        """

        mmsi = mmsi.replace(" ", "")

        if mmsi.upper().startswith("MMSI"):
            mmsi = mmsi[4:]

        return mmsi
