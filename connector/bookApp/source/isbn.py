#!/usr/bin/env python3
# coding: utf-8

"""
Module Name: isbn.py
Author:      artur
Date:        2026-08-13
Description:
"""

import requests
import xml.etree.ElementTree as ET

URL = "https://e-isbn.pl/IsbnWeb/api.xml"

def isbn2Book( isbn ):
    response = requests.get(URL, params={"isbn": isbn}, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    for element in root.iter():
        if element.text and element.text.strip():
            print(element.tag, element.text.strip())


def isbn10_to_isbn13(isbn10: str) -> str:
    value = isbn10.replace("-", "").replace(" ", "").upper()

    if len(value) != 10:
        raise ValueError("ISBN-10 powinien mieć 10 znaków")

    body = value[:9]
    check = value[9]

    if not all(c.isdigit() for c in body):
        raise ValueError("Nieprawidłowy ISBN-10")

    # Opcjonalnie można tu zweryfikować starą cyfrę kontrolną.
    digits = [int(c) for c in "978" + body]

    total = sum(
        digit * (1 if index % 2 == 0 else 3)
        for index, digit in enumerate(digits)
    )
    new_check = (10 - total % 10) % 10

    return "978" + body + str(new_check)

"""
ISBN Validation Module

Validates ISBN-10 and ISBN-13 formats including checksum verification.
- ISBN-10: 10 digits, last digit can be 'X' (representing 10)
- ISBN-13: 13 digits, last digit is a check digit (0-9)
"""

def validate_isbn(isbn: str) -> bool:
    """
    Validate an ISBN string (either ISBN-10 or ISBN-13).

    Args:
        isbn: The ISBN string to validate

    Returns:
        True if the ISBN is valid, False otherwise
    """
    if not isbn or not isinstance(isbn, str):
        return False

    # Remove hyphens and spaces
    cleaned = isbn.replace('-', '').replace(' ', '').strip()

    if len(cleaned) == 10:
        return _validate_isbn10(cleaned)
    elif len(cleaned) == 13:
        return _validate_isbn13(cleaned)
    else:
        return False


def _validate_isbn10(isbn: str) -> bool:
    """
    Validate ISBN-10 format with checksum.

    The check digit for ISBN-10 is calculated as follows:
    - Multiply each of the first 9 digits by its position (1-9)
    - Sum these products
    - The check digit (position 10) should make the total sum divisible by 11
    - Check digit can be 0-9 or 'X' (representing 10)

    Args:
        isbn: A 10-character ISBN string

    Returns:
        True if valid, False otherwise
    """
    if len(isbn) != 10:
        return False

    # First 9 characters must be digits
    for i in range(9):
        if not isbn[i].isdigit():
            return False

    # Last character can be digit or 'X'/'x'
    last_char = isbn[9].upper()
    if last_char == 'X':
        check_value = 10
    elif last_char.isdigit():
        check_value = int(last_char)
    else:
        return False

    # Calculate checksum: sum of (digit * position) for positions 1-9
    total = 0
    for i in range(9):
        total += int(isbn[i]) * (i + 1)

    # Add the check digit multiplied by 10
    total += check_value * 10

    # Valid if total is divisible by 11
    return total % 11 == 0


def _validate_isbn13(isbn: str) -> bool:
    """
    Validate ISBN-13 format with checksum.

    The check digit for ISBN-13 is calculated as follows:
    - Multiply digits alternately by 1 and 3 (starting with 1)
    - Sum these products
    - The check digit should make the total sum divisible by 10

    Args:
        isbn: A 13-character ISBN string (all digits)

    Returns:
        True if valid, False otherwise
    """
    if len(isbn) != 13:
        return False

    # All characters must be digits
    if not isbn.isdigit():
        return False

    # Calculate checksum using alternating weights 1 and 3
    total = 0
    for i in range(13):
        weight = 1 if i % 2 == 0 else 3
        total += int(isbn[i]) * weight

    # Valid if total is divisible by 10
    return total % 10 == 0


def normalize_isbn(isbn: str) -> str:
    """
    Normalize an ISBN string by removing hyphens and spaces.

    Args:
        isbn: The ISBN string to normalize

    Returns:
        Normalized ISBN string (digits only, except possibly 'X' at end for ISBN-10)
    """
    if not isbn or not isinstance(isbn, str):
        return ''

    cleaned = isbn.replace('-', '').replace(' ', '').strip()
    return cleaned.upper()  # Convert 'x' to 'X' for ISBN-10

def main():
    if len(isbn) == 10:
        isbn13 = isbn10_to_isbn13(isbn)
    else:
        isbn13 = isbn

    isbn2Book(isbn13)

if __name__ == "__main__":

    isbn = "9788327600035"
    main(isbn)
    isbn="8303022474"
    main(isbn)
