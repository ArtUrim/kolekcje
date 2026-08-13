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
