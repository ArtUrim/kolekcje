#!/usr/bin/env python3
# coding: utf-8

"""
Module Name: test_isbn.py
Author:      artur
Date:        2026-08-13
Description:
"""


"""
Tests for ISBN validation module
"""
import pytest
from isbn import validate_isbn, normalize_isbn


class TestISBN10Validation:
    """Test ISBN-10 validation"""

    def test_valid_isbn10_with_numeric_check(self):
        """Test valid ISBN-10 with numeric check digit"""
        assert validate_isbn("0306406152") is True

    def test_valid_isbn10_with_x_check(self):
        """Test valid ISBN-10 with 'X' check digit"""
        assert validate_isbn("020161622X") is True
        assert validate_isbn("020161622x") is True  # lowercase x

    def test_valid_isbn10_with_hyphens(self):
        """Test valid ISBN-10 with hyphens"""
        assert validate_isbn("0-306-40615-2") is True

    def test_valid_isbn10_with_spaces(self):
        """Test valid ISBN-10 with spaces"""
        assert validate_isbn("0 306 40615 2") is True

    def test_invalid_isbn10_wrong_length(self):
        """Test invalid ISBN-10 with wrong length"""
        assert validate_isbn("030640615") is False
        assert validate_isbn("03064061523") is False

    def test_invalid_isbn10_bad_checksum(self):
        """Test invalid ISBN-10 with bad checksum"""
        assert validate_isbn("0306406153") is False  # Changed last digit

    def test_invalid_isbn10_non_digit_in_first_9(self):
        """Test invalid ISBN-10 with non-digit in first 9 positions"""
        assert validate_isbn("03064A6152") is False

    def test_invalid_isbn10_invalid_last_char(self):
        """Test invalid ISBN-10 with invalid last character (not digit or X)"""
        assert validate_isbn("030640615A") is False


class TestISBN13Validation:
    """Test ISBN-13 validation"""

    def test_valid_isbn13(self):
        """Test valid ISBN-13"""
        assert validate_isbn("9780306406157") is True

    def test_valid_isbn13_with_hyphens(self):
        """Test valid ISBN-13 with hyphens"""
        assert validate_isbn("978-0-306-40615-7") is True

    def test_valid_isbn13_with_spaces(self):
        """Test valid ISBN-13 with spaces"""
        assert validate_isbn("978 0 306 40615 7") is True

    def test_invalid_isbn13_wrong_length(self):
        """Test invalid ISBN-13 with wrong length"""
        assert validate_isbn("978030640615") is False
        assert validate_isbn("97803064061523") is False

    def test_invalid_isbn13_bad_checksum(self):
        """Test invalid ISBN-13 with bad checksum"""
        assert validate_isbn("9780306406158") is False  # Changed last digit

    def test_invalid_isbn13_with_x(self):
        """Test invalid ISBN-13 with 'X' (not allowed in ISBN-13)"""
        assert validate_isbn("978030640615X") is False

    def test_invalid_isbn13_non_digit(self):
        """Test invalid ISBN-13 with non-digit character"""
        assert validate_isbn("97803064061A7") is False


class TestNormalizeISBN:
    """Test ISBN normalization"""

    def test_normalize_isbn10(self):
        """Test normalizing ISBN-10"""
        assert normalize_isbn("0-306-40615-2") == "0306406152"
        assert normalize_isbn("0 306 40615 2") == "0306406152"

    def test_normalize_isbn10_with_x(self):
        """Test normalizing ISBN-10 with X"""
        assert normalize_isbn("0-201-61622-X") == "020161622X"
        assert normalize_isbn("0-201-61622-x") == "020161622X"  # lowercase to uppercase

    def test_normalize_isbn13(self):
        """Test normalizing ISBN-13"""
        assert normalize_isbn("978-0-306-40615-7") == "9780306406157"
        assert normalize_isbn("978 0 306 40615 7") == "9780306406157"

    def test_normalize_empty_or_none(self):
        """Test normalizing empty or None values"""
        assert normalize_isbn("") == ""
        assert normalize_isbn(None) == ""

    def test_normalize_already_clean(self):
        """Test normalizing already clean ISBN"""
        assert normalize_isbn("0306406152") == "0306406152"
        assert normalize_isbn("9780306406157") == "9780306406157"


class TestEdgeCases:
    """Test edge cases"""

    def test_empty_string(self):
        """Test empty string"""
        assert validate_isbn("") is False

    def test_none_value(self):
        """Test None value"""
        assert validate_isbn(None) is False

    def test_non_string_input(self):
        """Test non-string input"""
        assert validate_isbn(123) is False
        assert validate_isbn(1234567890) is False

    def test_whitespace_only(self):
        """Test whitespace-only string"""
        assert validate_isbn("   ") is False

    def test_mixed_format_valid(self):
        """Test mixed format that should be valid"""
        # Real ISBN-10 example
        assert validate_isbn("0-439-42089-X") is True

        # Real ISBN-13 example
        assert validate_isbn("978-0-439-42089-1") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
