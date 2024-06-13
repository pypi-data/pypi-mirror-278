from aau_ais_utilities.validate.imo import IMOValidator
import pytest

test_cases = []

invalid_prefix = ["IMOO", "IM", "IIMO", "" "MMSI"]
valid_imo_numbers = ["9074729", "0289239"]

for number in valid_imo_numbers:
    test_cases.append((number, True))  # IMO number without prefix
    test_cases.append((f"IMO {number}", True))  # IMO number with prefix

    for prefix in invalid_prefix:
        test_cases.append((f"{prefix} {number}", False))

invalid_imo_numbers = ["1111111", "2222222", "3333333"]

for number in invalid_imo_numbers:
    test_cases.append((number, False))
    test_cases.append((f"IMO {number}", False))

invalid_imo_numbers_len_short = [
    number[:-1] for number in valid_imo_numbers
]

for number in invalid_imo_numbers_len_short:
    test_cases.append((number, False))
    test_cases.append((f"IMO {number}", False))

invalid_imo_numbers_len_long = [
    number.join("1") for number in valid_imo_numbers
]

for number in invalid_imo_numbers_len_long:
    test_cases.append((number, False))
    test_cases.append((f"IMO {number}", False))


@pytest.mark.parametrize("imo, expected", test_cases)
def test_validate(imo, expected):
    validator = IMOValidator()

    assert validator.validate(imo) == expected


def test_error_messages():
    validator = IMOValidator()

    assert validator.validate("IMOO 9074729") == False

    error_last = validator.get_last_error()
    assert error_last[1] == "IMOO 9074729"
    assert len(validator.log) == 1



