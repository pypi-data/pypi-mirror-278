"""Module for IMO number validation."""
from .validator import Validator


class IMOValidator(Validator):
    """Class for IMO number validation."""

    @property
    def error_messages(self) -> dict:
        return {
            "incorrect_format": "Incorrect Format - IMO number must be 7 digits long. May include the prefix 'IMO'.",
            "failed_algorithm": "Invalid IMO number - Did not pass the IMO validation algorithm."
        }

    def __init__(self) -> None:
        """Initialize the IMOValidator class."""
        super().__init__()

    def validate(self, imo: int) -> bool:
        """Validate IMO number.

        Args:
            imo (str): IMO number to validate.
        """
        imo = str(imo).zfill(7)

        imo_parsed = self._parse_imo(imo)

        if not imo_parsed.isdigit() or len(imo_parsed) != 7:
            self._add_error_to_log("incorrect_format", imo)
            return False

        if self.validate_vessel(imo_parsed):
            return True

        if self.validate_company_vessel(imo_parsed):
            return True

        self._add_error_to_log("failed_algorithm", imo)
        return False

    @staticmethod
    def _parse_imo(imo: str) -> str:
        """Parse IMO number, removing any whitespace or IMO prefix.

        Args:
            imo (str): IMO number to parse.
        """

        imo = imo.replace(" ", "").upper()

        if imo.startswith("IMO"):
            imo = imo[3:]

        return imo

    @staticmethod
    def validate_vessel(imo: str) -> bool:
        """Validate IMO number for a vessel.

        This IMO number validation algorithm is the first of 2 validation algorithms for IMO numbers, see:
        https://en.wikipedia.org/wiki/IMO_number#Structure

        Args:
            imo (str): IMO number to validate.
        """

        check_digit = int(imo[-1])
        numbers = (int(digit) for digit in imo[:-1])

        factor = 7
        summation = 0
        for number in numbers:
            summation += number * factor
            factor -= 1

        return summation % 10 == check_digit

    @staticmethod
    def validate_company_vessel(imo: str) -> bool:
        """Validate IMO number for a company vessel.

        This IMO number validation algorithm is the second of 2 algorithms for IMO numbers, see:
        https://en.wikipedia.org/wiki/IMO_number#Structure

        Args:
            imo (str): IMO number to validate.
        """

        check_digit = int(imo[-1])
        numbers = (int(digit) for digit in imo[:-1])
        weights = (8, 6, 4, 2, 9, 7)

        summation = 0
        for e1, e2 in zip(numbers, weights):
            summation += e1 * e2

        return ((11 - (summation % 11)) % 10) == check_digit
